#!/bin/sh

echo "Starting celery worker..."
celery -A lunch_voting worker -l info
