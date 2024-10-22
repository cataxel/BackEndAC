from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_systemac',
        'USER': 'axel',
        'PASSWORD': 'Admin2022&',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}