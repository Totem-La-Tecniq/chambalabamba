import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = config('DEBUG', default=True, cast=bool)
# Archivos estáticos
STATIC_URL = "/static/"


# para Local
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
"""
# para Render:
MEDIA_ROOT = "/opt/render/project/src/media"
MEDIA_URL = "/media/"
"""

print ("BD",BASE_DIR)
# Seguridad
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
"""
ALLOWED_HOSTS = [
    "192.168.100.2",
    "192.168.100.2:8000",
    "localhost",
    "127.0.0.1",
]
"""

# Aplicaciones instaladas
INSTALLED_APPS = [
    'autenticacion.apps.AutenticacionConfig',
    "core.apps.CoreConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',

    "crispy_forms",
    "crispy_bootstrap4",
    "django_cleanup.apps.CleanupConfig",
    # apps personalizadas:
    "participa.apps.ParticipaConfig",
    'inicio',
    'filosofia',
    'saberes',
    'escuela',
    'hospedaje',
    'voluntariado',
    "donaciones.apps.DonacionesConfig",
    "tienda.apps.TiendaConfig",
    'noticias',
    'contacto',
     "blog",   # <-- debe estar
    'contenido',
    "eventos.apps.EventosConfig",
    "nosotros.apps.NosotrosConfig",
    "cooperaciones.apps.CooperacionesConfig",
    'visitas',
    "proyectos.apps.ProyectosConfig",

]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "perfil"
LOGOUT_REDIRECT_URL = "home"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]



# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


ROOT_URLCONF = 'chambalabamba.urls'
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format", "Bold", "Italic", "Underline", "Strike"],
            ["NumberedList", "BulletedList", "Blockquote"],
            ["Link", "Unlink"],
            ["Image", "Table"],
            ["RemoveFormat", "Source"],
        ],
        "height": 300,
        "width": "100%",
        "extraPlugins": ",".join(["uploadimage", "justify", "autolink"]),
        "removePlugins": "stylesheetparser",
        "forcePasteAsPlainText": False,
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chambalabamba.wsgi.application'



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
    os.path.join(BASE_DIR, 'contacto', 'static'),
    os.path.join(BASE_DIR, 'inicio', 'static'),
    os.path.join(BASE_DIR, 'nosotros', 'static'),
    os.path.join(BASE_DIR, 'donaciones', 'static'),
    os.path.join(BASE_DIR, 'blog', 'static'),
    os.path.join(BASE_DIR, 'participa', 'static'),
    os.path.join(BASE_DIR, 'tienda', 'static'),
    os.path.join(BASE_DIR, 'eventos', 'static'),
    os.path.join(BASE_DIR, 'visitas', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Base de datos
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.eu'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# PayPal settings
PAYPAL_RECEIVER_EMAIL = config('PAYPAL_RECEIVER_EMAIL', default='sb-wtmbn45974096@business.example.com')
PAYPAL_TEST = config('PAYPAL_TEST', default=True, cast=bool)
