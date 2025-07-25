#!/usr/bin/env bash
set -o errexit

pip install --user gunicorn
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python -m gunicorn --version  # Debe mostrar la versión