"""Configure our celery instance."""

from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunch_voting.settings.dev")

app_celery = Celery("lunch_voting")
app_celery.config_from_object("django.conf:settings", namespace="CELERY")
app_celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=timedelta(hours=72),
)
app_celery.autodiscover_tasks()
