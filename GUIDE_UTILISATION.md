# 🎓 Guide d'Utilisation - Site UNA Redesigné

## 📌 Introduction

Bienvenue sur votre site UNA redesigné! Ce guide vous explique les nouvelles fonctionnalités et comment les utiliser.

---

## 🏠 Page d'Accueil (index.html)

### 🎨 Slider Interactif

La page d'accueil contient un **slider 3 images** qui se change automatiquement:

#### Fonctionnalités:
- **Auto-rotation**: Change toutes les 5 secondes
- **Arrows**: Cliquez sur les flèches pour naviguer manuellement
  - ◀ Slide précédent
  - ▶ Slide suivant
- **Dots**: 3 points en bas du slider (indicateurs)
  - Cliquez sur un point pour aller directement à ce slide
- **Animations**: Les titres et textes s'animent en slide-in

#### Contrôles:
```
Slider: ┌─────────────────────────────┐
        │ ◀ [IMAGE + TITRE] ▶         │
        │ • ◦ ◦  (Dots)               │
        └─────────────────────────────┘
```

#### Essayez:
1. Attendez 5 secondes → Slide change automatiquement
2. Cliquez sur ▶ → Slide suivant immédiatement
3. Cliquez sur le dot du milieu → Va au slide 2
4. Cliquez sur ◀ → Revient au slide précédent

---

## 🧭 Navigation Globale

### Desktop (≥992px)
```
┌────────────────────────────────────────────┐
│ UNA Logo | Accueil | À propos | Actualités│ UNA+ │
│          | Clubs | Événements | CROUA2    │      │
│          | Contact                         │      │
└────────────────────────────────────────────┘
```

**Menu horizontal** - Tous les liens visibles

### Mobile (<992px)
```
┌──────────────────────┐
│ UNA Logo      ☰      │  ← Burger menu
└──────────────────────┘

Menu déroulant:
├─ Accueil
├─ À propos
├─ Actualités
├─ Clubs
├─ Événements
├─ CROUA2
├─ Contact
└─ UNA+ (button)
```

**Burger menu** - Apparaît au click
- Cliquez sur ☰ pour ouvrir/fermer le menu
- Cliquez sur un lien pour aller à la page et fermer le menu

#### Navigation Links:
| Lien | Page | URL |
|------|------|-----|
| Accueil | Accueil | / |
| À propos | About | /about |
| Actualités | Courses | /courses |
| Clubs | Trainers | /trainers |
| Événements | Events | /events |
| CROUA2 | Pricing | /pricing |
| Contact | Contact | /contact |

---

## 📄 Pages Internes

### Avec Banner et Breadcrumb

Chaque page interne a:

1. **Navbar** (en haut)
2. **Banner** (avec fond + overlay bleu + texte blanc)
3. **Breadcrumb** (navigation en bas du banner)
4. **Contenu** (sections spécifiques à la page)
5. **Footer** (en bas)

### Exemple: Page "À Propos"
```
┌─────────────────────────────────────────────┐
│ NAVBAR (UNA Logo + Navigation)              │ ← Sticky (reste en haut)
├─────────────────────────────────────────────┤
│                                             │
│ BANNER: "À Propos de l'UNA"                │ ← Fond + Overlay bleu
│ Sous-titre: "Découvrez notre histoire..."  │
│ Accueil / À Propos                          │ ← Breadcrumb
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│ CONTENU:                                    │
│ - Section About                             │
│ - Statistiques (Counts)                     │
│ - Témoignages (Carousel)                    │
│                                             │
├─────────────────────────────────────────────┤
│ FOOTER                                      │
└─────────────────────────────────────────────┘
```

---

## 🎯 Lien Actif

À chaque page, le **lien de navigation correspondant** est marqué comme **actif** (souligné ou en couleur).

#### Exemples:
- Vous êtes sur la page "À Propos" → "À propos" link souligné
- Vous êtes sur la page "Actualités" → "Actualités" link souligné
- Vous êtes sur la page "Contact" → "Contact" link souligné

---

## 📱 Responsive Design

### Breakpoints

Le site s'adapte à **4 tailles d'écran**:

| Appareil | Largeur | Navbar | Banner | Texte |
|----------|---------|--------|--------|-------|
| Mobile | <480px | Burger | 220px | Petit |
| Tablet | 480-768px | Burger | 280px | Moyen |
| Desktop | 768-1200px | Horizontal | 350px | Large |
| Grand écran | >1200px | Horizontal | 350px | Large |

#### Responsive en pratique:
```
DESKTOP (1920px):
┌──────────────────────────────┐
│ Logo | Nav | Button           │
├──────────────────────────────┤
│ BANNER (350px, 48px titre)   │
├──────────────────────────────┤
│ Contenu (2-3 colonnes)       │
└──────────────────────────────┘

MOBILE (375px):
┌──────────────────┐
│ Logo | Burger    │
├──────────────────┤
│ BANNER (220px,   │
│  22px titre)     │
├──────────────────┤
│ Contenu (1 colonne)
└──────────────────┘
```

