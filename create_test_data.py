#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'una_site.settings')
django.setup()

from vie_estudiantine_una.models import *
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_test_image(name="test.jpg"):
    img = Image.new('RGB', (800, 600), color=(220, 20, 60))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return ContentFile(img_bytes.read(), name=name)

print("Creation des donnees de test...")

try:
    # Creer AboutUNA
    about, created = AboutUNA.objects.get_or_create(
        titre="Bienvenue a l'UNA",
        defaults={
            'description': 'Universite Nangui Abrogoua est une institution d\'enseignement superieur.',
            'image': create_test_image('about.jpg'),
            'point_1': 'Excellence academique',
            'point_2': 'Vie estudiantine dynamique',
            'point_3': 'Partenariats internationaux',
            'bouton_texte': 'En savoir plus',
            'bouton_lien': 'https://www.univ-na.ci/'
        }
    )
    print("OK AboutUNA")

    # Creer Filieres
    filieres_data = ['Informatique', 'Sciences', 'Lettres', 'Economie']
    for filiere_name in filieres_data:
        _, created = Filiere.objects.get_or_create(nom=filiere_name, defaults={'icon': 'bi-mortarboard'})
    print("OK Filieres")

    # Creer Acteurs
    for i in range(5):
        _, created = Acteur.objects.get_or_create(
            nom='Acteur ' + str(i+1),
            defaults={
                'role': 'Responsable',
                'photo': create_test_image('acteur' + str(i+1) + '.jpg'),
                'twitter': 'https://twitter.com/una' + str(i+1),
                'facebook': 'https://facebook.com/una' + str(i+1),
            }
        )
    print("OK Acteurs")

    # Creer Temoins
    for i in range(3):
        _, created = Temoin.objects.get_or_create(
            nom='Etudiant ' + str(i+1),
            defaults={
                'promotion': '2024',
                'photo': create_test_image('temoin' + str(i+1) + '.jpg'),
                'message': 'Mon experience a l\'UNA a ete transformatrice.'
            }
        )
    print("OK Temoins")

    # Creer Actualites
    for i in range(5):
        _, created = Actualite.objects.get_or_create(
            titre='Actualite ' + str(i+1) + ': Nouvelles du campus',
            defaults={
                'categorie': 'UNA',
                'resume': 'Resume de l\'actualite ' + str(i+1),
                'image': create_test_image('actualite' + str(i+1) + '.jpg'),
                'nom_auteur': 'Administration UNA',
                'image_auteur': create_test_image('author' + str(i+1) + '.jpg'),
                'vues': 100 + i*10,
                'likes': 20 + i*5
            }
        )
    print("OK Actualites")

    # Creer Evenements
    for i in range(3):
        _, created = Evenement.objects.get_or_create(
            titre='Evenement ' + str(i+1) + ': Grand evenement du campus',
            defaults={
                'photo': create_test_image('event' + str(i+1) + '.jpg'),
                'description': 'Description de l\'evenement ' + str(i+1),
                'details': 'Details complets de l\'evenement ' + str(i+1)
            }
        )
    print("OK Evenements")

    # Creer Services CROU
    services_data = [
        {'nom': 'Restauration', 'categorie': 'restauration', 'lieu': 'Cantine principale'},
        {'nom': 'Logement', 'categorie': 'logement', 'lieu': 'Residence universitaire'},
        {'nom': 'Sante', 'categorie': 'sante', 'lieu': 'Infirmerie UNA'},
    ]
    for service in services_data:
        _, created = ServiceCROU.objects.get_or_create(
            nom=service['nom'],
            defaults={
                'categorie': service['categorie'],
                'description': 'Service de ' + service['nom'].lower(),
                'localisation': service['lieu'],
                'horaires': '8h00 - 18h00',
                'contact': '+225 01234567',
                'image': create_test_image('service_' + service['nom'].lower() + '.jpg'),
            }
        )
    print("OK Services CROU")

    # Creer Clubs
    clubs_data = ['Informatique', 'Sportif', 'Culturel', 'Humanitaire']
    for club_name in clubs_data:
        _, created = Club_association.objects.get_or_create(
            nom_club='Club ' + club_name,
            defaults={
                'domaine': club_name,
                'description': 'Club specialise dans ' + club_name,
                'logo': create_test_image('club_' + club_name.lower() + '.jpg'),
                'url': 'https://club' + club_name.lower() + '.una.local'
            }
        )
    print("OK Clubs")

    print("\n" + "="*50)
    print("SUCCESS! Toutes les donnees de test sont prets!")
    print("="*50)
    print("\nVisitez le site a: http://127.0.0.1:8000/")
    print("Admin a: http://127.0.0.1:8000/admin/")
    print("username: admin")
    print("password: admin123")

except Exception as e:
    print("ERREUR: " + str(e))
    import traceback
    traceback.print_exc()
