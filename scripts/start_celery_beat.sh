#!/bin/sh

exec celery -A lunch_voting beat --loglevel=info
