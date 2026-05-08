import os
from pathlib import Path

# Charge les variables d'environnement depuis .env si présent.
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'
if ENV_PATH.exists():
    with ENV_PATH.open('r', encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'una_site.settings')

import django
from django.conf import settings
from django.core.files import File

django.setup()

from vie_estudiantine_una.models import (
    Actualite,
    Evenement,
    ServiceCROU,
    Partenaire,
    AboutUNA,
    Slide,
    Acteur,
    Temoin,
    Club_association,
    Banner,
    Profile,
    Post,
)

MIGRATION_MAP = {
    Actualite: ['image', 'image_auteur'],
    Evenement: ['photo'],
    ServiceCROU: ['image'],
    Partenaire: ['logo'],
    AboutUNA: ['image'],
    Slide: ['image'],
    Acteur: ['photo'],
    Temoin: ['photo'],
    Club_association: ['logo'],
    Banner: ['image'],
    Profile: ['photo'],
    Post: ['image'],
}


def migrate_file(instance, field_name):
    file_field = getattr(instance, field_name)
    if not file_field or not getattr(file_field, 'name', None):
        return False

    filename = file_field.name
    if filename.lower().startswith(('http://', 'https://')):
        return False

    local_path = Path(settings.MEDIA_ROOT) / filename
    if not local_path.exists():
        print(f"[SKIP] fichier introuvable: {local_path}")
        return False

    with local_path.open('rb') as file_obj:
        file_field.save(filename, File(file_obj), save=False)

    instance.save(update_fields=[field_name])
    print(f"[MIGRATED] {instance.__class__.__name__}#{instance.pk}.{field_name} -> {filename}")
    return True


def main():
    total = 0
    for model, fields in MIGRATION_MAP.items():
        qs = model.objects.all()
        print(f"Migration pour {model.__name__}: {qs.count()} objets")
        for instance in qs:
            for field_name in fields:
                if migrate_file(instance, field_name):
                    total += 1

    print(f"Migration terminée. {total} fichier(s) envoyés vers Cloudinary.")


if __name__ == '__main__':
    main()
