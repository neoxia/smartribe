from smartribe.settings import *


DEBUG = False
PROD = True

DATABASES = {
    'default': {
        'NAME': 'smartribe',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'smartribe',
        'PASSWORD': 'password',
        'HOST': '10.129.235.136',
    }
}

# Allowed IP addresses for server actions
ALLOWED_IP = ['127.0.0.1', '172.17.42.1', '95.85.39.49']

