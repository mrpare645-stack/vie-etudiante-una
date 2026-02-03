from django.db import models
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom

class Actualite(models.Model):
    CATEGORIES = [
        ('UNA', 'Vie universitaire'),
        ('EVENT', 'Événement'),
        ('CROU', 'CROU'),
        ('CLUB', 'Club & Association'),
    ]

    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    resume = models.TextField()
    image = models.ImageField(upload_to='actualites/')
    date_pub = models.DateTimeField(auto_now_add=True)
    nom_auteur = models.CharField(max_length=100, default="Administration UNA")
    image_auteur = models.ImageField(upload_to='auteurs/', blank=True)

    vues = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titre

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='evenements/', blank=True, null=True)
    description = models.TextField()
    details = models.TextField(blank=True)

    def __str__(self):
        return self.titre
    
    
class ServiceCROU(models.Model):
    CATEGORIE_SERVICE = [
        ('logement', 'Logement'),
        ('restauration', 'Restauration'),
        ('sante', 'Santé'),
    ]
    
    nom = models.CharField(max_length=150)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_SERVICE)
    description = models.TextField()
    localisation = models.CharField(max_length=200)
    horaires = models.TextField(blank=True)
    contact = models.CharField(max_length=200)
    lien_externe = models.URLField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    
    class Meta:
        verbose_name = "Service CROU"
        verbose_name_plural = "Services CROU"
    
    def __str__(self):
        return self.nom

class OffreLogement(models.Model):
    TYPE_LOGEMENT = [
        ('chambre', 'Chambre'),
        ('studio', 'Studio'),
        ('appartement', 'Appartement'),
    ]
    
    titre = models.CharField(max_length=150)
    type_logement = models.CharField(max_length=50, choices=TYPE_LOGEMENT)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    lieu = models.CharField(max_length=200)
    contact_crou = models.CharField(max_length=200)
    date_publication = models.DateField(auto_now_add=True)
    est_disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Offre de logement"
        verbose_name_plural = "Offres de logement"
    
    def __str__(self):
        return f"{self.titre} - {self.type_logement}"

class Temoignage(models.Model):
    etudiant_nom = models.CharField(max_length=100)
    filiere = models.CharField(max_length=100)
    promotion = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='temoignages/', blank=True)
    message = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    est_approuve = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-date_publication']
    
    def __str__(self):
        return f"Témoignage de {self.etudiant_nom}"

class Partenaire(models.Model):
    nom = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partenaires/')
    domaine = models.CharField(max_length=100)
    site_web = models.URLField()
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
    
    def __str__(self):
        return self.nom
    

class Filiere(models.Model):
    nom = models.CharField(max_length=150)
    icon = models.CharField(
        max_length=50,
        help_text="Classe Bootstrap Icons ex: bi-mortarboard"
    )

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"

    def __str__(self):
        return self.nom
    
class AboutUNA(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')
    point_1 = models.CharField(max_length=255)
    point_2 = models.CharField(max_length=255)
    point_3 = models.CharField(max_length=255)
    bouton_texte = models.CharField(max_length=100, default="En savoir plus")
    bouton_lien = models.URLField(default="https://www.univ-na.ci/")

    def __str__(self):
        return self.titre
    
class Slide(models.Model):
    titre = models.CharField(max_length=200, blank=True)
    sous_titre = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='slides/')
    bouton_texte = models.CharField(max_length=100, blank=True)
    bouton_lien = models.CharField(max_length=255, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Slide"
        verbose_name_plural = "Slides"

    def __str__(self):
        return self.titre or f"Slide #{self.pk}"
    
class Acteur(models.Model):
    nom = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='acteurs/')
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.nom
    
class Temoin(models.Model):
    nom = models.CharField(max_length=100)
    promotion = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='temoins/', blank=True)
    message = models.TextField()
   

   
    def __str__(self):
        return f"Témoin {self.nom}"
    
class Club_association(models.Model):
    domaine = models.CharField(max_length=100)
    nom_club = models.CharField(max_length=150)
    description = models.TextField()
    logo = models.ImageField(upload_to='clubs_associations/', blank=True)
    url = models.URLField(blank=True)
    
     
    class Meta:
        verbose_name = "Club/Association"
        verbose_name_plural = "Clubs/Associations"
    
    def __str__(self):
        return self.nom_club
# Create your models here.
