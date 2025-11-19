# 🚀 Groq API Setup - Step by Step Guide

## Quick Setup (5 Minutes)

### Step 1: Get Your Groq API Key

1. **Visit Groq Console:**
   - Go to: **https://console.groq.com/**
   - Click **"Sign Up"** (or **"Log In"** if you already have an account)

2. **Create Account:**
   - Sign up with your email or Google account
   - Verify your email if required

3. **Navigate to API Keys:**
   - Once logged in, click on **"API Keys"** in the left sidebar
   - Or go directly to: **https://console.groq.com/keys**

4. **Create New API Key:**
   - Click **"Create API Key"** button
   - Give it a name (e.g., "Resume Optimizer")
   - Click **"Submit"** or **"Create"**

5. **Copy Your Key:**
   - Your API key will appear (starts with `gsk_...`)
   - **IMPORTANT:** Copy it immediately - you won't be able to see it again!
   - It looks like: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### Step 2: Install Groq Package

Open your terminal and run:

```bash
pip install groq
```

Or if you're using Python 3 specifically:

```bash
pip3 install groq
```

**Verify installation:**
```bash
python3 -c "import groq; print('✅ Groq installed successfully!')"
```

---

### Step 3: Set Your API Key

**Choose ONE method:**

#### Method A: Environment Variable (Quick Test)

**On macOS/Linux:**
```bash
export GROQ_API_KEY=your_api_key_here
```

**On Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

⚠️ **Note:** This only works for the current terminal session. When you close the terminal, you'll need to set it again.

---

#### Method B: .env File (Recommended - Permanent)

1. **Create a `.env` file** in your project folder:
   ```bash
   cd /Users/mitacharya/Desktop/resumeoptimization
   touch .env
   ```

2. **Add your API key to the file:**
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```
   
   Or manually edit the file and add:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

3. **Make sure `.env` is in `.gitignore`** (so you don't accidentally share your key):
   ```bash
   echo ".env" >> .gitignore
   ```

---

### Step 4: Verify Setup

Test if everything is working:

```bash
python3 -c "
from utils.groq_optimizer import GroqResumeOptimizer
from dotenv import load_dotenv
import os

load_dotenv()
opt = GroqResumeOptimizer()

if opt.is_available():
    print('✅ SUCCESS! Groq API is connected!')
    print(f'✅ Using API key: {opt.api_key[:10]}...')
else:
    print('❌ Not connected. Check your API key.')
"
```

---

### Step 5: Restart Your App

After setting the API key, restart your app:

```bash
# Stop the current app (Ctrl+C if running)
# Then start it again:
python3 app_web.py
```

**You should see:**
```
✅ Groq API Connected - Using real AI analysis!
```

Instead of:
```
⚠️  Using dummy data (no Groq API key)
```

---

## ✅ Verification Checklist

- [ ] Groq account created at console.groq.com
- [ ] API key created and copied
- [ ] Groq package installed (`pip install groq`)
- [ ] API key set in `.env` file or environment variable
- [ ] App restarted and shows "Groq API Connected"

---

## 🎯 Quick Command Summary

```bash
# 1. Install Groq
pip3 install groq

# 2. Create .env file with your key
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Test connection
python3 -c "from utils.groq_optimizer import GroqResumeOptimizer; from dotenv import load_dotenv; import os; load_dotenv(); opt = GroqResumeOptimizer(); print('✅ Connected!' if opt.is_available() else '❌ Not connected')"

# 4. Run app
python3 app_web.py
```

---

## 🔍 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'groq'"
**Solution:**
```bash
pip3 install groq
```

### Problem: "Groq API not available"
**Solution:**
1. Check your API key is correct: `echo $GROQ_API_KEY` (or check `.env` file)
2. Make sure the key starts with `gsk_`
3. Verify the key is active in Groq console
4. Restart your app after setting the key

### Problem: "Still using dummy data"
**Solution:**
1. Make sure you restarted the app after setting the API key
2. Check the terminal output for error messages
3. Verify `.env` file is in the same folder as `app_web.py`
4. Try setting it as environment variable instead

### Problem: API key not found
**Solution:**
- Make sure `.env` file is in the project root (same folder as `app_web.py`)
- Check the file has exactly: `GROQ_API_KEY=your_key_here` (no spaces around `=`)
- Make sure you saved the file

---

## 💡 Tips

1. **Free Tier:** Groq offers free API access with generous limits
2. **Rate Limits:** Free tier has rate limits, but should be fine for personal use
3. **Security:** Never share your API key or commit it to Git
4. **Backup:** Save your API key in a password manager

---

## 📞 Need Help?

If you encounter issues:
1. Check the terminal output for error messages
2. Verify your API key at https://console.groq.com/keys
3. Make sure the Groq package is installed: `pip3 list | grep groq`
4. Try the verification command above

---

## 🎉 You're Done!

Once set up, your app will use **real AI-powered analysis** instead of dummy data, providing:
- More accurate match scores
- Better content suggestions
- Real optimization improvements
- Faster and smarter analysis

Happy optimizing! 🚀

