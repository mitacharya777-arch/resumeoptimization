#!/bin/bash
# Start Redis Server

echo "🔴 Starting Redis Server..."
echo "================================"

# Check if Redis is already running
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is already running"
    exit 0
fi

# Start Redis
redis-server

