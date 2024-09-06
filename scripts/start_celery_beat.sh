#!/bin/sh

echo "Starting celery beat..."
celery -A lunch_voting beat --loglevel=info
