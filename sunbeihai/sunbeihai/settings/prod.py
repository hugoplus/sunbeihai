import os
from .base import *

DEBUG = False

ADMINS = [
    ('Beihai Sun', 'beihaisun@gmail.com'),
]

ALLOWED_HOSTS = ['sunbeihai.com', 'www.sunbeihai.com',]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Redis settings
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND')