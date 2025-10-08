#!/bin/bash

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
exec gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
