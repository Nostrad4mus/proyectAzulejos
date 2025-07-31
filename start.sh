#!/usr/bin/env bash
set -o errexit

# pip install -r requirements.txt
python manage.py collectstatic --noinput
gunicorn tu_proyecto.wsgi --bind 0.0.0.0:10000