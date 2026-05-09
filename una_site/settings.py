import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-g+w)gf-n+1$ycng2)fvgx7h4nm+%x3wg%yw@35blz-nl@iy02n')

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host.strip()]

JAZZMIN_SETTINGS = {
    "site_header": "UNA Admin",
    "site_brand": "Vie Estudiantine UNA",
    "welcome_sign": "Bienvenue sur le gestionnaire UNA",
    "copyright": "Université Nangui Abrogoua",
    "search_model": ["vie_estudiantine_una.Actualite"],
    "site_url": "/",
    "topmenu_links": [
        {"name": "Voir le site", "url": "/", "new_window": True, "icon": "fas fa-globe"},
    ],
    "side_menu_groups": [
        {
            "name": "Communication",
            "models": ["vie_estudiantine_una.Actualite", "vie_estudiantine_una.Evenement", "vie_estudiantine_una.Slide", "vie_estudiantine_una.Banner"],
        },
        {
            "name": "Vie Étudiante & CROU",
            "models": ["vie_estudiantine_una.OffreLogement", "vie_estudiantine_una.ServiceCROU", "vie_estudiantine_una.Club_association"],
        },
        {
            "name": "Académique & Partenaires",
            "models": ["vie_estudiantine_una.Filiere", "vie_estudiantine_una.Partenaire", "vie_estudiantine_una.Acteur"],
        },
        {
            "name": "Retours & Témoignages",
            "models": ["vie_estudiantine_una.Temoignage", "vie_estudiantine_una.Temoin"],
        },
    ],
    "icons": {
        "vie_estudiantine_una.Actualite": "fas fa-newspaper",
        "vie_estudiantine_una.Evenement": "fas fa-calendar-alt",
        "vie_estudiantine_una.OffreLogement": "fas fa-home",
        "vie_estudiantine_una.Filiere": "fas fa-graduation-cap",
    },
}

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'vie_estudiantine_una',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'una_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'vie_estudiantine_una.context_processors.notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'una_site.wsgi.application'

# Base de données
if os.environ.get('DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = 'vie_estudiantine_una:login'

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'mrpare645@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Administration UNA <mrpare645@gmail.com>')

# Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}