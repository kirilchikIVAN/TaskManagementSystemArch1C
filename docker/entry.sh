#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# Init db values
# TODO: add script here

# Start server
echo "Starting server"
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
