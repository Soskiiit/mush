from importlib.metadata import packages_distributions
from pathlib import Path

from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent

environment_variables = dotenv_values()
environment_variables.setdefault('SECRET_KEY', 'test')
environment_variables.setdefault('DEBUG', 'True')
environment_variables.setdefault('ALLOWED_HOSTS', '')
environment_variables.setdefault('LOWRES_MODEL_FACE_COUNT', 10000)

SECRET_KEY = environment_variables['SECRET_KEY']
DEBUG = environment_variables['DEBUG'].upper() in ['1', 'TRUE', 'T']
ALLOWED_HOSTS = environment_variables['ALLOWED_HOSTS'].split()
LOWRES_MODEL_FACE_COUNT = environment_variables['LOWRES_MODEL_FACE_COUNT']

installed_packages = packages_distributions()
ENABLE_PHOTOGRAMMETRY = 'Metashape' in installed_packages

INSTALLED_APPS = [
    'photogrammetry.apps.PhotogrammetryConfig',
    'catalog.apps.CatalogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mush.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
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

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_mail'

AUTH_USER_MODEL = 'users.User'
