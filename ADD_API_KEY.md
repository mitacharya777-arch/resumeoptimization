# 🔑 Add Your Groq API Key

## ✅ Step 1: Groq Package - DONE!
The groq package is already installed! ✅

## 🔑 Step 2: Get Your API Key

1. **Open this link:** https://console.groq.com/
2. **Sign up** (if you don't have an account) or **Log in**
3. Click on **"API Keys"** in the menu
4. Click **"Create API Key"**
5. **Copy the key** (it starts with `gsk_...`)

## ⚡ Step 3: Add Your Key (Choose One Method)

### Method 1: Quick Command (Easiest!)
Just run this command and paste your key when asked:
```bash
./auto_setup_groq.sh
```

### Method 2: One-Line Command
Replace `your_key_here` with your actual API key:
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

### Method 3: Manual .env File
1. Create a file named `.env` in this folder
2. Add this line (replace with your actual key):
```
GROQ_API_KEY=gsk_your_actual_key_here
```

## ✅ Step 4: Done!
After adding your key, just run:
```bash
python3 app_web.py
```

The app will automatically use Groq AI! 🚀