---

## 🎨 Design Elements

### Colors
- **Primary**: #004687 (Bleu UNA)
- **Secondary**: #0066cc (Bleu gradient)
- **Accent**: #ff6b35 (Orange pour CTA)
- **Text**: #333 (Gris foncé)
- **Background**: #f5f5f5 (Gris clair)

### Fonts
- **Headings**: Poppins (700 weight)
- **Body**: Open Sans (400 weight)
- **Monospace**: Raleway (600 weight)

### Buttons
- **CTA (UNA+)**: Gradient orange → couleur interactive
- **Hover**: Sous-lignes animées sur les links

### Icons
- Utilise **Bootstrap Icons** (bi classe)
- Exemples:
  - `bi-list` → Menu burger
  - `bi-chevron` → Arrows
  - `bi-person-circle` → User

---

## ⚡ Animations

### Navbar
- Underline animation on hover (gradient 0→100%)
- Mobile menu slide-in from left (0.3s)

### Slider (Accueil)
- Fade transition entre slides (0.7s)
- Slide-in-down pour titles (0.8s)
- Slide-in-up pour texte (0.8s)

### Banners
- Overlay blend avec fond
- Text shadow pour lisibilité

### Scroll Animations
- AOS (Animations on Scroll) sur tout le contenu
- Fade-up, zoom-in, etc.

---

## 🔍 SEO et Metadata

Chaque page a:
- **Title**: Unique pour chaque page
- **Meta Description**: Description courte
- **Meta Keywords**: Mots-clés pertinents
- **Canonical Links**: Évite duplication

---

## 🖥️ Pages Disponibles

### 1. **Accueil** (/)
- Slider 3 images
- Auto-rotation 5 secondes
- Navigation arrows et dots

### 2. **À Propos** (/about)
- Banner: "À Propos de l'UNA"
- Contenu: Histoire, valeurs, testimonials

### 3. **Actualités** (/courses)
- Banner: "Actualités"
- Grille de actualités/courses

### 4. **Clubs & Associations** (/trainers, /club)
- Banner: "Clubs & Associations"
- Liste de clubs avec descriptions

### 5. **Événements** (/events)
- Banner: "Événements & Activités"
- Calendar d'événements

### 6. **CROUA2** (/pricing, /crouA2)
- Banner: "CROUA2"
- Tableau tarifaire services

### 7. **Contact** (/contact)
- Banner: "Nous Contacter"
- Formulaire de contact

### 8. **Détails Actualité** (/course-details)
- Banner: "Détails Actualité"
- Article complet

---

## 🚀 Tips & Tricks

### Pour Mobile:
1. Utiliser le **burger menu** pour naviguer
2. **Toucher** les images pour les agrandir (lightbox)
3. **Scroller** pour voir les animations

### Pour Desktop:
1. **Hover** sur les links pour voir les underlines animées
2. **Click** les arrows du slider pour naviguer
3. Utiliser **Ctrl+Plus** pour zoomer si texte trop petit

### Accessibilité:
1. Utiliser **Tab** pour naviguer entre les links
2. **Appuyer sur Enter** pour activer les buttons
3. **Alt+F4** pour fermer le menu burger (si bloqué)

---

## 🐛 Dépannage

### Slider ne tourne pas
- Vérifier que JavaScript est activé
- Rafraîchir la page (F5)
- Essayer dans un autre navigateur

### Images manquantes
- Vérifier que `/stactic/mentor/assets/img/` existe
- Vérifier que les fichiers images existent
- Vérifier les chemins d'accès dans les templates

### Menu burger ne marche pas
- Vérifier que JavaScript est activé
- Ouvrir console (F12) pour voir les erreurs
- Vérifier que `navbar-slider-custom.css` est chargé

### Texte du banner illisible
- Vérifier le contraste (texte blanc sur overlay bleu)
- Augmenter le navigateur (Ctrl+Plus)
- Utiliser le mode dark reader si disponible

---

## 📞 Support

### Pour des problèmes:
1. Vérifier cette documentation
2. Vérifier la console navigateur (F12)
3. Vérifier les fichiers logs Django
4. Contacter l'administrateur

---

## 📚 Ressources

- **Django**: https://docs.djangoproject.com/
- **Bootstrap**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/
- **AOS**: https://michalsnik.github.io/aos/
- **Swiper**: https://swiperjs.com/

---

## ✅ Checklist avant le lancement

- [ ] Tester sur Chrome, Firefox, Safari, Edge
- [ ] Tester sur mobile (iPhone, Android)
- [ ] Tester tablet (iPad, Android tablets)
- [ ] Vérifier tous les links fonctionnent
- [ ] Vérifier que les images se chargent
- [ ] Tester le burger menu
- [ ] Tester le slider (accueil)
- [ ] Vérifier le responsive
- [ ] Lancer `python manage.py collectstatic`
- [ ] Tester en production

---

**Bonne utilisation du site! 🎉**

**Version**: 1.0  
**Date**: 02 Février 2026  
**Auteur**: GitHub Copilot Assistant
