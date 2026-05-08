import re
import unicodedata
import logging
from django.conf import settings
from .tasks import send_moderation_email_task # Import de la tâche

logger = logging.getLogger(__name__)

# --- CONFIGURATION MODÉRATION ---

STATUS_CHOICES = [
    ('APPROVED', 'Approuvé'),
    ('PENDING', 'En attente de validation'),
    ('REJECTED', 'Masqué / Rejeté'),
]

# Liste étendue de mots-clés sensibles (Regex patterns)
SENSITIVE_PATTERNS = [
    r'\b(merde|con|putain|salope|encule|connard|batard)\b',  # Insultes basiques
    r'\b(viagra|cialis|casino|poker|bitcoin|crypto|forex)\b',   # Spam commercial
    r'\b(escort|prostituee?|sexe|porn|nude|bizi)\b',          # Contenu adulte
    r'\b(suicide|mourir|tuer|meurtre|viol|sang)\b',             # Violence
    r'\b(arnaque|fraude|argent facile|gratuit)\b',              # Scam
]

def normalize_text(text):
    """Normalise le texte : supprime les accents et met en minuscules."""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.lower()

def calculate_risk_score(content_text, user=None):
    """
    Calcule un score de risque de 0 à 100.
    0 = Sûr, 100 = Très risqué.
    """
    score = 0
    details = []
    normalized_content = normalize_text(content_text)

    # 1. Détection de mots interdits (Regex)
    for pattern in SENSITIVE_PATTERNS:
        matches = re.findall(pattern, normalized_content, re.IGNORECASE)
        if matches:
            count = len(matches)
            points = count * 20
            score += points
            details.append(f"Mots sensibles détectés ({count}): {', '.join(set(matches))}")

    # 2. Analyse heuristique : MAJUSCULES (Crier / Spam)
    if len(content_text) > 10:
        caps_ratio = sum(1 for c in content_text if c.isupper()) / len(content_text)
        if caps_ratio > 0.6:
            score += 15
            details.append("Usage excessif de majuscules")

    # 3. Analyse heuristique : Liens externes (Spam potentiel)
    link_count = content_text.count("http")
    if link_count > 0:
        score += 10 * link_count
        details.append(f"{link_count} liens détectés")

    # 4. Répétitions suspectes (ex: "aaaaaa", "!!!!!!")
    if re.search(r'(.)\1{4,}', content_text):
        score += 10
        details.append("Répétitions de caractères suspectes")

    # Logging pour audit
    if score > 0:
        user_info = f"User: {user.username} (ID: {user.id})" if user else "Anonymous"
        logger.warning(f"MODERATION RISK [{score}]: {user_info} | Details: {', '.join(details)}")

    return min(score, 100), details

def determine_status(score):
    """Définit le statut en fonction du score."""
    if score >= 40:
        return 'REJECTED'
    elif score >= 15:
        return 'PENDING'
    else:
        return 'APPROVED'

def notify_admin_moderation(content_object, score, details):
    """Envoie un email aux admins si un contenu est risqué."""
    if score >= 15:
        subject = f"⚠️ Alerte Modération : Contenu suspect (Score: {score})"
        message = f"""
        Un contenu nécessite votre attention.
        
        Type: {content_object.__class__.__name__}
        Auteur: {getattr(content_object, 'user', 'Inconnu')}
        Score de risque: {score}/100
        Statut attribué: {determine_status(score)}
        
        Détails de l'analyse :
        {', '.join(details)}
        
        Contenu :
        {str(content_object)}
        """
        # Appel de la tâche asynchrone. .delay() exécute la tâche en arrière-plan.
        send_moderation_email_task.delay(subject, message)