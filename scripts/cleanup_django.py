#!/usr/bin/env python3
"""
cleanup_django.py

Usage:
  python scripts/cleanup_django.py [--apply] [--fix-imports] [--archive-dir ARCHIVE_DIR]

Features:
  - Supprime tous les dossiers __pycache__ et tous les fichiers .pyc
  - Archive les apps non listées dans INSTALLED_APPS vers `archive/` (configurable)
  - Supprime toutes les migrations dans chaque app sauf __init__.py
  - Vérifie les imports inutilisés et (optionnellement) les supprime si --fix-imports est fourni
  - Affiche un résumé des fichiers supprimés / archivés

Notes:
  - Par défaut le script tourne en "dry-run" (ne fait rien). Passez --apply pour effectuer les changements.
  - Passez --fix-imports en conjonction avec --apply pour que le script modifie les fichiers Python et enlève
    automatiquement les imports complètement inutilisés. Les suppressions partielles sont gérées pour
    les lignes "from module import a, b" si seulement certains noms sont utilisés.

"""

import argparse
import ast
from collections import defaultdict
from pathlib import Path
import shutil
import sys
import re
from typing import List, Tuple, Set, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {"env", "venv", "node_modules", "static", "stactic", "media", "templates", "archive"}


def parse_installed_apps(settings_path: Path) -> List[str]:
    """Parse INSTALLED_APPS from Django settings without importing Django."""
    try:
        text = settings_path.read_text(encoding="utf-8")
    except Exception:
        return []

    try:
        module = ast.parse(text)
    except Exception:
        return []

    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "INSTALLED_APPS":
                    try:
                        value = ast.literal_eval(node.value)
                        return list(value)
                    except Exception:
                        # Could not literal_eval (maybe dynamic), fall back to regex extract
                        m = re.search(r"INSTALLED_APPS\s*=\s*(\[.*?\]|\(.*?\))", text, re.S)
                        if m:
                            try:
                                return list(ast.literal_eval(m.group(1)))
                            except Exception:
                                return []
    return []


def find_pycache_and_pyc(root: Path) -> Tuple[List[Path], List[Path]]:
    pyc_files = []
    pycache_dirs = []
    for p in root.rglob("*"):
        # Skip any files or directories that live inside excluded directories (env, venv, node_modules...)
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.is_dir() and p.name == "__pycache__":
            pycache_dirs.append(p)
        elif p.is_file() and p.suffix == ".pyc":
            pyc_files.append(p)
    return pycache_dirs, pyc_files


def find_candidate_apps(root: Path) -> List[Path]:
    candidates = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if child.name in EXCLUDE_DIRS:
            continue
        # consider a directory an app if it contains apps.py or models.py or migrations dir
        if (child / "apps.py").exists() or (child / "models.py").exists() or (child / "migrations").exists():
            candidates.append(child)
    return candidates


def get_base_app_names(installed_apps: List[str]) -> Set[str]:
    bases = set()
    for item in installed_apps:
        if not isinstance(item, str):
            continue
        base = item.split(".")[0]
        bases.add(base)
    return bases


def archive_app(app_path: Path, archive_root: Path, apply: bool) -> Tuple[bool, Path]:
    target = archive_root / app_path.name
    if apply:
        archive_root.mkdir(parents=True, exist_ok=True)
        # In case already exists, move to a timestamped folder
        if target.exists():
            import datetime
            target = archive_root / f"{app_path.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(app_path), str(target))
        return True, target
    else:
        return True, target


def clean_migrations(app_path: Path, apply: bool) -> List[Path]:
    removed = []
    mig = app_path / "migrations"
    if not mig.exists() or not mig.is_dir():
        return removed
    for p in mig.iterdir():
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py":
            removed.append(p)
            if apply:
                p.unlink()
    return removed


# --- Import analysis ---

