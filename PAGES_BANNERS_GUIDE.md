# 🎨 Templates avec Banners - Pages Mises à Jour

## ✅ Pages Modifiées

### 1. **index.html** ✅
- Nouvelle navbar moderne + sticky
- Slider 3 slides avec auto-rotation
- Rest du contenu intact

### 2. **about.html** ✅
- Nouvelle navbar moderne + sticky
- Banner: "À Propos de l'UNA"
- Sous-titre: "Découvrez notre histoire et nos valeurs"
- Breadcrumb navigation
- Rest du contenu intact

### 3. **contact.html** ✅
- Nouvelle navbar moderne + sticky
- Banner: "Nous Contacter"
- Sous-titre: "Posez-nous vos questions et suggestions"
- Breadcrumb navigation
- Rest du contenu intact

---

## 📄 Pages à Mettre à Jour (Template Disponible)

Pour chaque page, il y a un pattern similaire:

```html
<!-- Banner avec titre personnalisé -->
<section class="page-banner" style="background-image: url('{% static 'mentor/assets/img/hero-bg .jpg' %}');">
  <div style="...">
    <h1>{{ TITRE_PAGE }}</h1>
    <p>{{ SOUS_TITRE_PAGE }}</p>
  </div>
  <!-- Breadcrumb -->
  <nav style="...">
    <ol>
      <li><a href="{% url 'vie_estudiantine_una:accueil' %}">Accueil</a></li>
      <li>/</li>
      <li>{{ NOM_PAGE }}</li>
    </ol>
  </nav>
</section>
```

---

## 🚀 Pages à Mettre à Jour Rapidement

### Pour: **courses.html** (Actualités)
**Banner:**
- Titre: "Actualités"
- Sous-titre: "Les dernières nouvelles de votre communauté"
- Page Name: "Actualités"

### Pour: **events.html** (Événements)
**Banner:**
- Titre: "Événements & Activités"
- Sous-titre: "Découvrez tous nos événements"
- Page Name: "Événements"

### Pour: **trainers.html** (Clubs)
**Banner:**
- Titre: "Clubs & Associations"
- Sous-titre: "Rejoignez nos clubs et associations"
- Page Name: "Clubs"

### Pour: **pricing.html** (CROUA2)
**Banner:**
- Titre: "CROUA2"
- Sous-titre: "Restauration, Logement et Services"
- Page Name: "CROUA2"

### Pour: **course-details.html** (Détail Actualité)
**Banner:**
- Titre: "Détails Actualité"
- Sous-titre: "Article complet"
- Page Name: "Détail Article"

### Pour: **starter-page.html** (Page Test)
**Banner:**
- Titre: "Page Personnalisée"
- Sous-titre: "Contenu de test"
- Page Name: "Starter"

---

## 📝 Instructions Rapides

Pour mettre à jour une page manuellement:

### Étape 1: Ouvrir le fichier

Exemple: `templates/mentor/courses.html`

### Étape 2: Remplacer le Header

Remplacer:
```html
<header id="header" class="header d-flex align-items-center sticky-top">
  <!-- ancien code -->
</header>
```

