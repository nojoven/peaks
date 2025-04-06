#!/bin/sh
# entrypoint.sh

echo "Running Alembic migrations..."
alembic -c /peaks/alembic.ini upgrade head

echo "Starting API with Uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
