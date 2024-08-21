#!/bin/sh

export DJANGO_SUPERUSER_PASSWORD='25733034'
echo DJANGO_SUPERUSER_PASSWORD
echo "PostgreSQL started"
python manage.py migrate
python manage.py createsuperuser --email=jhocce3022@hotmail.com --noinput
exec "$@"