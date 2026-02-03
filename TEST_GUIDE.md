# 🧪 Guide de Test - Navbar et Slider

**Version**: 1.0  
**Date**: 2 février 2026

---

## ✅ Liste de Contrôle Complète

### 1️⃣ Tests de Base

#### Navbar - Desktop (1200px+)
- [ ] Logo visible avec image et texte
- [ ] Tous les liens de navigation visibles
- [ ] Bouton UNA+ visible
- [ ] Menu burger caché
- [ ] Navbar sticky (reste visible lors du scroll)

#### Navbar - Tablet (768px - 991px)
- [ ] Logo toujours visible
- [ ] Liens masqués
- [ ] Menu burger visible
- [ ] Clicking burger affiche le menu
- [ ] Menu disparaît quand on clique sur un lien

#### Navbar - Mobile (< 768px)
- [ ] Logo adapté à la taille
- [ ] Burger menu visible et fonctionnel
- [ ] Menu ouvre/ferme en swipe
- [ ] Texte lisible
- [ ] Pas de défilement horizontal

---

### 2️⃣ Tests du Slider

#### Affichage Initial
- [ ] 3 slides chargées
- [ ] Première slide visible
- [ ] Image de fond affichée correctement
- [ ] Texte du slide visible et lisible
- [ ] Bouton "En savoir plus" visible

#### Navigation par Flèches
- [ ] Cliquer flèche droite → slide suivant
- [ ] Cliquer flèche gauche → slide précédent
- [ ] Transition fluide entre les slides (0.7s)
- [ ] Pas de saut ou de scintillement

#### Navigation par Points
- [ ] 3 points visibles au bas
- [ ] Premier point actif (blanc)
- [ ] Cliquer un point → aller au slide
- [ ] Points se mettent à jour lors de la transition

#### Auto-rotation
- [ ] Slider avance automatiquement
- [ ] Intervalle ~ 5 secondes
- [ ] Boucle à la fin (retour au début)
- [ ] Bouton arrête l'auto-rotation quand on clique

#### Pause au Hover
- [ ] Hover sur slider → auto-rotation en pause
- [ ] Sortir du hover → auto-rotation reprend
- [ ] Fonctionne uniquement sur desktop

#### Animations
- [ ] Titre "slide-in-down" au chargement du slide
- [ ] Sous-titre "slide-in-up" au chargement
- [ ] Bouton "slide-in-up" au chargement
- [ ] Animations fluides, sans saccades

