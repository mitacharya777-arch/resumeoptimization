#!/bin/bash
# Start the Beautiful UI App

echo "🚀 Starting Resume Optimizer..."
echo "================================"

# Kill any existing processes on port 5000
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# Wait a moment
sleep 1

# Start the app
python3 app_recruiter_ui.py
