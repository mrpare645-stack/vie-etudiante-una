from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Actualite, Banner, Filiere, AboutUNA, Acteur, Temoin, 
    Club_association, Evenement, ServiceCROU,
    Categorie,  Partenaire, Slide, Statistique
)

# --- Mixin pour les miniatures ---
class ImagePreviewMixin:
    def apercu_image(self, obj):
        for field in ['image', 'photo', 'icone', 'icon', 'logo']: # Ajout de 'logo' pour les clubs
            if hasattr(obj, field) and getattr(obj, field):
                try:
                    url = getattr(obj, field).url
                    return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 5px; object-fit: cover;" />', url)
                except:
                    continue
        return "No Image"
    apercu_image.short_description = "Aperçu"

# --- Administrations Spécifiques ---

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ('apercu_image', 'titre', 'categorie', 'date_pub', 'vues')
    list_display_links = ('titre',)
    list_filter = ('categorie', 'date_pub')
    search_fields = ('titre', 'resume', 'nom_auteur')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("apercu_image", "ordre", "titre", "actif")
    list_editable = ("ordre", "actif")
    list_display_links = ("titre",)
    ordering = ("ordre",)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin, ImagePreviewMixin):
    # On affiche la colonne 'page' pour savoir quelle bannière va où
    list_display = ("apercu_image", "page", "titre", "actif")
    list_editable = ("actif", "page")
    list_filter = ("page", "actif")

@admin.register(Club_association)
class ClubAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("apercu_image", "nom_club", "domaine", "is_approved")
    search_fields = ("nom_club",)

# --- Groupement pour les autres modèles ---

@admin.register(Filiere, Categorie, Partenaire, Acteur, ServiceCROU)
class NameBasedAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("nom", "apercu_image")
    search_fields = ("nom",)

@admin.register(Evenement, AboutUNA)
class TitleBasedAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("titre", "apercu_image")
    search_fields = ("titre",)

@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("nom", "promotion", "apercu_image", "is_approved")
    list_filter = ("is_approved", "promotion")
    search_fields = ("nom", "message")

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ("nombre_etudiants", "nombre_enseignants")
    
    def has_add_permission(self, request):
        # Empêche de créer plus d'une instance de configuration pour garder un seul jeu de stats
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
