#!/bin/bash
set -e

# Wait for PostgreSQL
while ! pg_isready -h postgres-master -p 5432 -U admin -d appdb; do
  echo "Waiting for PostgreSQL master..."
  sleep 2
done

# Apply core migrations first
python manage.py migrate accounts --no-input
python manage.py migrate contenttypes --no-input
python manage.py migrate auth --no-input
python manage.py migrate admin --no-input
python manage.py migrate sessions --no-input

# Then apply your app migrations
python manage.py migrate --no-input

# Start server
exec uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 4
