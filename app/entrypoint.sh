#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting application with gunicorn..."
exec gunicorn --chdir /app app.app:app --workers 4 --bind 0.0.0.0:5000
