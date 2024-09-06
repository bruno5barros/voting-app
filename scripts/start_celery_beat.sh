#!/bin/sh

celery -A lunch_voting beat --loglevel=info
