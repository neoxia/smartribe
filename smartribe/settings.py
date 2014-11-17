"""
Django settings for smartribe project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^tb)yl#7-fk*vch+e5@cjbcsi6)otseo*ft4c6ze+-*(n$kiw0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PROD = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

# Django do spliting with '.' for determining app from class
# so we can't set our User from core.models.User
# see core/__init__.py to see the trick
INSTALLED_APPS = (
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework',
    'api',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.auth.models',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend', 'rest_framework.filters.SearchFilter'),
    'PAGINATE_BY': 10,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/day'
    }
}

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'smartribe.urls'

WSGI_APPLICATION = 'smartribe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'NAME': 'smartribe',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'smartribe',
            'PASSWORD': 'password',
            'HOST': '10.129.235.136',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# JWT parameters
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600*10)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.gandi.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@smartri.be'
EMAIL_HOST_PASSWORD = 'sjhqd6qsjhdsqjhgHJGqsljkdhsqkjdhqkjsqdhkqshdsq'
EMAIL_USE_TLS = True

MEDIA_ROOT = 'media/'

MEDIA_URL = '/media/'

# Password recovery token validity (hour) :
PRT_VALIDITY = 1

# Warning threshold for inappropriate content :
INAP_LIMIT = 5

# Allowed IP addresses for server actions
ALLOWED_IP = ['127.0.0.1', '192.168.161.12']