def analyze_unused_imports(file_path: Path) -> Tuple[Dict[int, ast.AST], Dict[str, Tuple[ast.AST, List[str]]]]:
    """
    Return a tuple:
      - mapping lineno -> import AST node
      - mapping imported_name -> (import node, list of alias names)
    Also compute used names and determine which imports are unused.
    """
    text = file_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}, {}

    imports_by_line = {}
    import_entries = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports_by_line[node.lineno] = node
            if isinstance(node, ast.Import):
                for alias in node.names:
                    asname = alias.asname or alias.name.split(".")[0]
                    import_entries[asname] = (node, [alias.name])
            else:  # ImportFrom
                # skip import *
                if any(alias.name == "*" for alias in node.names):
                    continue
                for alias in node.names:
                    asname = alias.asname or alias.name
                    import_entries[asname] = (node, [alias.name])

    # collect used names
    used = set()
    class NameVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            used.add(node.id)
            self.generic_visit(node)

        def visit_Attribute(self, node):
            # collect top-level name for attribute chains: module.attr
            val = node
            while isinstance(val, ast.Attribute):
                val = val.value
            if isinstance(val, ast.Name):
                used.add(val.id)
            self.generic_visit(node)

    NameVisitor().visit(tree)

    unused = {}
    for name, (node, original_names) in import_entries.items():
        if name not in used:
            unused[name] = (node, original_names)

    return imports_by_line, unused


def fix_unused_imports_in_file(file_path: Path, apply: bool) -> Tuple[List[str], List[str]]:
    """Return (fixed_lines, messages) where fixed_lines lists modified lines and messages describes changes."""
    text = file_path.read_text(encoding="utf-8")
    imports_by_line, unused = analyze_unused_imports(file_path)
    if not unused:
        return [], []

    lines = text.splitlines()
    messages = []
    modified_lines = []

    # groupunused by line
    lines_to_modify = defaultdict(list)
    for name, (node, original_names) in unused.items():
        lines_to_modify[node.lineno].append((name, node))

    # process lines descending to avoid messing indices
    for lineno in sorted(lines_to_modify.keys(), reverse=True):
        node = imports_by_line.get(lineno)
        if node is None:
            continue
        orig = lines[lineno - 1]
        if isinstance(node, ast.Import):
            # all aliases unused? If any alias still used skip.
            names = [a.asname or a.name.split(".")[0] for a in node.names]
            unused_aliases = [n for n in names if n in [u[0] for u in lines_to_modify[lineno]]]
            if len(unused_aliases) == len(names):
                messages.append(f"Removing import line {lineno}: {orig.strip()}")
                modified_lines.append(orig)
                if apply:
                    lines.pop(lineno - 1)
            else:
                # remove only unused aliases
                keep = [a for a in node.names if (a.asname or a.name.split(".")[0]) not in unused_aliases]
                new_code = "import " + ", ".join(a.name + (" as " + a.asname if a.asname else "") for a in keep)
                messages.append(f"Replacing import line {lineno} with: {new_code}")
                modified_lines.append(orig)
                if apply:
                    lines[lineno - 1] = new_code
        elif isinstance(node, ast.ImportFrom):
            # If all names are unused, remove line. If some used, keep used names.
            names = [a.name for a in node.names if a.name != "*"]
            unused_names = [n for n in names if (n not in [u[0] for u in lines_to_modify[lineno]] and (n not in analyze_real_usage(file_path, n)) )]
            # The above is conservative; instead, check alias names in import_entries
            # Simpler approach: determine used alias names from unused mapping
            unused_aliases = [nm for nm, nd in lines_to_modify[lineno]]
            if len(unused_aliases) >= len(names):
                messages.append(f"Removing from-import line {lineno}: {orig.strip()}")
                modified_lines.append(orig)
                if apply:
                    lines.pop(lineno - 1)
            else:
                # keep used aliases
                keep_aliases = [a for a in node.names if (a.asname or a.name) not in unused_aliases]
                if not keep_aliases:
                    if apply:
                        lines.pop(lineno - 1)
                    messages.append(f"Removing from-import line {lineno}: {orig.strip()}")
                    modified_lines.append(orig)
                else:
                    new_code = f"from {'.' * node.level + (node.module or '')} import " + ", ".join(a.name + (" as " + a.asname if a.asname else "") for a in keep_aliases)
                    messages.append(f"Replacing from-import line {lineno} with: {new_code}")
                    modified_lines.append(orig)
                    if apply:
                        lines[lineno - 1] = new_code

    if apply and modified_lines:
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return modified_lines, messages


def analyze_real_usage(file_path: Path, name: str) -> Set[str]:
    # helper (kept for potential future use)
    return set()


