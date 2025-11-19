#!/bin/bash
# Simple startup script for Resume Analyzer

echo "🚀 Starting Resume Analyzer API..."
echo ""

# Kill any existing processes on common ports
for port in 5000 5001 5002 5003 5004 5005; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done

sleep 1

# Start the app
python3 app_resume_analyzer.py

