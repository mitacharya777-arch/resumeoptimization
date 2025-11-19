#!/bin/bash
# Start All Services for Production

echo "🚀 Starting Production Services..."
echo "===================================="

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed!"
    echo "   Install: brew install redis (Mac) or sudo apt-get install redis (Linux)"
    exit 1
fi

# Start Redis in background
echo "🔴 Starting Redis..."
redis-server --daemonize yes
sleep 2

# Check if Redis started
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis started successfully"
else
    echo "❌ Failed to start Redis"
    exit 1
fi

# Start Celery worker in background
echo "⚙️  Starting Celery Worker..."
celery -A config.celery_config worker \
    --loglevel=info \
    --concurrency=10 \
    --detach \
    --logfile=celery.log \
    --pidfile=celery.pid

sleep 2
echo "✅ Celery worker started"

# Start Flask app
echo "🌐 Starting Flask Application..."
echo ""
python app_recruiter_production.py

