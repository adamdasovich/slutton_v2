#!/bin/bash

echo "Running database migrations..."
python manage.py migrate --noinput

# Import data if RUN_IMPORT is set
if [ "$RUN_IMPORT" = "true" ]; then
    echo "RUN_IMPORT is true, importing data..."
    python import_on_railway.py
fi

echo "Starting gunicorn..."
exec gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
