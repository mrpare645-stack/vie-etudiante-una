from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

@shared_task
def send_2fa_email_task(user_id, otp):
    """
    Envoie l'email de 2FA de manière asynchrone.
    """
    try:
        user = User.objects.get(id=user_id)
        subject = f"Code de connexion : {otp} - Administration UNA"
        body = f"""
Bonjour {user.first_name or user.username},

Votre code de vérification unique pour accéder au tableau de bord de l'administration du site "Vie Estudiantine UNA" est :

{otp}

Ce code est valide pour une seule utilisation et expirera bientôt.

Cordialement,
L'équipe technique de l'UNA
"""
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        return f"Email 2FA envoyé à {user.email}"
    except User.DoesNotExist:
        return "Utilisateur non trouvé."
    except Exception as e:
        # Log l'erreur pour le débogage
        print(f"Erreur lors de l'envoi de l'email 2FA: {e}")
        return f"Échec de l'envoi de l'email 2FA: {e}"

@shared_task
def send_moderation_email_task(subject, message):
    """
    Envoie un email de notification de modération de manière asynchrone.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER], fail_silently=True)
    return "Email de modération envoyé."