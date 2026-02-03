from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.utils import OperationalError

from vie_estudiantine_una.models import (
    Actualite, Filiere, AboutUNA, Slide, Acteur, Temoin, Club_association,
    Evenement, ServiceCROU, OffreLogement, Partenaire, Temoignage
)


def accueil(request):
    """Page d'accueil avec les éléments clés"""
    actualites = Actualite.objects.all().order_by('-date_pub')[:3]
    filieres = Filiere.objects.all()
    about = AboutUNA.objects.first()
    acteurs = Acteur.objects.all()[:6]
    partenaires = Partenaire.objects.all()
    try:
        slides = Slide.objects.filter(actif=True).order_by('ordre')
    except OperationalError:
        # Si la table des slides n'existe pas encore (migrations non appliquées),
        # on évite l'erreur 500 en renvoyant une liste vide. Les slides par défaut
        # du template s'afficheront.
        slides = []
    # Top clubs (2 premiers, par défaut les plus récents)
    top_clubs = Club_association.objects.all().order_by('-id')[:2]
    # Événements récents (3 derniers)
    recent_events = Evenement.objects.all().order_by('-id')[:3]
    
    context = {
        'actualites': actualites,
        'filieres': filieres,
        'about': about,
        'acteurs': acteurs,
        'partenaires': partenaires,
        'slides': slides,
        'top_clubs': top_clubs,
        'recent_events': recent_events,
    }
    return render(request, 'mentor/index.html', context)


def about(request):
    """Page À propos"""
    about = AboutUNA.objects.first()
    temoins = Temoin.objects.all()
    acteurs = Acteur.objects.all()
    
    context = {
        'about': about,
        'temoins': temoins,
        'acteurs': acteurs,
    }
    return render(request, 'mentor/about.html', context)


def contact(request):
    """Page de contact"""
    return render(request, 'mentor/contact.html')


def courses(request):
    """Liste des actualités"""
    actualites = Actualite.objects.all().order_by('-date_pub')
    
    # Pagination
    paginator = Paginator(actualites, 9)  # 9 items par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'actualites': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'mentor/courses.html', context)


def course_details(request, id=None):
    """Détail d'une actualité"""
    if id:
        actualite = get_object_or_404(Actualite, id=id)
        # Incrémenter les vues
        actualite.vues += 1
        actualite.save(update_fields=['vues'])
    else:
        actualite = Actualite.objects.first()
    
    context = {
        'actualite': actualite,
    }
    return render(request, 'mentor/course-details.html', context)


def events(request):
    """Liste des événements"""
    evenements = Evenement.objects.all()
    
    context = {
        'evenements': evenements,
    }
    return render(request, 'mentor/events.html', context)


def pricing(request):
    """Services CROUA2"""
    services = ServiceCROU.objects.all()
    
    context = {
        'services': services,
    }
    return render(request, 'mentor/pricing.html', context)


def trainers(request):
    """Clubs et associations"""
    clubs = Club_association.objects.all()
    
    context = {
        'clubs': clubs,
    }
    return render(request, 'mentor/trainers.html', context)