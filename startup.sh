#!/bin/bash

# Azure Web App Startup Script for Flask Application
echo "Starting Resume Optimizer on Azure..."

# Install dependencies if needed
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Use Gunicorn as production WSGI server
# Workers: 2 (good for small Azure instances)
# Timeout: 120 seconds (for resume processing)
# Bind to PORT environment variable (Azure sets this)
echo "Starting Gunicorn server..."
gunicorn --bind=0.0.0.0:${PORT:-8000} --workers=2 --timeout=120 app_web:app
