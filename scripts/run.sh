#!/bin/sh
set -e

python manage.py migrate
gunicorn -b :80 --chdir /app lunch_voting.wsgi:application

if [ "$1" = "drf" ]; then
    echo "Starting Django development server..."
    gunicorn -b :8000 --chdir /app lunch_voting.wsgi:application
elif [ "$1" = "celery-worker" ]; then
    echo "Starting Celery worker..."
    exec celery -A lunch_voting worker -l info
elif [ "$1" = "celery-beat" ]; then
    echo "Starting Celery beat..."
    exec celery -A lunch_voting beat --loglevel=info
else
    echo "Unknown command: $1"
    exec "$@"  # Pass any unknown command to the shell
fi
