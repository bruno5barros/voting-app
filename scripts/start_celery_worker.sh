#!/bin/sh

exec celery -A lunch_voting worker -l info
