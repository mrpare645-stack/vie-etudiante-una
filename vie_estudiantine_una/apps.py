from django.apps import AppConfig


class VieEstudiantineUnaConfig(AppConfig):
    name = 'vie_estudiantine_una'

    def ready(self):
        # Importer les signaux pour la création de profil
        import vie_estudiantine_una.signals

        # Configuration globale de l'admin au démarrage de l'application
        from django.contrib import admin
        admin.site.site_header = "🚀 UNA | Administration Professionnelle"
        admin.site.site_title = "Admin UNA"
        admin.site.index_title = "Tableau de Bord"
        admin.site.site_url = "/management/dashboard/"
