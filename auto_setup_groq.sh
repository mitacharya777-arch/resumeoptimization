#!/bin/bash

echo "=========================================="
echo "🤖 Automated Groq API Setup"
echo "=========================================="
echo ""

# Step 1: Install groq package
echo "📦 Step 1: Installing groq package..."
if pip3 install groq --quiet 2>/dev/null; then
    echo "✅ Groq package installed successfully"
else
    echo "⚠️  Installing groq package (this may take a moment)..."
    pip3 install groq
    echo "✅ Groq package installed"
fi

echo ""
echo "=========================================="
echo "🔑 Step 2: API Key Setup"
echo "=========================================="
echo ""

# Check if API key is already set
if [ -f .env ] && grep -q "GROQ_API_KEY" .env; then
    echo "✅ Found existing API key in .env file"
    echo ""
    echo "Current setup:"
    grep "GROQ_API_KEY" .env | sed 's/GROQ_API_KEY=.*/GROQ_API_KEY=***hidden***/'
    echo ""
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ Keeping existing API key"
        echo ""
        echo "=========================================="
        echo "✅ Setup Complete!"
        echo "=========================================="
        echo ""
        echo "Your app is ready! Run:"
        echo "  python3 app_web.py"
        exit 0
    fi
fi

# Check if API key is in environment
if [ ! -z "$GROQ_API_KEY" ]; then
    echo "✅ Found API key in environment variable"
    echo "GROQ_API_KEY=$GROQ_API_KEY" > .env
    echo "✅ Saved to .env file"
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Your app is ready! Run:"
    echo "  python3 app_web.py"
    exit 0
fi

# Ask for API key
echo "To complete setup, you need a Groq API key."
echo ""
echo "📝 Get your API key:"
echo "   1. Visit: https://console.groq.com/"
echo "   2. Sign up / Log in"
echo "   3. Go to 'API Keys' section"
echo "   4. Create new key"
echo "   5. Copy the key (starts with 'gsk_...')"
echo ""
read -p "Enter your Groq API key (or press Enter to skip): " api_key

if [ ! -z "$api_key" ]; then
    echo "GROQ_API_KEY=$api_key" > .env
    echo "✅ API key saved to .env file"
    echo ""
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Your app is ready! Run:"
    echo "  python3 app_web.py"
else
    echo ""
    echo "⚠️  No API key provided"
    echo ""
    echo "You can set it later by:"
    echo "  1. Creating .env file: echo 'GROQ_API_KEY=your_key' > .env"
    echo "  2. Or setting environment: export GROQ_API_KEY=your_key"
    echo ""
    echo "The app will work with dummy data until you set the key."
fi

echo ""

