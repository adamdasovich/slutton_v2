#!/bin/bash

echo "Running database migrations..."
python manage.py migrate --noinput

# Import data if RUN_IMPORT is set
if [ "$RUN_IMPORT" = "true" ]; then
    echo "RUN_IMPORT is true, importing data..."
    python import_on_railway.py
fi

# Reset/create superuser password if RUN_PASSWORD_RESET is set
if [ "$RUN_PASSWORD_RESET" = "true" ]; then
    echo "Resetting superuser password..."
    python reset_superuser.py
fi

echo "Starting gunicorn..."
echo "PORT is set to: $PORT"
# Use PORT from Railway, default to 8000 if not set
PORT=${PORT:-8000}
echo "Using PORT: $PORT"
exec gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
