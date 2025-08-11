#!/bin/bash

# Development script for AI Coder Agent

set -e

echo "Starting AI Coder Agent development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start PostgreSQL
echo "Starting PostgreSQL..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U ai_coder_user -d ai_coder_db; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

# Start Redis
echo "Starting Redis..."
docker-compose up -d redis

# Start OpenTelemetry Collector
echo "Starting OpenTelemetry Collector..."
docker-compose up -d otel-collector

# Start Prometheus
echo "Starting Prometheus..."
docker-compose up -d prometheus

# Start Grafana
echo "Starting Grafana..."
docker-compose up -d grafana

# Start Jaeger
echo "Starting Jaeger..."
docker-compose up -d jaeger

# Start backend
echo "Starting backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn autodev_agent.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo "Development environment started successfully!"
echo "Backend running at: http://localhost:8000"
echo "Frontend running at: http://localhost:5173"
echo "Grafana running at: http://localhost:3000"
echo "Jaeger running at: http://localhost:16686"

# Wait for interrupt
trap "echo 'Stopping development environment...'; kill $BACKEND_PID $FRONTEND_PID; docker-compose down" INT
wait