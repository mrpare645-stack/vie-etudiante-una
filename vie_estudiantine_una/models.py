from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .utils import STATUS_CHOICES  

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
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.titre
    
    
class ServiceCROU(models.Model):
    CATEGORIE_SERVICE = [
        ('logement', 'Logement'),
        ('restauration', 'Restauration'),
        ('sante', 'Santé'),
        ('Autre','autres')
    ]
    
    nom = models.CharField(max_length=150)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_SERVICE)
    description = models.TextField()
    localisation = models.CharField(max_length=200)
    horaires = models.TextField(blank=True)
    contact = models.CharField(max_length=200)
    proposer_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="services_proposes", verbose_name="Proposé par")
    lien_externe = models.URLField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    is_student = models.BooleanField(default=False, verbose_name="Service Étudiant")
    
    class Meta:
        verbose_name = "Service CROU"
        verbose_name_plural = "Services CROU"
    
    def __str__(self):
        return self.nom





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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Étudiant")
    nom = models.CharField(max_length=100)
    promotion = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='temoins/', blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    date_creation = models.DateTimeField(auto_now_add=True)
   

   
    def save(self, *args, **kwargs):
        self.is_approved = (self.status == 'APPROVED')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Témoin {self.nom}"
    
class Club_association(models.Model):
    proposer_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="clubs_proposes", verbose_name="Proposé par")
    domaine = models.CharField(max_length=100)
    nom_club = models.CharField(max_length=150)
    description = models.TextField()
    logo = models.ImageField(upload_to='clubs_associations/', blank=True)
    url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut Modération")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'APPROVED':
            self.is_approved = True
        else:
            self.is_approved = False
        super().save(*args, **kwargs)
     
    class Meta:
        verbose_name = "Club/Association"
        verbose_name_plural = "Clubs/Associations"
    
    def __str__(self):
        return self.nom_club
    


class PageChoice(models.TextChoices):
    ACCUEIL = 'accueil', 'Accueil'
    A_PROPOS = 'about', 'À propos'
    CONTACT = 'contact', 'Contact'
    ACTUALITES = 'actualites', 'Actualités'
    EVENTS = 'events', 'Événements'
    CROUA2 = 'crouA2', 'Services CROU'
    CLUB = 'club', 'Clubs et Associations'


class Banner(models.Model):
    page = models.CharField(max_length=50, choices=PageChoice.choices)
    titre = models.CharField(max_length=200)
    sous_titre = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/')
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_page_display()} - {self.titre}"

class Statistique(models.Model):
    nombre_etudiants = models.CharField(max_length=50, default="15000", help_text="Ex: 15000")
    nombre_enseignants = models.CharField(max_length=50, default="500", help_text="Ex: 500")
    
    class Meta:
        verbose_name = "Chiffres Clés (Statistiques)"
        verbose_name_plural = "Chiffres Clés (Statistiques)"

    def __str__(self):
        return "Configuration des Statistiques Site"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profils/', default='profils/default.jpg', blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.CharField(max_length=50, blank=True, help_text="Ex: Licence 3, Master 1")
    centres_interet = models.TextField(blank=True, help_text="Séparés par des virgules")
    bio = models.TextField(blank=True, max_length=500, help_text="Une courte biographie pour votre profil public.")
    clubs_suivis = models.ManyToManyField(Club_association, blank=True, related_name="followers")

    class Meta:
        verbose_name = "Profil Étudiant"
        verbose_name_plural = "Profils Étudiants"

    def __str__(self):
        return f"Profil de {self.user.username}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', '👍'),
        ('LOVE', '❤️'),
        ('FIRE', '🔥'),
        ('CLAP', '👏'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id') # Une seule réaction par objet par user

class Commentaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Com de {self.user} sur {self.content_object}"



class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = "Abonnement"

    def __str__(self):
        return f"{self.follower} suit {self.following}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name="Exprimez-vous...")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED', verbose_name="Statut")
    # Note: Les posts sont souvent auto-approuvés sauf détection de risque

    class Meta:
        ordering = ['-created_at']

    @property
    def is_visible(self):
        return self.status == 'APPROVED'

    def __str__(self):
        return f"Post de {self.author} ({self.created_at.strftime('%d/%m/%Y')})"

    @property
    def likes_count(self):
        return self.post_likes.count()

    @property
    def comments_count(self):
        return self.post_comments.count()

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        
    @property
    def is_visible(self):
        return self.status == 'APPROVED'

class Notification(models.Model):
    TYPE_CHOICES = [
        ('follow', 'Nouvel abonné'),
        ('like', 'Nouveau like'),
        ('comment', 'Nouveau commentaire'),
        ('message', 'Nouveau message'),
    ]
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']



class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message de {self.sender} à {self.timestamp}"
