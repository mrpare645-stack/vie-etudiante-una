import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Q, Case, When, Value, BooleanField
from django.urls import reverse
from django.apps import apps
from django.contrib.auth import login, logout, authenticate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .tasks import send_2fa_email_task
from .models import *
from .forms import UserUpdateForm, ProfileUpdateForm, PostForm, PostCommentForm # Import de la tâche
from .utils import calculate_risk_score, determine_status, notify_admin_moderation


def is_admin(user):
    """Vérifie si l'utilisateur est un administrateur connecté"""
    return user.is_authenticated and user.is_superuser

def get_common_context(page_key):
    """Récupère les éléments communs (Bannière, Témoins approuvés)"""
    banner_obj = Banner.objects.filter(page=page_key, actif=True).first()
    if not banner_obj:
        banner_obj = Banner.objects.filter(actif=True).first()

    return {
        'temoins': Temoin.objects.filter(is_approved=True).order_by('-id'),
        'banner': banner_obj,
    }

def get_public_stats():
    """Récupère les statistiques dynamiques pour le front-office"""
    # Récupère ou crée l'objet statistique par défaut
    stats_obj = Statistique.objects.first()
    if not stats_obj:
        stats_obj = Statistique.objects.create(nombre_etudiants="15000", nombre_enseignants="500")
    
    return {
        'stat_etudiants': stats_obj.nombre_etudiants,
        'stat_enseignants': stats_obj.nombre_enseignants,
        'stat_actualites': Actualite.objects.count(),
        'stat_events': Evenement.objects.filter(is_approved=True).count(),
        'stat_clubs': Club_association.objects.filter(is_approved=True).count(),
    }


def accueil(request):
    context = {
        'slides': Slide.objects.all(),
        'top_clubs': Club_association.objects.filter(is_approved=True)[:3],
        'actualites': Actualite.objects.all().order_by('-date_pub')[:3],
        'filieres': Filiere.objects.all(),
        'about': AboutUNA.objects.first(),
        'acteurs': Acteur.objects.all()[:6],
        'recent_events': Evenement.objects.filter(is_approved=True).order_by('-id')[:3],
        'partenaires': Partenaire.objects.all(),
        **get_public_stats(), # Injection des stats
        **get_common_context('accueil')
    }
    return render(request, 'mentor/index.html', context)

def course_details(request, id):
    """Détails d'une actualité"""
    actualite = get_object_or_404(Actualite, id=id)
    if hasattr(actualite, 'vues'):
        actualite.vues += 1
        actualite.save(update_fields=['vues'])
    
    # Récupération des commentaires (parents seulement, les réponses sont accessibles via .replies)
    ct = ContentType.objects.get_for_model(Actualite)
    comments = Commentaire.objects.filter(content_type=ct, object_id=actualite.id, parent=None).order_by('-date')
    
    # Récupération des réactions
    reactions = Reaction.objects.filter(content_type=ct, object_id=actualite.id)
    reaction_counts = {
        'LIKE': reactions.filter(reaction_type='LIKE').count(),
        'LOVE': reactions.filter(reaction_type='LOVE').count(),
        'FIRE': reactions.filter(reaction_type='FIRE').count(),
        'CLAP': reactions.filter(reaction_type='CLAP').count(),
    }
    user_reaction = None
    if request.user.is_authenticated:
        user_reaction = reactions.filter(user=request.user).first()

    return render(request, 'mentor/course-details.html', {'actualite': actualite, 'comments': comments, 'reaction_counts': reaction_counts, 'user_reaction': user_reaction})

def content_pages(request, page_name):
    """Gestion des pages dynamiques"""
    config = {
        'about':      {'model': Acteur,           'template': 'about.html',   'key': 'acteurs'},
        'actualites': {'model': Actualite,        'template': 'courses.html', 'key': 'actualites'},
        'events':     {'model': Evenement,        'template': 'events.html',  'key': 'evenements'},
        'crouA2':     {'model': ServiceCROU,      'template': 'crouA2.html',  'key': 'services'},
        'club':       {'model': Club_association, 'template': 'club.html',    'key': 'clubs'},
        'contact':    {'model': None,             'template': 'contact.html', 'key': None},
    }

    if page_name not in config:
        raise Http404("Page non trouvée")

    page_info = config[page_name]
    context = get_common_context(page_name)
    
    if page_name == 'about':
        context['about'] = AboutUNA.objects.first()
        context.update(get_public_stats()) # Injection des stats pour la page À Propos

    if page_info['model']:
        queryset = page_info['model'].objects.all()
        if hasattr(page_info['model'], 'is_approved'):
            queryset = queryset.filter(is_approved=True)
        context[page_info['key']] = queryset

    return render(request, f"mentor/{page_info['template']}", context)

