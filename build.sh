#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
pip install gunicorn
python manage.py collectstatic --noinput  # Recolecta archivos estáticos
python manage.py migrate