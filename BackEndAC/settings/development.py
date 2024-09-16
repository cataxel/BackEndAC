from .__init__ import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_dev_db_name',
        'USER': 'your_dev_db_user',
        'PASSWORD': 'your_dev_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}