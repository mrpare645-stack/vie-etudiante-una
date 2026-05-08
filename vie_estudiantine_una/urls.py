# urls.py
from django.urls import path
from . import views

app_name = 'vie_estudiantine_una'

urlpatterns = [
    # --- ACCUEIL ---
    path('', views.accueil, name='accueil'),

    # --- NOUVELLES ROUTES AUTHENTIFICATION & ESPACE ÉTUDIANT ---
    path('auth/inscription/', views.register_view, name='register'),
    path('auth/connexion/', views.login_view, name='login'),
    path('auth/deconnexion/', views.logout_view, name='logout'),
    path('etudiant/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('etudiant/profil/modifier/', views.edit_profile, name='edit_profile'),
    path('club/<int:club_id>/follow/', views.toggle_follow_club, name='toggle_follow_club'),
    path('reaction/<str:model_type>/<int:item_id>/<str:reaction_type>/', views.toggle_reaction, name='toggle_reaction'),
    path('comment/<str:model_type>/<int:item_id>/', views.add_comment, name='add_comment'),

    # --- RÉSEAU SOCIAL ÉTUDIANT ---
    path('social/', views.social_feed, name='social_feed'),
    path('social/post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('social/profil/<str:username>/', views.profile_public, name='profile_public'),
    path('social/follow/<str:username>/', views.toggle_follow_user, name='toggle_follow_user'),
    path('social/like/<int:post_id>/', views.toggle_like_post, name='toggle_like_post'),
    path('social/comment/<int:post_id>/', views.add_post_comment, name='add_post_comment'),
    path('social/notifications/', views.notifications_view, name='notifications'),

    # --- ACTUALITÉS ---
    path('actualites/<int:id>/', views.course_details, name='course_details'),

    # --- FORMULAIRES ET ENVOIS ---
    path('envoyer-temoignage/', views.envoyer_temoignage, name='envoyer_temoignage'),
    path('envoyer-club/', views.envoyer_club, name='envoyer_club'),
    path('envoyer-service/', views.envoyer_service, name='envoyer_service'),

    # --- ESPACE GESTION (ADMIN CUSTOM) ---
    path('management/auth/', views.admin_2fa, name='admin_2fa'),
    path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Route pour Approuver (Appelée par {% url '...:valider' ... %})
    path('management/approve/<str:model_type>/<int:item_id>/', views.valider_item, name='valider'),
    
    # Route pour Supprimer/Refuser (Appelée par {% url '...:supprimer' ... %})
    # AJOUTE CETTE LIGNE :
    path('management/delete/<str:model_type>/<int:item_id>/', views.supprimer_item, name='supprimer'),

    # --- PAGES DYNAMIQUES (About, Club, Events, etc.) ---
    path('<str:page_name>/', views.content_pages, name='pages'),

    # --- MESSAGERIE ---
    path('messages/', views.chat_index, name='chat_index'),
    path('messages/<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('messages/start/<str:username>/', views.start_chat, name='start_chat'),

    # --- RECHERCHE ---
    path('recherche/', views.search_view, name='search'),
]