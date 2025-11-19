#!/bin/bash
# Quick start script - Run this to start the app!

echo "🚀 Starting Resume Optimizer..."
echo ""

# Check if we're in the right directory
if [ ! -f "app_demo.py" ]; then
    echo "❌ Error: app_demo.py not found!"
    echo "   Make sure you're in the resumeoptimization folder"
    echo "   Run: cd Desktop/resumeoptimization"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found!"
    exit 1
fi

echo "✅ Using: $PYTHON_CMD"
echo ""

# Run the demo app
echo "🎨 Starting Demo Mode..."
echo ""
echo "📱 The app will show you the URL to open in your browser"
echo "   (Usually http://localhost:5001 or similar)"
echo ""
echo "Press Ctrl+C to stop the server when you're done"
echo ""
echo "─────────────────────────────────────────────────────────"
echo ""

$PYTHON_CMD app_demo.py