@login_required
def envoyer_temoignage(request):
    """Réceptionne le formulaire de témoignage avec validation automatique."""
    if request.method == 'POST':
        message_text = request.POST.get('message')

        user = request.user
        profile = user.profile

        # Concaténer les champs texte pour la vérification
        content_to_check = f"{user.get_full_name()} {message_text}"

        # Analyse intelligente
        score, details = calculate_risk_score(content_to_check, user)
        status = determine_status(score)

        obj = Temoin.objects.create(
            user=user,
            nom=user.get_full_name() or user.username,
            promotion=profile.niveau or "Étudiant",
            message=message_text,
            photo=profile.photo,
            status=status
        )
        
        notify_admin_moderation(obj, score, details)

        if status == 'APPROVED':
            messages.success(request, "Votre ajout est en cours de traitement... ✅ Validé ! Votre témoignage est en ligne.")
        elif status == 'PENDING':
            messages.warning(request, "Votre témoignage contient des éléments nécessitant une validation manuelle. Il sera visible après approbation.")
        else:
            messages.error(request, "Votre témoignage a été masqué automatiquement car il semble enfreindre nos règles de communauté.")
        
        return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:accueil'))
    # Si la méthode n'est pas POST, rediriger vers le dashboard
    return redirect('vie_estudiantine_una:student_dashboard')

@login_required
def envoyer_club(request):
    """Réceptionne la proposition de club avec validation automatique."""
    if request.method == 'POST':
        nom = request.POST.get('nom_club')
        domaine = request.POST.get('domaine')
        description = request.POST.get('description')
        url = request.POST.get('url', '')
        logo = request.FILES.get('logo')

        # Concaténer les champs texte pour la vérification
        content_to_check = f"{nom} {domaine} {description}"

        # Analyse intelligente
        score, details = calculate_risk_score(content_to_check, request.user)
        status = determine_status(score)

        obj = Club_association.objects.create(
            proposer_par=request.user,
            nom_club=nom,
            domaine=domaine,
            description=description,
            url=url,
            logo=logo,
            status=status
        )
        
        notify_admin_moderation(obj, score, details)

        if status == 'APPROVED':
            messages.success(request, "Votre ajout est en cours de traitement... ✅ Validé ! Le club a été créé.")
        elif status == 'PENDING':
            messages.warning(request, "Votre club est en attente de validation par l'administration.")
        else:
            messages.error(request, "Votre proposition a été rejetée automatiquement (Contenu inapproprié).")
        
        return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:accueil'))
    return redirect('vie_estudiantine_una:student_dashboard')

@login_required
def envoyer_service(request):
    """Réceptionne la proposition de service étudiant avec validation automatique."""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        categorie = request.POST.get('categorie')
        description = request.POST.get('description')
        contact = request.POST.get('contact')
        localisation = request.POST.get('localisation')
        image = request.FILES.get('image')

        # Concaténer les champs texte pour la vérification
        content_to_check = f"{nom} {categorie} {description} {localisation}"

        # Analyse intelligente
        score, details = calculate_risk_score(content_to_check, request.user)
        status = determine_status(score)

        obj = ServiceCROU.objects.create(
            proposer_par=request.user,
            nom=nom,
            categorie=categorie,
            description=description,
            contact=contact,
            localisation=localisation,
            image=image,
            is_approved=(status == 'APPROVED'), # ServiceCROU n'a pas encore le champ status dans le modèle fourni, on garde is_approved pour l'instant ou on l'ajoute
            is_student=True
        )
        
        if status == 'APPROVED':
            messages.success(request, "Votre ajout est en cours de traitement... ✅ Validé ! Le service est en ligne.")
        else:
            messages.warning(request, "Votre service est en attente de modération.")

        return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:accueil'))
    return redirect('vie_estudiantine_una:student_dashboard')

