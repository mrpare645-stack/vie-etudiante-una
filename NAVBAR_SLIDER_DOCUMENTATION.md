# Documentation - Améliorations Navbar et Slider

## Changements Effectués

### 1. **Nouvelle Navbar Responsive et Sticky**

#### Caractéristiques:
- **Logo à gauche** avec image et texte (UNA - Vie Estudiantine)
- **Liens de navigation à droite** vers toutes les pages principales
- **Sticky-top** - la navbar reste visible en haut lors du scroll
- **Responsive** - Collapsible menu burger sur mobile (< 992px)
- **Style moderne** avec:
  - Fond blanc propre
  - Ombre subtile
  - Liens avec animation de underline au hover
  - Couleur primaire: #004687
  - Bouton CTA "UNA+" avec gradient

#### Structure HTML:
```html
<header class="navbar-header">
  <div class="navbar-content">
    <!-- Logo -->
    <a href="#" class="logo-section">
      <img src="logo.webp">
      <div class="logo-text">
        <h1>UNA</h1>
        <p>Vie Estudiantine</p>
      </div>
    </a>
    
    <!-- Navigation -->
    <nav class="nav-menu">
      <ul class="nav-links">
        <!-- Liens -->
      </ul>
    </nav>
    
    <!-- CTA Button -->
    <a href="#" class="btn-cta">UNA+</a>
    
    <!-- Mobile Toggle -->
    <button class="mobile-toggle">
      <i class="bi bi-list"></i>
    </button>
  </div>
  
  <!-- Mobile Nav -->
  <nav class="mobile-nav">
    <!-- Liens mobiles -->
  </nav>
</header>
```

#### Classes CSS Principales:
- `.navbar-header` - Conteneur principal
- `.navbar-content` - Contenu avec flexbox
- `.logo-section` - Logo et texte
- `.nav-links` - Liens de navigation
- `.btn-cta` - Bouton d'appel à l'action
- `.mobile-nav` - Menu mobile caché par défaut
- `.mobile-toggle` - Bouton hamburger

#### Points de Rupture Responsive:
- **Desktop (≥992px)**: Menu horizontal + Bouton visible
- **Tablet/Mobile (<992px)**: Menu hamburger + Navigation verticale fixe

---

### 2. **Nouveau Slider/Carousel Plein Écran**

