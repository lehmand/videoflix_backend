"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

CORS_ALLOW_ALL_ORIGINS = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
# CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = []
for origin in csrf_origins:
    if origin:  # Skip empty strings
        if not (origin.startswith('http://') or origin.startswith('https://')):
            origin = f'https://{origin}'
        CSRF_TRUSTED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'user_auth',
    'corsheaders',
    'videos.apps.VideosConfig',
    'debug_toolbar',
    'django_rq',
    'import_export',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


RQ_QUEUES = {
    'default': {
        'HOST':     os.getenv('REDIS_HOST', 'localhost'),
        'PORT':     int(os.getenv('REDIS_PORT', 6379)),
        'DB':       int(os.getenv('REDIS_DB', 0)),
        'PASSWORD': os.getenv('REDIS_PASSWORD', None),
        'DEFAULT_TIMEOUT':   int(os.getenv('RQ_DEFAULT_TIMEOUT', 360)),
        'DEFAULT_RESULT_TTL':int(os.getenv('RQ_DEFAULT_RESULT_TTL', 800)),
    }
}

ROOT_URLCONF = 'videoflix.urls'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_CACHE_URL", "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            **({"PASSWORD": os.getenv("REDIS_PASSWORD")} 
                if os.getenv("REDIS_PASSWORD") 
                else {}),
        },
        "KEY_PREFIX": os.getenv("CACHE_KEY_PREFIX", "videoflix"),
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

CACHE_TTL = 60 * 15

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = 'videoflix.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.getenv("POSTGRES_NAME"),
        "USER":     os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST":     os.getenv("POSTGRES_HOST"),
        "PORT":     os.getenv("POSTGRES_PORT"),
    }
}

EMAIL_BACKEND       = os.getenv('EMAIL_BACKEND')
EMAIL_HOST          = os.getenv('EMAIL_HOST')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT', 25))
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_USE_SSL       = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = os.getenv('DEFAULT_FROM_EMAIL')


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_auth.User'

FRONTEND_URL = os.getenv('FRONTEND_URL')
