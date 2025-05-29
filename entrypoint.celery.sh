#!/bin/sh

echo "Starting Celery worker..."
exec poetry run celery -A config worker --loglevel=info
