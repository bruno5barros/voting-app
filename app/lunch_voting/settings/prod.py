import os
from typing import List
from .common import *
#import dj_database_url


DEBUG = False

# _+60kz7s4xd!#dq4ll0ag3_x6byi5%-d*r@9q9a)an-m5h1-hh
# DJANGO_SETTINGS_MODULE = lunch_voting.settings.prod
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS: List[str] = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "db",
        "NAME": "root",
        "USER": "root",
        "PASSWORD": "root",
    }
}

# DATABASES = {
#     "default": dj_database_url.config()
# }

REDIS_URL = os.environ["redis_url"]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


CELERY_BROKER_URL = REDIS_URL
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_BACKEND = REDIS_URL
