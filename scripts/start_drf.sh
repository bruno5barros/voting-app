#!/bin/sh
set -e

python manage.py migrate
echo "Starting Django development server..."
gunicorn -b :8000 --chdir /app lunch_voting.wsgi:application
