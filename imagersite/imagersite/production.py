import os
import dj_database_url
from .settings import *

DEBUG = os.environ.get("DEBUG")
THUMBNAIL_DEBUG = os.environ.get("DEBUG")
SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
ALLOWED_HOSTS = [
    '.us-west-2.compute.amazonaws.com',
    'localhost',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
