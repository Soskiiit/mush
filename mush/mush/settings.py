import os
import pkgutil
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = os.path.join(BASE_DIR, '.env')

load_dotenv(DOTENV_PATH)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = os.getenv('DJANGO_DEBUG', 'True') != 'False'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
INTERNAL_IPS = os.getenv('DJANGO_INTERNAL_IPS', '').split(',')
LOWRES_MODEL_FACE_COUNT = int(
    os.getenv('DJANGO_LOWRES_MODEL_FACE_COUNT', 10000)
)

ENABLE_PHOTOGRAMMETRY = os.getenv(
    'DJANGO_ENABLE_PHOTOGRAMMETRY', 'True'
) != 'False' and pkgutil.find_loader('Metashape') is not None

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'sorl.thumbnail',
    'django_browser_reload',
    # Project-specific
    'photogrammetry.apps.PhotogrammetryConfig',
    'theme.apps.ThemeConfig',
    'catalog.apps.CatalogConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    # Django
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Third-party
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'mush.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Django
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mush.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            '''django.contrib.auth.password_validation.'''
            '''UserAttributeSimilarityValidator'''
        ),
    },
    {
        'NAME': (
            '''django.contrib.auth.password_validation.'''
            '''MinimumLengthValidator'''
        ),
    },
    {
        'NAME': (
            '''django.contrib.auth.password_validation.'''
            '''CommonPasswordValidator'''
        ),
    },
    {
        'NAME': (
            '''django.contrib.auth.password_validation.'''
            '''NumericPasswordValidator'''
        ),
    },
]

DATABASE_DIR = DATABASES['default']['NAME']

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
    BASE_DIR / 'theme' / 'static',
]

AUTH_USER_MODEL = 'users.User'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_mail'