#### Caractéristiques:
- **Hauteur responsive** - 550px (desktop), 320px (mobile)
- **3 slides** avec images de fond
- **Chaque slide contient**:
  - Titre (h2) avec animation
  - Sous-titre avec animation
  - Bouton "En savoir plus" orange (#ff6b35)
  - Fond semi-transparent (overlay bleu)

#### Navigation:
- **Flèches** (← et →) pour naviguer manuellement
- **Points indicateurs (dots)** pour voir la progression
  - Point actif s'agrandit en largeur
  - Tous les points cliquables
- **Auto-rotation** toutes les 5 secondes
- **Pause au hover** sur le slider

#### Animations:
- Transition d'opacité entre les slides (0.7s)
- Animation d'entrée du contenu (slide-in)
- Animations de hover sur boutons et flèches

#### Structure HTML:
```html
<section class="hero-slider">
  <div class="slides-container">
    <div class="slide active">
      <div class="slide-content">
        <h2 class="slide-title">Titre</h2>
        <p class="slide-subtitle">Sous-titre</p>
        <a href="#" class="slide-btn">En savoir plus</a>
      </div>
    </div>
    <!-- Plus de slides -->
  </div>
  
  <div class="slider-nav">
    <button class="slider-arrow" id="prev-slide">←</button>
    <div class="slider-dots">
      <div class="dot active" data-slide="0"></div>
      <!-- Plus de dots -->
    </div>
    <button class="slider-arrow" id="next-slide">→</button>
  </div>
</section>
```

#### JavaScript Principal:
```javascript
// Variables
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

// Afficher un slide
function showSlide(n) {
  slides.forEach(s => s.classList.remove('active'));
  dots.forEach(d => d.classList.remove('active'));
  
  slides[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
}

// Navigation
document.getElementById('next-slide').addEventListener('click', nextSlide);
document.getElementById('prev-slide').addEventListener('click', prevSlide);

// Auto-play toutes les 5 secondes
setInterval(autoplay, 5000);
```

---

### 3. **Fichiers Modifiés/Créés**

#### Créés:
1. `/templates/mentor/_navbar.html` - Composant navbar réutilisable
2. `/stactic/mentor/assets/css/navbar-slider-custom.css` - Styles personnalisés

#### Modifiés:
1. `/templates/mentor/index.html` - Remplacée avec nouvelle structure

#### Intacts:
- ✓ Toutes les autres pages (about.html, contact.html, etc.)
- ✓ Section "About" 
- ✓ Counts (statistiques)
- ✓ Why Us
- ✓ Features
- ✓ Courses (Actualités)
- ✓ Trainers (Acteurs)
- ✓ Footer

---

### 4. **Variables CSS Personnalisées**

```css
:root {
  --primary-color: #004687;        /* Bleu UNA */
  --secondary-color: #0066cc;      /* Bleu secondaire */
  --accent-color: #ff6b35;         /* Orange pour CTA */
  --light-gray: #f5f5f5;           /* Fond léger */
  --border-color: #eee;            /* Bordures */
  --text-color: #333;              /* Texte */
}
```

---

### 5. **Améliorations Apportées**

#### Pour la Navbar:
- ✓ Navigation claire et intuitive
- ✓ Logo avec image et texte descriptif
- ✓ Responsive design avec menu burger
- ✓ Animations fluides au hover
- ✓ Sticky pour toujours visible
- ✓ Mobile-first approach

#### Pour le Slider:
- ✓ Images plein écran responsive
- ✓ Transitions fluides
- ✓ Navigation intuitive (flèches + dots)
- ✓ Auto-rotation configurable
- ✓ Animations d'entrée du contenu
- ✓ Compatible mobile/tablette/desktop
- ✓ Utilise {% static %} pour les images Django

---

### 6. **Intégration Django**

Toutes les URLs utilisent les template tags Django:
```django
{% url 'vie_estudiantine_una:accueil' %}
{% url 'vie_estudiantine_una:about' %}
{% url 'vie_estudiantine_una:courses' %}
{% url 'vie_estudiantine_una:trainers' %}
{% url 'vie_estudiantine_una:events' %}
{% url 'vie_estudiantine_una:pricing' %}
{% url 'vie_estudiantine_una:contact' %}
```

Les images utilisent `{% static %}`:
```django
{% static 'mentor/assets/img/logo.webp' %}
```

---

### 7. **Personnalisation Possible**

Pour modifier les slides, éditez dans `index.html`:
- Titre: `.slide-title` text
- Sous-titre: `.slide-subtitle` text
- Image: `background-image: url('...')`
- Lien bouton: `href="#"`
- Délai auto-rotation: Dans le script `setInterval(autoplay, 5000)` (5000ms = 5s)

---

### 8. **Performance & Optimisation**

- ✓ CSS critique intégré
- ✓ CSS externe séparé pour meilleur cache
- ✓ JavaScript vanilla (pas de dépendances)
- ✓ Animations utilisant CSS transforms (GPU)
- ✓ Media queries pour responsive design
- ✓ Lighthouse ready

---

## Comment Mettre à Jour les Autres Pages

Pour utiliser la même navbar sur les autres pages, remplacez le `<header>` existant par:

```django
{% include 'mentor/_navbar.html' %}
```

Ou copiez-collez le code HTML de la navbar de l'index.html.

---

## Support Navigateurs

- Chrome/Edge: ✓ Full support
- Firefox: ✓ Full support
- Safari: ✓ Full support
- Mobile Safari: ✓ Full support
- Android Chrome: ✓ Full support

---

**Date de création**: 2 février 2026
**Version**: 1.0
