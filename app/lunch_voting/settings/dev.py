from typing import List
from .common import *

DEBUG = True

SECRET_KEY = (
    "django-insecure--q&5x0un615u#p+jg&iy+!eqjkowjy=397pr*h^($qpiuvsqgp"
)

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = "redis://redis:6379/2"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_BACKEND = "redis://redis:6379/3"