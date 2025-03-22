#!/bin/bash
set -e

echo "Waiting for database to be ready..."
/app/scripts/wait-for-it.sh ${DB_HOST}:3306 -s -t 30

echo "Running database migrations..."
flask db upgrade

echo "Starting application with gunicorn..."
exec gunicorn --chdir /app app.app:app --workers 4 --bind 0.0.0.0:5000
