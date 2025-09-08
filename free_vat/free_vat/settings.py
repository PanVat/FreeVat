from pathlib import Path
from dotenv import load_dotenv
import shutil
import os

load_dotenv()  # Načtení proměnných prostředí z .env souboru

BASE_DIR = Path(__file__).resolve().parent.parent

# Získání tajného klíče z proměnné prostředí
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Nastavení pro vývojové prostředí z proměnné prostředí
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ## Vlastní aplikace ##
    'rest_framework',  # Django REST framework pro API
    'free_vat',  # Hlavní aplikace
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Pro více jazyků (Čeština, Angličtina)
]

ROOT_URLCONF = 'free_vat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'], # Cesta k šablonám
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'free_vat.wsgi.application'

# Použití PostgreSQL jako databáze
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'postgres',

        'USER': 'postgres',  # Uživatel z pgAdmin4

        'PASSWORD': 'admin',  # Heslo z pgAdmin4

        'HOST': 'localhost',

        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'cs-cz'

LANGUAGES = [
    ('cs', 'Čeština'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/' # Cesta ke statickým souborům

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
