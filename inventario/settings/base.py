# from pathlib import Path
import os
from unipath import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY_TOKEN = os.environ.get("SECRET_KEY_TOKEN")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h1o+5l-mkolc8g4=k4$mno08##6o9e*2@ub9img^dmzmb5)tv2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]


APPS_LOCAL = [
    'apps.user',
    'apps.system',
    'apps.producto',
    'apps.almacen',
]


THY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_yasg'
]


INSTALLED_APPS = DJANGO_APPS + APPS_LOCAL + THY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

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

WSGI_APPLICATION = 'inventario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-VE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_ROOT_TEMP = MEDIA_ROOT.child('temp')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = BASE_DIR.child('staticfiles')

AUTH_USER_MODEL = 'user.user'
AUTH_AUTHENTICATION_TYPE="email"
# CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://voysweb.netlify.app"
]
ALGORITM_ENCAP_BACK = "RS256"
APPEND_SLASH=False

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}
