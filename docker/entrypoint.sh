#!/bin/bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding data..."
python -m migrations.seed.gen_seed_data

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
