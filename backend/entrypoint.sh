#!/bin/bash

echo "Running database migrations..."
python manage.py migrate --noinput

# Generate trivia for next 7 days (if not already exists)
echo "Generating trivia for the next 7 days..."
python manage.py generate_trivia_week --days 7 || echo "Trivia generation skipped"

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

echo "Starting Daphne (ASGI server for WebSocket support)..."
echo "PORT is set to: $PORT"
# Use PORT from Railway, default to 8000 if not set
PORT=${PORT:-8000}
echo "Using PORT: $PORT"
exec daphne -b 0.0.0.0 -p $PORT slutton_backend.asgi:application
