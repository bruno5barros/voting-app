#!/bin/sh

celery -A lunch_voting worker -l info
