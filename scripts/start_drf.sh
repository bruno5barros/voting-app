#!/bin/sh
set -e

python manage.py migrate
python manage.py setup_periodic_tasks
python manage.py setup_voting_locker
echo "Starting Django development server..."
gunicorn -b :8000 --chdir /app lunch_voting.wsgi:application