Par:
```html
<header class="navbar-header">
  <div class="container-fluid container-xl">
    <div class="navbar-content">
      <!-- Logo -->
      <a href="{% url 'vie_estudiantine_una:accueil' %}" class="logo-section">
        <img src="{% static 'mentor/assets/img/logo.webp' %}" alt="UNA Logo">
        <div class="logo-text">
          <h1>UNA</h1>
          <p>Vie Estudiantine</p>
        </div>
      </a>

      <!-- Navigation Menu -->
      <nav class="nav-menu">
        <ul class="nav-links">
          <li><a href="{% url 'vie_estudiantine_una:accueil' %}">Accueil</a></li>
          <li><a href="{% url 'vie_estudiantine_una:about' %}">À propos</a></li>
          <li><a href="{% url 'vie_estudiantine_una:courses' %}" class="active">Actualités</a></li>
          <li><a href="{% url 'vie_estudiantine_una:trainers' %}">Clubs</a></li>
          <li><a href="{% url 'vie_estudiantine_una:events' %}">Événements</a></li>
          <li><a href="{% url 'vie_estudiantine_una:pricing' %}">CROUA2</a></li>
          <li><a href="{% url 'vie_estudiantine_una:contact' %}">Contact</a></li>
        </ul>
      </nav>

      <!-- CTA Button -->
      <a href="{% url 'vie_estudiantine_una:courses' %}" class="btn-cta">UNA+</a>

      <!-- Mobile Menu Toggle -->
      <button class="mobile-toggle" id="mobile-toggle">
        <i class="bi bi-list"></i>
      </button>

    </div>

    <!-- Mobile Navigation -->
    <nav class="mobile-nav" id="mobile-nav">
      <ul>
        <li><a href="{% url 'vie_estudiantine_una:accueil' %}">Accueil</a></li>
        <li><a href="{% url 'vie_estudiantine_una:about' %}">À propos</a></li>
        <li><a href="{% url 'vie_estudiantine_una:courses' %}">Actualités</a></li>
        <li><a href="{% url 'vie_estudiantine_una:trainers' %}">Clubs</a></li>
        <li><a href="{% url 'vie_estudiantine_una:events' %}">Événements</a></li>
        <li><a href="{% url 'vie_estudiantine_una:pricing' %}">CROUA2</a></li>
        <li><a href="{% url 'vie_estudiantine_una:contact' %}">Contact</a></li>
        <li style="border: none; padding: 15px 0;"><a href="{% url 'vie_estudiantine_una:courses' %}" class="btn-cta" style="display: inline-block;">UNA+</a></li>
      </ul>
    </nav>

  </div>
</header>
```

### Étape 3: Ajouter le CSS dans le Head

```html
<link href="{% static 'mentor/assets/css/navbar-slider-custom.css' %}" rel="stylesheet">
```

### Étape 4: Ajouter le Banner Après le Header

```html
<!-- Banner Section -->
<section class="page-banner" style="background-image: url('{% static 'mentor/assets/img/hero-bg .jpg' %}'); background-size: cover; background-position: center; height: 350px; position: relative; display: flex; align-items: center; justify-content: center;">
  <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 70, 135, 0.5); z-index: 1;"></div>
  <div style="position: relative; z-index: 2; text-align: center; color: white; padding: 40px 20px;">
    <h1 style="font-size: 48px; font-weight: 700; margin-bottom: 15px; line-height: 1.2; text-shadow: 0 2px 8px rgba(0,0,0,0.3);">TITRE_PAGE</h1>
    <p style="font-size: 20px; margin: 0; opacity: 0.95; text-shadow: 0 1px 4px rgba(0,0,0,0.2);">SOUS_TITRE_PAGE</p>
  </div>
  <nav style="position: absolute; bottom: 20px; left: 0; right: 0; z-index: 3;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
      <ol style="list-style: none; padding: 0; margin: 0; display: flex; gap: 10px; color: white; font-size: 14px;">
        <li><a href="{% url 'vie_estudiantine_una:accueil' %}" style="color: white; text-decoration: none; transition: opacity 0.3s; cursor: pointer;">Accueil</a></li>
        <li style="opacity: 0.7;">/</li>
        <li>NOM_PAGE</li>
      </ol>
    </div>
  </nav>
</section>
```

### Étape 5: Ajouter le Script Mobile Menu à la Fin (Avant </body>)

```html
<!-- Mobile Menu Toggle Script -->
<script>
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  if (mobileToggle && mobileNav) {
    mobileToggle.addEventListener('click', () => {
      mobileNav.classList.toggle('active');
    });

    const mobileNavLinks = mobileNav.querySelectorAll('a');
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('active');
      });
    });
  }
</script>

<!-- Responsive Banner CSS -->
<style>
  @media (max-width: 1200px) {
    .page-banner h1 {
      font-size: 42px !important;
    }
    .page-banner p {
      font-size: 18px !important;
    }
  }

  @media (max-width: 768px) {
    .page-banner {
      height: 280px !important;
    }
    .page-banner h1 {
      font-size: 28px !important;
    }
    .page-banner p {
      font-size: 16px !important;
    }
  }

  @media (max-width: 480px) {
    .page-banner {
      height: 220px !important;
    }
    .page-banner h1 {
      font-size: 22px !important;
    }
    .page-banner p {
      font-size: 14px !important;
    }
  }
</style>
```

