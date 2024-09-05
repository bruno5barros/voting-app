#!/bin/sh
set -e

python manage.py migrate
gunicorn -b :80 --chdir /app lunch_voting.wsgi:application
