"""Celery app config."""

from __future__ import absolute_import, unicode_literals
from .celery import app_celery

__all__ = ("app_celery",)
