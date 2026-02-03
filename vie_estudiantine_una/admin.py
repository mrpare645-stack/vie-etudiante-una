from django.contrib import admin

from .models import (
    Actualite,
    Filiere,
    AboutUNA,
    Acteur,
    Temoin,
    Club_association,
    Evenement,
    ServiceCROU,
    Temoignage,
    Categorie,
    OffreLogement,
    Partenaire,
    Slide,
)

# Personnalisation de l'en-tête admin
admin.site.site_header = "Administration UNA - Vie Estudiantine"
admin.site.site_title = "Admin UNA"
admin.site.index_title = "Bienvenue à l'administration"


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "nom_auteur", "date_pub", "vues", "likes")
    list_filter = ("categorie", "date_pub")
    search_fields = ("titre", "resume", "nom_auteur")
    readonly_fields = ("date_pub", "vues", "likes")


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ("titre",)
    search_fields = ("titre", "description")


@admin.register(ServiceCROU)
class ServiceCROUAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie", "localisation", "contact")
    list_filter = ("categorie",)
    search_fields = ("nom", "description", "localisation")


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ("nom", "icon")
    search_fields = ("nom",)


@admin.register(AboutUNA)
class AboutUNAAdmin(admin.ModelAdmin):
    list_display = ("titre",)


@admin.register(Acteur)
class ActeurAdmin(admin.ModelAdmin):
    list_display = ("nom", "role")
    search_fields = ("nom", "role")


@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin):
    list_display = ("nom", "promotion")
    search_fields = ("nom", "promotion", "message")


@admin.register(Club_association)
class ClubAssociationAdmin(admin.ModelAdmin):
    list_display = ("nom_club", "domaine")
    list_filter = ("domaine",)
    search_fields = ("nom_club", "description", "domaine")


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = (
        "etudiant_nom",
        "filiere",
        "promotion",
        "date_publication",
        "est_approuve",
    )
    list_filter = ("filiere", "est_approuve", "date_publication")
    search_fields = ("etudiant_nom", "filiere", "message")
    readonly_fields = ("date_publication",)


@admin.register(OffreLogement)
class OffreLogementAdmin(admin.ModelAdmin):
    list_display = ("titre", "type_logement", "prix", "est_disponible")
    list_filter = ("type_logement", "est_disponible", "date_publication")
    search_fields = ("titre", "lieu", "description")
    readonly_fields = ("date_publication",)


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ("nom", "domaine")
    list_filter = ("domaine",)
    search_fields = ("nom", "description", "domaine")


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "icone")
    search_fields = ("nom",)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("titre", "ordre", "actif", "date_publication")
    list_filter = ("actif",)
    search_fields = ("titre", "sous_titre", "bouton_texte")
    ordering = ("ordre",)
    readonly_fields = ("date_publication",)

