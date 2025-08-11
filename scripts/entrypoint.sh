#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
until python -c "import asyncio; import asyncpg; asyncio.run(asyncpg.connect('$DATABASE_URL'))" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 1
done

echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
python -m autodev_agent.db.migrations

# Start the application
echo "Starting the application..."
exec "$@"