---

## 🎯 Checklist par Page

### courses.html (Actualités)
- [ ] Remplacer header
- [ ] Ajouter CSS navbar
- [ ] Ajouter banner avec "Actualités"
- [ ] Ajouter script mobile toggle
- [ ] Ajouter CSS responsive banner
- [ ] Tester navbar mobile (< 992px)
- [ ] Tester banner responsive
- [ ] Vérifier liens navigation

### events.html (Événements)
- [ ] Remplacer header
- [ ] Ajouter CSS navbar
- [ ] Ajouter banner avec "Événements & Activités"
- [ ] Ajouter script mobile toggle
- [ ] Ajouter CSS responsive banner
- [ ] Tester navbar mobile
- [ ] Tester banner responsive
- [ ] Vérifier liens navigation

### trainers.html (Clubs)
- [ ] Remplacer header
- [ ] Ajouter CSS navbar
- [ ] Ajouter banner avec "Clubs & Associations"
- [ ] Ajouter script mobile toggle
- [ ] Ajouter CSS responsive banner
- [ ] Tester navbar mobile
- [ ] Tester banner responsive
- [ ] Vérifier liens navigation

### pricing.html (CROUA2)
- [ ] Remplacer header
- [ ] Ajouter CSS navbar
- [ ] Ajouter banner avec "CROUA2"
- [ ] Ajouter script mobile toggle
- [ ] Ajouter CSS responsive banner
- [ ] Tester navbar mobile
- [ ] Tester banner responsive
- [ ] Vérifier liens navigation

---

## 📊 Structure des Banners

```
┌─────────────────────────────────────────────┐
│                                             │
│  IMAGE FOND + OVERLAY BLEU (opacity 0.5)  │
│                                             │
│           Titre (48px, blanc)              │
│         Sous-titre (20px, blanc)           │
│                                             │
│  Accueil / Nom Page                        │
│  (breadcrumb en bas)                       │
│                                             │
└─────────────────────────────────────────────┘
```

### Hauteurs Responsive:
- Desktop (> 1200px): 350px
- Tablet (768-1199px): 280px
- Mobile (< 768px): 220px

### Couleurs:
- Overlay: rgba(0, 70, 135, 0.5) (Bleu UNA semi-transparent)
- Texte: blanc (#fff)
- Shadow: 0 2px 8px rgba(0,0,0,0.3)

---

## 🔄 Lien Actif dans Navigation

Assurez-vous que le lien actif a la classe `active`:

```html
<!-- Pour la page Actualités -->
<li><a href="{% url 'vie_estudiantine_una:courses' %}" class="active">Actualités</a></li>

<!-- Pour la page Événements -->
<li><a href="{% url 'vie_estudiantine_una:events' %}" class="active">Événements</a></li>

<!-- etc -->
```

---

## 🌍 Fichiers Modifiés Jusqu'à Présent

- ✅ index.html - Slider + Navbar
- ✅ about.html - Banner "À Propos"
- ✅ contact.html - Banner "Contact"
- ⏳ courses.html - À faire (Actualités)
- ⏳ events.html - À faire (Événements)
- ⏳ trainers.html - À faire (Clubs)
- ⏳ pricing.html - À faire (CROUA2)
- ⏳ course-details.html - À faire
- ⏳ starter-page.html - À faire

---

## 💡 Conseil

Pour aller plus vite, utilisez un éditeur de texte avec:
- Find & Replace (Ctrl+H)
- Multi-selection (Ctrl+D)

Ou utilisez un script Python pour automatiser les modifications si besoin.

---

**Version**: 1.0  
**Date**: 2 février 2026  
**Status**: À finaliser (4/7 pages terminées)
