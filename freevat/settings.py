from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _  # Pro překlad do jiných jazyků
import os

from environ import Env

env = Env()
env.read_env()

load_dotenv()  # Načtení proměnných prostředí z .env souboru

BASE_DIR = Path(__file__).resolve().parent.parent

# Zde se ukládají mediální soubory databáze
MEDIA_ROOT = BASE_DIR / 'media'

# URL, pod kterou jsou mediální soubory dostupné v prohlížeči
MEDIA_URL = '/media/'

# Získání tajného klíče z proměnné prostředí
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Nastavení pro vývojové prostředí z proměnné prostředí
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Povolené hosty, načtené z proměnné prostředí
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ## Allauth ##
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    ## Poskytovatelé Allauth ##
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    ## Vlastní aplikace ##
    'freevat.apps.ModelsConfig',  # Hlavní aplikace
    'users.apps.UsersConfig',  # Aplikace pro správu uživatelů

    ## Třetí strany ##
    'rosetta',  # Rosetta (vícejazyčnost)
    'django_browser_reload',  # Pro automatické obnovení stránky při změně kódu
    'crispy_forms',  # Crispy - pro lepší vzhled formulářů
    'crispy_tailwind'  # Pro použití Tailwind CSS s crispy_forms
]

# Důležité kvůli chybě
SITE_ID = 1

# Nastavení pro crispy_forms a Tailwind CSS
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Backendy pro autentizaci
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

INTERNAL_IPS = [
    "127.0.0.1"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Pro více jazyků
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",  # Pro automatické obnovení stránky při změně kódu
]

# Nastavení pro přihlášení přes sociální sítě
SOCIALACCOUNT_PROVIDERS = {
    # Google
    'google': {
        'APP': {
            'client_id': env('OAUTH_GOOGLE_CLIENT_ID'),
            'secret': env('OAUTH_GOOGLE_SECRET'),
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'EXTRACT_EMAIL': True,
    },
    # GitHub
    'github': {
        'APP': {
            'client_id': env('OAUTH_GITHUB_CLIENT_ID'),
            'secret': env('OAUTH_GITHUB_SECRET'),
        },
        'SCOPE': [
            'user',
            'user:email',
        ],
    }
}

# Zobrazí se klasický Google login formulář
SOCIALACCOUNT_LOGIN_ON_GET = True

# Přesměrování po přihlášení a odhlášení
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Nastavení pro Allauth
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Automaticky načti profilovou fotku
SOCIALACCOUNT_AUTO_SIGNUP = True

# Pro Django Allauth
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

ROOT_URLCONF = 'freevat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Cesta k šablonám
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

WSGI_APPLICATION = 'freevat.wsgi.application'

# Použití PostgreSQL jako databáze (vše se načítá z proměnných prostředí)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT"),
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

# Výchozí jazyk aplikace
LANGUAGE_CODE = 'cs'

# Více jazyků, mezi kterými lze přepínat
LANGUAGES = [
    ('en', _('English')),  # Angličtina
    ('cs', _('Czech')),  # Čeština
    ('de', _('German')),  # Němčina
]

# Cesta k překladovým souborům
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'Europe/Prague'

USE_I18N = True  # Povolení mezinárodní podpory
USE_L10N = True  # Povolení lokalizace (např. datum)

USE_TZ = True

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_URL = '/static/'  # Pod touto URL jsou statické soubory dostupné v prohlížeči

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Uživatelský model
AUTH_USER_MODEL = 'users.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
