#!/bin/sh

echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=3 --timeout=120 --log-level=debug