# --- NOUVELLES VUES POUR L'ESPACE ÉTUDIANT ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('vie_estudiantine_una:student_dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Vous êtes maintenant connecté.")
            return redirect('vie_estudiantine_una:student_dashboard')
        else:
            messages.error(request, "Erreur d'inscription. Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserCreationForm()
    return render(request, 'mentor/section/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('vie_estudiantine_una:student_dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Rediriger vers la page 'next' si elle existe, sinon vers le dashboard
                next_page = request.POST.get('next') or request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('vie_estudiantine_una:student_dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    form = AuthenticationForm()
    return render(request, 'mentor/section/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('vie_estudiantine_una:accueil')

@login_required
def student_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "Votre profil étudiant a été initialisé. Pensez à le compléter !")

    # 1. Actualités de la filière (Recherche simple par nom de filière dans le titre/résumé)
    filiere_news = []
    if profile.filiere:
        filiere_news = Actualite.objects.filter(
            Q(titre__icontains=profile.filiere.nom) | 
            Q(resume__icontains=profile.filiere.nom)
        ).order_by('-date_pub')[:3]
    
    # Si pas de news spécifiques, on prend les dernières news générales
    if not filiere_news:
            filiere_news = Actualite.objects.order_by('-date_pub')[:3]

    # 2. Événements recommandés (Basé sur les centres d'intérêt)
    suggested_events = Evenement.objects.filter(is_approved=True).order_by('-id')[:3] # Par défaut : les plus récents
    
    if profile.centres_interet:
        keywords = [k.strip() for k in profile.centres_interet.split(',')]
        if keywords:
            # Construction d'une requête pour chercher n'importe quel mot clé
            query = Q()
            for k in keywords:
                if k:
                    query |= Q(description__icontains=k) | Q(titre__icontains=k)
            
            matched_events = Evenement.objects.filter(query, is_approved=True).distinct()
            if matched_events.exists():
                suggested_events = matched_events[:3]

    # Récupération des contributions de l'utilisateur
    my_temoignages = Temoin.objects.filter(user=request.user).order_by('-id')
    my_clubs = Club_association.objects.filter(proposer_par=request.user).order_by('-id')
    my_services = ServiceCROU.objects.filter(proposer_par=request.user).order_by('-id')

    context = {
        'profile': profile,
        'filiere_news': filiere_news,
        'suggested_events': suggested_events,
        'my_contributions': list(my_temoignages) + list(my_clubs) + list(my_services),
    }
    return render(request, 'mentor/section/student_dashboard.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre profil a été mis à jour avec succès !')
            return redirect('vie_estudiantine_una:student_dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'mentor/section/edit_profile.html', context)

@login_required
def toggle_follow_club(request, club_id):
    """Permet de suivre ou ne plus suivre un club."""
    club = get_object_or_404(Club_association, id=club_id)
    profile = request.user.profile
    
    if club in profile.clubs_suivis.all():
        profile.clubs_suivis.remove(club)
        messages.info(request, f"Vous ne suivez plus le club {club.nom_club}.")
    else:
        profile.clubs_suivis.add(club)
        messages.success(request, f"Vous suivez maintenant le club {club.nom_club} !")
        
    return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:accueil'))

@login_required
def toggle_reaction(request, model_type, item_id, reaction_type):
    """AJAX: Ajoute ou modifie une réaction (Like, Love, Fire, Clap)"""
    mapping = {'actualite': Actualite, 'event': Evenement, 'club': Club_association}
    model = mapping.get(model_type)
    
    if not model:
        return JsonResponse({'error': 'Type invalide'}, status=400)
        
    obj = get_object_or_404(model, id=item_id)
    ct = ContentType.objects.get_for_model(model)
    
    # Vérifier si l'utilisateur a déjà réagi
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        content_type=ct,
        object_id=obj.id,
        defaults={'reaction_type': reaction_type}
    )
    
    if not created:
        if reaction.reaction_type == reaction_type:
            # Si on clique sur la même réaction, on l'enlève (toggle off)
            reaction.delete()
            action = 'removed'
        else:
            # Sinon on change le type
            reaction.reaction_type = reaction_type
            reaction.save()
            action = 'updated'
    else:
        action = 'created'
        
    # Recalculer les totaux pour mettre à jour l'UI
    all_reactions = Reaction.objects.filter(content_type=ct, object_id=obj.id)
    counts = {
        'LIKE': all_reactions.filter(reaction_type='LIKE').count(),
        'LOVE': all_reactions.filter(reaction_type='LOVE').count(),
        'FIRE': all_reactions.filter(reaction_type='FIRE').count(),
        'CLAP': all_reactions.filter(reaction_type='CLAP').count(),
    }
    
    return JsonResponse({'status': 'ok', 'action': action, 'counts': counts})

@login_required
def add_comment(request, model_type, item_id):
    mapping = {'actualite': Actualite, 'event': Evenement, 'club': Club_association}
    model = mapping.get(model_type)
    if request.method == 'POST' and model:
        obj = get_object_or_404(model, id=item_id)
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        parent = Commentaire.objects.get(id=parent_id) if parent_id else None
        
        Commentaire.objects.create(
            user=request.user,
            text=text,
            parent=parent,
            content_object=obj
        )
        messages.success(request, "Commentaire ajouté !")
    return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:accueil'))

# --- MODULE RÉSEAU SOCIAL ---

@login_required
def social_feed(request):
    """Fil d'actualité du réseau social étudiant"""
    # Création de post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Analyse de modération
            content = form.cleaned_data.get('content', '')
            score, details = calculate_risk_score(content, request.user)
            status = determine_status(score)

            post = form.save(commit=False)
            post.author = request.user
            post.status = status
            post.save()
            
            notify_admin_moderation(post, score, details)

            if status == 'REJECTED':
                messages.error(request, "Votre post a été masqué car il ne respecte pas nos règles.")
            elif status == 'PENDING':
                messages.warning(request, "Votre post est en attente de validation.")
            else:
                messages.success(request, "Post publié !")
            return redirect('vie_estudiantine_una:social_feed')
    else:
        form = PostForm()

    # Récupération des IDs des utilisateurs suivis pour le template et le tri
    followed_users_ids = list(request.user.following.values_list('following__id', flat=True))

    # Récupération des posts : Priorité aux abonnements (is_followed=True), puis chronologique
    # FILTRE : On ne montre que les posts APPROUVÉS, sauf si c'est l'auteur qui regarde (il voit ses Pending/Rejected)
    posts = Post.objects.filter(
        Q(status='APPROVED') | Q(author=request.user)
    ).select_related('author__profile').prefetch_related('post_likes', 'post_comments').annotate(
        is_followed=Case(
            When(author__id__in=followed_users_ids, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by('-is_followed', '-created_at')
    
    # Notifications non lues
    unread_notifs = Notification.objects.filter(recipient=request.user, is_read=False).count()

    context = {
        'form': form,
        'posts': posts,
        'unread_notifs': unread_notifs,
        'followed_users_ids': followed_users_ids,
    }
    return render(request, 'mentor/section/social_feed.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, "Post supprimé.")
    else:
        messages.error(request, "Vous n'avez pas la permission.")
    return redirect('vie_estudiantine_una:social_feed')

@login_required
def profile_public(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj)
    
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()

    followers_count = user_obj.followers.count()
    following_count = user_obj.following.count()

    context = {
        'profile_user': user_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    }
    return render(request, 'mentor/section/profile_public.html', context)

@login_required
def toggle_follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    
    if target_user == request.user:
        return redirect('vie_estudiantine_una:profile_public', username=username)

    follow_instance = Follow.objects.filter(follower=request.user, following=target_user).first()
    
    if follow_instance:
        follow_instance.delete()
        messages.info(request, f"Vous ne suivez plus {target_user.username}.")
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        # Notification
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            message=f"{request.user.username} a commencé à vous suivre."
        )
        messages.success(request, f"Vous suivez maintenant {target_user.username} !")
        
    # Rediriger vers la page précédente (fil d'actu) ou le profil si pas de referer
    return redirect(request.META.get('HTTP_REFERER', reverse('vie_estudiantine_una:profile_public', args=[username])))

@login_required
def toggle_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = PostLike.objects.filter(user=request.user, post=post).first()
    
    if like:
        like.delete()
    else:
        PostLike.objects.create(user=request.user, post=post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post,
                message=f"{request.user.username} a aimé votre post."
            )
            
    return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:social_feed'))

@login_required
def add_post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content', '')
            score, details = calculate_risk_score(content, request.user)
            status = determine_status(score)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.status = status
            comment.save()
            
            if status == 'REJECTED':
                messages.error(request, "Commentaire masqué (contenu inapproprié).")
            elif status == 'PENDING':
                messages.warning(request, "Commentaire en attente de validation.")
            elif post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    message=f"{request.user.username} a commenté votre post."
                )
    return redirect(request.META.get('HTTP_REFERER', 'vie_estudiantine_una:social_feed'))

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(recipient=request.user)
    # Marquer comme lu
    notifs.update(is_read=True)
    return render(request, 'mentor/section/notifications.html', {'notifications': notifs})

# ESPACE ADMIN & 2FA


@user_passes_test(is_admin)
def admin_2fa(request):
    """Gère l'authentification à deux facteurs pour le dashboard"""
    # --- Gestion du renvoi de code ---
    if request.GET.get('resend'):
        if 'otp_code' in request.session:
            del request.session['otp_code']
        messages.info(request, "Un nouveau code a été généré et envoyé.")
        return redirect('vie_estudiantine_una:admin_2fa')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if otp_input == str(request.session.get('otp_code')):
            request.session['2fa_verified'] = True
            del request.session['otp_code'] 
            return redirect('vie_estudiantine_una:admin_dashboard')
        else:
            messages.error(request, "Code incorrect.")

    if not request.session.get('otp_code'):
        otp = random.randint(100000, 999999)
        request.session['otp_code'] = otp
        
        # Email de réception configuré pour la démo
        email_destinataire = request.user.email

        # Création de l'email masqué pour l'affichage (ex: mrp****@gmail.com)
        email_masque = "votre adresse email"
        if email_destinataire and '@' in email_destinataire:
            try:
                nom, domaine = email_destinataire.split('@')
                visible = nom[:3] if len(nom) > 3 else nom[:1]
                email_masque = f"{visible}****@{domaine}"
            except:
                pass

        # --- NOUVEAU BLOC DE DÉBOGAGE ---
        print("\n" + "="*50)
        print(">>> DÉBUT DU DÉBOGAGE 2FA <<<")
        print(f"Utilisateur connecté : {request.user.username}")
        print(f"Email de destination : {email_destinataire}")
        print(f"Email d'envoi (settings.py) : {settings.EMAIL_HOST_USER}")
        print(f"Code OTP généré : {otp}")
        print("Tentative d'envoi de l'email...")
        # --- FIN DU BLOC DE DÉBOGAGE ---

        if not email_destinataire:
            messages.error(request, "Votre compte admin n'a pas d'adresse email configurée. Veuillez l'ajouter via l'interface admin Django.")
            print("ERREUR CRITIQUE : L'utilisateur connecté n'a pas d'email.")
            return render(request, 'mentor/section/admin_2fa.html')

        # Appel de la tâche asynchrone au lieu de send_mail direct
        result = send_2fa_email_task.delay(request.user.id, otp)
        if result: # Celery retourne un objet AsyncResult
            print(">>> SUCCÈS : La tâche d'envoi d'email a été mise en file d'attente.")
            print("="*50 + "\n")
            messages.success(request, f"Code de sécurité envoyé à {email_masque}")

    return render(request, 'mentor/section/admin_2fa.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard de gestion"""
    if not request.session.get('2fa_verified', False):
        return redirect('vie_estudiantine_una:admin_2fa')

    # Seuls les événements nécessitent une validation manuelle maintenant.
    events_pending = Evenement.objects.filter(is_approved=False).order_by('-id')
   
    total_vues = Actualite.objects.aggregate(Sum('vues'))['vues__sum'] or 0
    
    stats = {
        'total_actualites': Actualite.objects.count(),
        'total_events': Evenement.objects.filter(is_approved=True).count(),
        'total_clubs': Club_association.objects.count(),
        'total_services': ServiceCROU.objects.count(),
        'total_temoins': Temoin.objects.count(),
        'total_partenaires': Partenaire.objects.count(),
        'total_vues': total_vues,
        'pending_total': events_pending.count()
    }

    # --- Raccourcis vers les tables de l'Admin Django ---
    admin_shortcuts = []
    try:
        
        app_config = apps.get_app_config('vie_estudiantine_una')
        for model in app_config.get_models():
            try:
                
                url_name = f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist'
                admin_shortcuts.append({
                    'name': model._meta.verbose_name_plural.capitalize(),
                    'url': reverse(url_name),
                    'count': model.objects.count()
                })
            except Exception:
                continue 
        admin_shortcuts.sort(key=lambda x: x['name'])
    except LookupError:
        pass

    

    print(f"📊 Dashboard Admin: {len(admin_shortcuts)} tables trouvées.")

    context = {
        'events_pending': events_pending,
        'stats': stats,
        'recent_news': Actualite.objects.order_by('-date_pub')[:5],
        'admin_shortcuts': admin_shortcuts,
        **get_common_context('admin')
    }
    return render(request, 'mentor/admin_dashboard.html', context)

@user_passes_test(is_admin)
def valider_item(request, model_type, item_id):
    """Approuve un item"""
    mapping = {'club': Club_association, 'event': Evenement, 'temoin': Temoin, 'service': ServiceCROU}
    model = mapping.get(model_type)
    if model:
        obj = get_object_or_404(model, id=item_id)
        obj.is_approved = True
        obj.save(update_fields=['is_approved'])
        messages.success(request, f"{model_type.capitalize()} publié !")
    return redirect('vie_estudiantine_una:admin_dashboard')

@user_passes_test(is_admin)
def supprimer_item(request, model_type, item_id):
    """Supprime un item"""
    mapping = {'club': Club_association, 'event': Evenement, 'temoin': Temoin, 'service': ServiceCROU}
    model = mapping.get(model_type)
    if model:
        obj = get_object_or_404(model, id=item_id)
        obj.delete()
        messages.warning(request, f"{model_type.capitalize()} supprimé.")
    return redirect('vie_estudiantine_una:admin_dashboard')

# --- MESSAGERIE PRIVÉE ---

@login_required
def chat_index(request):
    """Affiche la liste des conversations"""
    conversations = request.user.conversations.all().prefetch_related('participants', 'messages')
    
    # Enrichir les conversations avec le "destinataire" (l'autre personne)
    for conv in conversations:
        conv.other_user = conv.participants.exclude(id=request.user.id).first()
        conv.last_message = conv.messages.last()

    return render(request, 'mentor/section/chat_index.html', {'conversations': conversations})

@login_required
def chat_room(request, conversation_id):
    """Affiche une conversation spécifique"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    other_user = conversation.participants.exclude(id=request.user.id).first()
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Créer une notification pour le destinataire
            if other_user:
                Notification.objects.create(
                    recipient=other_user,
                    sender=request.user,
                    notification_type='message',
                    message=f"Nouveau message de {request.user.username}",
                    conversation=conversation
                )
            return redirect('vie_estudiantine_una:chat_room', conversation_id=conversation_id)

    # Marquer les messages comme lus
    conversation.messages.exclude(sender=request.user).update(is_read=True)
    
    chat_messages = conversation.messages.order_by('timestamp')

    return render(request, 'mentor/chat_room.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'other_user': other_user
    })

@login_required
def start_chat(request, username):
    """Crée ou récupère une conversation avec un utilisateur"""
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('vie_estudiantine_una:chat_index')

    # Chercher une conversation existante entre ces deux utilisateurs
    # Note: Cette logique simple suppose des conversations à 2 uniquement
    conversations = Conversation.objects.filter(participants=request.user).filter(participants=target_user)
    
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, target_user)
    
    return redirect('vie_estudiantine_una:chat_room', conversation_id=conversation.id)

def search_view(request):
    """
    Gère la recherche sur le site.
    Recherche dans les actualités, clubs, événements et profils utilisateurs.
    """
    query = request.GET.get('q', '')
    results = {
        'actualites': [],
        'clubs': [],
        'evenements': [],
        'profils': [],
    }
    total_results = 0

    if query:
        # Recherche dans les Actualités
        results['actualites'] = Actualite.objects.filter(
            Q(titre__icontains=query) | Q(resume__icontains=query) | Q(description__icontains=query)
        ).distinct()

        # Recherche dans les Clubs (uniquement ceux qui sont approuvés)
        results['clubs'] = Club_association.objects.filter(
            Q(nom_club__icontains=query) | Q(description__icontains=query) | Q(domaine__icontains=query),
            status='APPROVED' 
        ).distinct()

        # Recherche dans les Événements (uniquement ceux qui sont approuvés)
        results['evenements'] = Evenement.objects.filter(
            Q(titre__icontains=query) | Q(description__icontains=query),
            is_approved=True
        ).distinct()

        # Recherche dans les profils utilisateurs
        user_qs = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        results['profils'] = Profile.objects.filter(
            Q(user__in=user_qs) | Q(bio__icontains=query)
        ).select_related('user').distinct()

        total_results = sum(len(v) for v in results.values())

    context = {
        'query': query,
        'results': results,
        'total_results': total_results,
    }
    return render(request, 'mentor/section/search_results.html', context)