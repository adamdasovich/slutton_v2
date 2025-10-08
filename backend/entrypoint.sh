#!/bin/bash

echo "Running database migrations..."
python manage.py migrate --noinput

# Import data if RUN_IMPORT is set
if [ "$RUN_IMPORT" = "true" ]; then
    echo "RUN_IMPORT is true, importing data..."
    python import_on_railway.py
fi

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser if it doesn't exist..."
    python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" 2>/dev/null || echo "Superuser already exists or creation skipped"
fi

echo "Starting gunicorn..."
exec gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
