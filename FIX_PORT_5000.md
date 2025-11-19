# Fix Port 5000 Issue on macOS

## Problem: Port 5000 Already in Use

On macOS, port 5000 is often used by **AirPlay Receiver**. This is a common issue!

## ✅ Solution 1: Use Different Port (EASIEST - Already Fixed!)

The app now **automatically finds an available port**! Just run:

```bash
python3 app_demo.py
```

It will automatically use port 5001, 5002, etc. if 5000 is busy.

**Look for this message:**
```
⚠️  Port 5000 is in use, using port 5001 instead
🌐 Application URL: http://localhost:5001
```

Then open: **http://localhost:5001** (or whatever port it shows)

---

## ✅ Solution 2: Disable AirPlay Receiver (Optional)

If you want to use port 5000 specifically:

1. **Open System Preferences**
   - Click Apple menu → System Preferences

2. **Go to General**
   - Click "General" in System Preferences

3. **Find AirDrop & Handoff**
   - Scroll down to "AirDrop & Handoff" section

4. **Turn off AirPlay Receiver**
   - Uncheck "AirPlay Receiver"
   - This will free up port 5000

5. **Restart the app**
   ```bash
   python3 app_demo.py
   ```

---

## ✅ Solution 3: Kill Process Using Port 5000

Find and kill the process:

```bash
# Find what's using port 5000
lsof -i :5000

# Kill it (replace PID with the number from above)
kill -9 <PID>
```

---

## 🎯 Recommended: Just Use Auto Port Selection!

The app now automatically finds an available port, so you don't need to do anything!

Just run:
```bash
python3 app_demo.py
```

And use whatever port it shows in the message!

---

## Quick Test

Run the app and look for:
```
🌐 Application URL: http://localhost:XXXX
```

Then open that URL in your browser!

