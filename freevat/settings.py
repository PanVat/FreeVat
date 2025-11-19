from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _  # Pro překlad do jiných jazyků
import os

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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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

# Nastavení pro crispy_forms a Tailwind CSS
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Přesměrování pro přihlášení/odhlášení
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'users:login'

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

# Použití PostgreSQL jako databáze
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'freevat',

        'USER': 'admin',  # Uživatel z pgAdmin4

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

# Důležité kvůli chybě
SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
