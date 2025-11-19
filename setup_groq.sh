#!/bin/bash

echo "=========================================="
echo "🔧 Groq API Setup Script"
echo "=========================================="
echo ""

# Check if groq is installed
if python3 -c "import groq" 2>/dev/null; then
    echo "✅ Groq package is installed"
else
    echo "📦 Installing groq package..."
    pip3 install groq
    echo "✅ Groq package installed"
fi

echo ""
echo "=========================================="
echo "📝 API Key Setup"
echo "=========================================="
echo ""
echo "To set your Groq API key, choose one option:"
echo ""
echo "Option 1: Set environment variable (temporary)"
echo "  export GROQ_API_KEY=your_api_key_here"
echo ""
echo "Option 2: Create .env file (persistent)"
echo "  echo 'GROQ_API_KEY=your_api_key_here' > .env"
echo ""
echo "Get your API key from: https://console.groq.com/"
echo ""
read -p "Do you want to set your API key now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your Groq API key: " api_key
    if [ ! -z "$api_key" ]; then
        echo "GROQ_API_KEY=$api_key" > .env
        echo "✅ API key saved to .env file"
        echo ""
        echo "Now restart your app:"
        echo "  python3 app_web.py"
    else
        echo "❌ No API key provided"
    fi
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="