def main():
    parser = argparse.ArgumentParser(description="Cleanup Django project: remove pyc/__pycache__, archive unused apps, remove migrations, check/fix unused imports")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--fix-imports", action="store_true", help="Attempt to remove unused imports (works only with --apply to actually modify files)")
    parser.add_argument("--archive-dir", default=str(PROJECT_ROOT / "archive"), help="Directory to move archived apps into")
    parser.add_argument("--settings", default=str(PROJECT_ROOT / "una_site" / "settings.py"), help="Path to Django settings.py to read INSTALLED_APPS")
    args = parser.parse_args()

    apply = args.apply
    fix_imports = args.fix_imports
    archive_dir = Path(args.archive_dir)
    settings_path = Path(args.settings)

    summary = {
        "pycache_dirs_removed": [],
        "pyc_files_removed": [],
        "archived_apps": [],
        "migrations_removed": [],
        "imports_report": defaultdict(list),
        "errors": []
    }

    # 1) pycache & pyc
    pycache_dirs, pyc_files = find_pycache_and_pyc(PROJECT_ROOT)
    for d in pycache_dirs:
        summary["pycache_dirs_removed"].append(d)
        if apply:
            try:
                shutil.rmtree(d)
            except Exception as e:
                summary["errors"].append((d, str(e)))
    for f in pyc_files:
        summary["pyc_files_removed"].append(f)
        if apply:
            try:
                f.unlink()
            except Exception as e:
                summary["errors"].append((f, str(e)))

    # 2) archive unused apps
    installed_apps = parse_installed_apps(settings_path)
    installed_bases = get_base_app_names(installed_apps)
    candidates = find_candidate_apps(PROJECT_ROOT)
    for app in candidates:
        if app.name not in installed_bases:
            ok, target = archive_app(app, archive_dir, apply)
            summary["archived_apps"].append((app, target))

    # 3) remove migrations except __init__.py
    for app in (PROJECT_ROOT,):
        for candidate in candidates:
            removed = clean_migrations(candidate, apply)
            for r in removed:
                summary["migrations_removed"].append(r)

    # 4) check unused imports
    py_files = [p for p in PROJECT_ROOT.rglob("*.py") if not any(part in EXCLUDE_DIRS for part in p.parts)]
    for p in py_files:
        imports_by_line, unused = analyze_unused_imports(p)
        if unused:
            summary["imports_report"][p] = list(unused.keys())
            if fix_imports and apply:
                modified, messages = fix_unused_imports_in_file(p, apply=True)
                summary["imports_report"][p] = {"unused": list(unused.keys()), "modified_lines": modified, "messages": messages}

    # 5) summary
    print("\n=== Résumé de l'opération ===\n")
    print(f"Mode: {'APPLY' if apply else 'DRY-RUN (aucun changement effectué)'}")
    print(f"Dossiers __pycache__ trouvés: {len(summary['pycache_dirs_removed'])}")
    for d in summary['pycache_dirs_removed']:
        print(f"  - {d}")
    print(f"Fichiers .pyc trouvés: {len(summary['pyc_files_removed'])}")
    for f in summary['pyc_files_removed']:
        print(f"  - {f}")

    print(f"Apps archivées: {len(summary['archived_apps'])}")
    for src, tgt in summary['archived_apps']:
        print(f"  - {src} -> {tgt}")

    print(f"Migrations supprimées: {len(summary['migrations_removed'])}")
    for m in summary['migrations_removed']:
        print(f"  - {m}")

    if summary['imports_report']:
        print("\nImports inutilisés détectés: \n")
        for p, data in summary['imports_report'].items():
            print(f"{p}:")
            if isinstance(data, dict):
                print(f"  Unused: {data.get('unused')}")
                if data.get('modified_lines'):
                    print(f"  Modified lines: {len(data['modified_lines'])}")
                    for ln in data['modified_lines']:
                        print(f"    - {ln.strip()}")
                    for msg in data['messages']:
                        print(f"    * {msg}")
            else:
                print(f"  Unused names: {data}")

    if summary['errors']:
        print("\nErreurs rencontrées:\n")
        for e in summary['errors']:
            print(f"  - {e[0]}: {e[1]}")

    print("\nOpération terminée.")


if __name__ == "__main__":
    main()
