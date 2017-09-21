from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["pubfeeds.theonion.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pubfeeds',
        'USER': 'pubfeeds',
        'PASSWORD': 'nitffer',
        "HOST": "192.168.179.247",
    }
}

STATIC_URL = 'http://assets2.onionstatic.com/pubfeeds/'
