# Groq API Setup Guide

## Step 1: Get Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy your API key (it looks like: `gsk_xxxxxxxxxxxxxxxxxxxxx`)

## Step 2: Install Groq Package

```bash
pip install groq
```

## Step 3: Set Your API Key

### Option A: Environment Variable (Recommended)

**On macOS/Linux:**
```bash
export GROQ_API_KEY=your_api_key_here
```

**On Windows:**
```cmd
set GROQ_API_KEY=your_api_key_here
```

### Option B: Create .env File (Better for persistence)

1. Create a file named `.env` in the project root:
```bash
touch .env
```

2. Add your API key to the file:
```
GROQ_API_KEY=your_api_key_here
```

3. The app will automatically load it (python-dotenv is already installed)

## Step 4: Verify Connection

Run this to test:
```bash
python3 -c "from utils.groq_optimizer import GroqResumeOptimizer; opt = GroqResumeOptimizer(); print('✅ Connected!' if opt.is_available() else '❌ Not connected. Check your API key.')"
```

## Step 5: Restart Your App

After setting the API key, restart the app:
```bash
python3 app_web.py
```

You should see:
- ✅ No "dummy data" warning
- ✅ Real AI-powered analysis
- ✅ Faster, more accurate results

## Troubleshooting

**Error: "groq package not installed"**
```bash
pip install groq
```

**Error: "Groq API not available"**
- Check that your API key is set: `echo $GROQ_API_KEY`
- Make sure the key starts with `gsk_`
- Verify the key is active in Groq console

**Still using dummy data?**
- Make sure you restarted the app after setting the API key
- Check the terminal output for any error messages

