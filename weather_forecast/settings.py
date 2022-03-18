"""
Django settings for weather_forecast project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import environ

from pathlib import Path
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool, True),
)
# reading .env file
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-9#)+1%1v8b6v*p4gag^(5s(d4sw(4k675$vovk5rrn-+1#u+_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
TESTING = sys.argv[1:2] == ['test']

# For now ALL ALLOWED
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['localhost', '*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'django_extensions',
    'drf_yasg',

    'api.oraculum'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'weather_forecast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'weather_forecast.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# SIMPLE_EMAIL_CONFIRMATION_KEY_LENGTH = 6

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

SITE_URL = env.str('SITE_URL', default='http://0.0.0.0:81')
FRONT_URL = env.str('FRONT_URL', default='http://localhost:3000')

LANGUAGES = (
    ('es', _('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),  # here makemessages modify
    # Override modules, here makemessages dont modify
    os.path.join(BASE_DIR, 'locale_extras'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),  # Where search
)
STATIC_ROOT = os.path.join(BASE_DIR, env.str(
    'STATIC_ROOT', default='static'))  # Where compile

# For default (only debug work in django server), in other case set explicit base url
MEDIA_URL = '/media/'
if env.str('MEDIA_SERVER', default='NONE') != 'NONE':
    MEDIA_URL = env.str('MEDIA_SERVER')
# For default store in root_folder/media in other case set full path
MEDIA_ROOT = os.path.join(BASE_DIR, env.str('MEDIA_ROOT', default='media'))
if env.str('MEDIA_ROOT', default='media') != 'media':
    MEDIA_ROOT = env.str('MEDIA_ROOT', default='media')

DEFAULT_CACHING_TIME = env.str('CACHE_TIMEOUT', default=60 * 10)

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'TIMEOUT': DEFAULT_CACHING_TIME,
        "KEY_PREFIX": "weather_forecast"
    }
}

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),

    'DEFAULT_PAGINATION_CLASS': 'common.utils.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 25,

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    )
}

# Security
PUBLIC_KEY = env.str('PUBLIC_KEY', default='').encode("utf-8")
PRIVATE_KEY = env.str('PRIVATE_KEY', default='').encode("utf-8")

JWT_AUTH_HEADER_PREFIX = env.str('JWT_AUTH_HEADER_PREFIX', default='Bearer')
RSA_ALGORITHM = env.str('RSA_ALGORITHM', default='RS256')

ALLOWED_PUBLIC_KEYS = [
    PUBLIC_KEY
]

try:
    from .secrets import APP_KEY

    SECRET_KEY = APP_KEY
except ImportError:
    # Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
    SECRET_KEY = env.str(
        'SECRET_KEY', default='jv5(78$62-hr+8==+kn4%r*(9g)fubx&&i=3ewc9p*tnkt6u$h')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=25),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'UPDATE_LAST_LOGIN': True,

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

# or sendgrid.EmailBackend, or...
EMAIL_BACKEND = env.str('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = int(env('EMAIL_PORT', default=587))
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='weather_forecast@gmail.com')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='weather_forecast')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=False)

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)
SERVER_EMAIL = env.str('SERVER_EMAIL', default=EMAIL_HOST_USER)

if TESTING:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# LOGGINGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug-weather-forecast-api.log',
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],  # ,'console']
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'ERROR',  # DEBUG for print queries
            'handlers': ['console'],
            'propagate': False
        }
    },
}

SWAGGER_SETTINGS = {
    'LOGIN_URL': '{}/admin/login'.format(SITE_URL),
    'LOGOUT_URL': '{}/admin/logout'.format(SITE_URL),
    'SECURITY_DEFINITIONS': {
        "api_key": {
            "type": "apiKey",
            "name": "authorization",
            "in": "header"
        },
        "basic": {
            "type": "basic"
        }
    },
}

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('DATABASE_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env.str('DATABASE_NAME', default='weather_forecast'),
        'USER': env.str('DATABASE_USER', default='weather_forecast'),
        'PASSWORD': env.str('DATABASE_PASSWORD', default='weather_forecast'),
        'HOST': env.str('DATABASE_HOST', default='localhost'),
        'PORT': env.str('DATABASE_PORT', default='5432'),
    }
}

DATABASE_URL = os.getenv('DATABASE_URL', None)
if DATABASE_URL:
    DATABASES['default'] = env.db()

OWM_API_URL = env.str('OWM_API_URL', default='https://api.openweathermap.org/data/2.5/')
OWM_API_TOKEN = env.str('OWM_API_TOKEN', default='')

# Incorporo las configuraciones locales - Las que hay que modificar por ambiente
try:
    from .local_settings import *
except ImportError:
    pass
