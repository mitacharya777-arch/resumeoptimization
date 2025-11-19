#!/bin/bash
# Start Celery Worker for Production

echo "🚀 Starting Celery Worker..."
echo "================================"

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running!"
    echo "   Please start Redis first: redis-server"
    exit 1
fi

echo "✅ Redis is running"
echo ""

# Start Celery worker
celery -A config.celery_config worker \
    --loglevel=info \
    --concurrency=10 \
    --max-tasks-per-child=50 \
    --time-limit=300 \
    --soft-time-limit=270

