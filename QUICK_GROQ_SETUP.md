# Quick Groq API Setup

## 🚀 3 Simple Steps

### Step 1: Install Groq Package
```bash
pip install groq
```

### Step 2: Get Your API Key
1. Go to: **https://console.groq.com/**
2. Sign up / Log in
3. Go to "API Keys"
4. Create new key
5. Copy it (starts with `gsk_...`)

### Step 3: Set Your API Key

**Option A: Quick Test (Terminal Session Only)**
```bash
export GROQ_API_KEY=your_api_key_here
python3 app_web.py
```

**Option B: Permanent (.env file)**
```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
python3 app_web.py
```

## ✅ Verify It's Working

After starting the app, you should see:
- ✅ No "dummy data" warning
- ✅ Real AI analysis (not sample data)
- ✅ Faster, more accurate results

## 🔍 Check Connection Status

Run this command:
```bash
python3 -c "from utils.groq_optimizer import GroqResumeOptimizer; opt = GroqResumeOptimizer(); print('✅ Connected!' if opt.is_available() else '❌ Not connected')"
```

## 📝 Example

```bash
# 1. Install
pip install groq

# 2. Set key
export GROQ_API_KEY=gsk_your_actual_key_here

# 3. Run app
python3 app_web.py
```

That's it! 🎉