#### Boutons des Slides
- [ ] Couleur orange (#ff6b35)
- [ ] Hover → couleur plus foncée
- [ ] Clic → navigation vers la page (À propos, Actualités, Événements)
- [ ] Animation hover fluide

---

### 3️⃣ Tests Responsifs

#### Hauteur Slider
- [ ] Desktop (> 1200px): 550px
- [ ] Desktop (768px - 1200px): 450px
- [ ] Mobile (< 768px): 320px
- [ ] Mobile petit (< 480px): 250px

#### Images de Fond
- [ ] Entièrement visibles et proportionnées
- [ ] Pas de déformation
- [ ] Couverture complète (background-cover)
- [ ] Centré (background-position: center)

#### Textes
- [ ] Lisibles à tous les appareils
- [ ] Pas de dépassement du conteneur
- [ ] Taille adaptée au responsive
- [ ] Ombre pour contraste suffisant

---

### 4️⃣ Tests de Performance

#### Temps de Chargement
- [ ] Page charge en < 3 secondes
- [ ] Images optimisées (webp si possible)
- [ ] CSS et JS minifiés

#### Fluidité
- [ ] Transitions fluides 60fps
- [ ] Pas de lag lors du scroll
- [ ] Pas de freeze lors des animations

#### Clic & Interaction
- [ ] Réponse immédiate aux clics
- [ ] Pas de délai dans les transitions
- [ ] Smooth scroll sur les liens

---

### 5️⃣ Tests de Compatibilité

#### Navigateurs Desktop
- [ ] Chrome 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+

#### Navigateurs Mobile
- [ ] Safari iOS (iPhone)
- [ ] Chrome Android
- [ ] Firefox Android
- [ ] Samsung Internet

#### Résolutions Testées
- [ ] 320px (iPhone 5S)
- [ ] 375px (iPhone 6/7/8)
- [ ] 414px (iPhone XR)
- [ ] 768px (iPad)
- [ ] 1024px (iPad Pro)
- [ ] 1366px (Laptop)
- [ ] 1920px (Desktop)

---

### 6️⃣ Tests Fonctionnels

#### Liens Navigation
- [ ] Accueil → `/`
- [ ] À propos → `/about/`
- [ ] Actualités → `/actualites/`
- [ ] Clubs → `/club/`
- [ ] Événements → `/events/`
- [ ] CROUA2 → `/crouA2/`
- [ ] Contact → `/contact/`

#### Boutons Slider
- [ ] Slide 1 "En savoir plus" → Actualités
- [ ] Slide 2 "En savoir plus" → À propos
- [ ] Slide 3 "En savoir plus" → Événements

#### Bouton UNA+
- [ ] Navbar → Actualités
- [ ] Mobile menu → Actualités
- [ ] Couleur gradient correcte

---

### 7️⃣ Tests d'Accessibilité

#### Keyboard Navigation
- [ ] Tab navigue tous les éléments interactifs
- [ ] Shift+Tab navigue en arrière
- [ ] Enter active les boutons/liens
- [ ] Escape ferme le menu mobile

#### Lecteur d'Écran
- [ ] Tous les éléments ont des labels/alt
- [ ] Les icônes ont des descriptions
- [ ] Structure HTML sémantique
- [ ] Contraste suffisant (WCAG AA)

#### Vision
- [ ] Texte lisible (taille minimale 14px)
- [ ] Contraste suffisant (4.5:1)
- [ ] Couleurs ne sont pas le seul indicateur
- [ ] Pas de clignotement > 3Hz

---

### 8️⃣ Tests du Menu Mobile

#### Ouverture/Fermeture
- [ ] Burger menu visible sur mobile
- [ ] Clic burger → menu s'ouvre
- [ ] Clic burger à nouveau → menu se ferme
- [ ] Clic lien → menu se ferme
- [ ] Clic hors menu → menu reste ouvert

#### Contenu Mobile Menu
- [ ] Tous les liens présents
- [ ] Bouton UNA+ présent
- [ ] Spacing correct entre éléments
- [ ] Pas de contenu qui dépasse

#### Animation Menu
- [ ] Slide depuis la gauche (smooth)
- [ ] Overlay derrière le menu
- [ ] Pas de saut ou scintillement
- [ ] Duré ~0.3s

---

### 9️⃣ Tests SEO/Meta

#### Head Tag
- [ ] Title: "UNA - Vie Estudiantine"
- [ ] Meta description présente
- [ ] Meta viewport présente
- [ ] Favicon présente
- [ ] Lang="fr" sur html

#### Open Graph (Optional)
- [ ] og:title présent
- [ ] og:description présent
- [ ] og:image présent
- [ ] og:url présent

---

### 🔟 Tests de Stabilité

#### Interactions Répétées
- [ ] Cliquer burger 10x → toujours fonctionne
- [ ] Naviguer slides 10x → toujours fonctionne
- [ ] Scroll up/down → navbar reste stable
- [ ] Resize fenêtre → layout s'adapte

#### Edge Cases
- [ ] Très petit écran (320px) → responsive
- [ ] Très grand écran (2560px) → responsive
- [ ] Navire en arrière/avant → contenu conservé
- [ ] Cache vidée → page charge normalement

---

## 📋 Checklist Avant Déploiement

### Code Quality
- [ ] Pas d'erreurs console (F12 → Console)
- [ ] Pas d'avertissements CSS
- [ ] Code formaté et indenté
- [ ] Commentaires présents

### Performance
- [ ] Lighthouse score > 90
- [ ] Temps de chargement < 3s
- [ ] Aucun layout shift
- [ ] Images optimisées

### Testing
- [ ] Testé sur 5+ appareils/résolutions
- [ ] Testé sur 4+ navigateurs
- [ ] Menu mobile fonctionne
- [ ] Slider fonctionne
- [ ] Tous les liens fonctionnent

### Documentation
- [ ] README créé
- [ ] Guide de mise à jour créé
- [ ] Documentation technique créée
- [ ] Commentaires dans le code

---

## 🐛 Debugging Guide

### Le menu burger ne fonctionne pas
```javascript
// Vérifiez dans la console:
document.getElementById('mobile-toggle')  // Doit exister
document.getElementById('mobile-nav')     // Doit exister

// Vérifiez que Bootstrap CSS est chargé
// Vérifiez que le script du toggle est présent
```

### Le slider ne bouge pas
```javascript
// Vérifiez dans la console:
document.querySelectorAll('.slide')      // Doit avoir 3 éléments
document.querySelectorAll('.dot')        // Doit avoir 3 éléments
document.getElementById('next-slide')    // Doit exister
```

### La navbar n'est pas sticky
```css
/* Vérifiez que ces styles sont présents */
.navbar-header {
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* Vérifiez que le parent n'a pas overflow: hidden */
```

### Les images de fond ne s'affichent pas
```html
<!-- Vérifiez que {% static %} est correct -->
{% static 'mentor/assets/img/hero-bg.jpg' %}

<!-- Vérifiez que le fichier existe -->
```

---

## 📸 Captures d'Écran Attendues

### Desktop
- Navbar horizontale + slider plein écran
- Flèches et dots bien positionnés
- Texte centré et lisible

### Tablet
- Navbar compacte + burger visible
- Slider adapté à la hauteur
- Menu fonctionne bien

### Mobile
- Burger menu visible + fonctionne
- Slider prend la largeur complète
- Texte du slider lisible
- Pas de défilement horizontal

---

## 🎯 Résultats Attendus

| Élément | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Navbar | Horizontal | Burger | Burger |
| Logo | 50px | 50px | 40px |
| Slider Hauteur | 550px | 450px | 320px |
| Points | 3 | 3 | 3 |
| Flèches | Visibles | Visibles | Visibles |
| Auto-rotate | ✓ | ✓ | ✓ |
| Responsive | ✓ | ✓ | ✓ |

---

## 📊 Notes de Test

```
Test Date: ________________
Tested By: ________________
Device/Browser: ________________
Result: ✓ PASS / ✗ FAIL

Issues Found:
1. _______________________
2. _______________________
3. _______________________

Fix Applied:
1. _______________________
2. _______________________
3. _______________________

Re-tested: ✓ PASS / ✗ FAIL
```

---

## 🚀 Après Avoir Testé

1. **Tout fonctionne?**
   - ✅ OUI → Prêt pour le déploiement
   - ❌ NON → Voir la section Debugging

2. **Signaler les bugs**
   - Incluez les détails du navigateur/appareil
   - Incluez les étapes pour reproduire le bug
   - Incluez des captures d'écran si possible

3. **Déployer**
   - Faire une sauvegarde
   - Tester en staging d'abord
   - Puis deployer en production

---

**Test Plan Version**: 1.0  
**Compatible avec**: Bootstrap 5.3.7+, Django 6.0+  
**Last Updated**: 2 février 2026
