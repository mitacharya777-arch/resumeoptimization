# Troubleshooting Guide

## Common Errors and Solutions

### Error: "Port 5000 is in use"

**Solution:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use the startup script
./start.sh
```

The app automatically finds a free port, so check the console output for the actual port number.

---

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install flask flask-cors
```

---

### Error: "ModuleNotFoundError: No module named 'groq'"

**This is OK!** The app works with dummy data without Groq. You'll see a warning but it still works.

To use real Groq API:
```bash
pip install groq
export GROQ_API_KEY=your_key_here
```

---

### Error: "Address already in use" or "403 Forbidden"

**Solution:**
This is usually AirPlay Receiver on macOS using port 5000.

**Option 1:** Use the startup script (automatically finds free port):
```bash
./start.sh
```

**Option 2:** Disable AirPlay Receiver:
- System Preferences → General → AirDrop & Handoff
- Turn off "AirPlay Receiver"

---

### Error: "Connection refused"

**Solution:**
1. Make sure the app is running
2. Check the console output for the actual port number
3. Use `127.0.0.1` instead of `localhost`:
   ```bash
   curl http://127.0.0.1:5004/api/health
   ```

---

## Quick Test

Run this to verify everything works:
```bash
python3 test_app.py
```

If all tests pass, the app is working correctly!

---

## Still Having Issues?

1. **Check the error message** - What exactly does it say?
2. **Check the console output** - What port is the app running on?
3. **Test with curl:**
   ```bash
   curl http://127.0.0.1:PORT/api/health
   ```
   (Replace PORT with the actual port from console)

4. **Share the error message** so I can help fix it!

---

## Working Example

```bash
# Start app
python3 app_resume_analyzer.py

# In another terminal, test it:
curl -X POST http://localhost:5004/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\nPython",
    "job_description": "Senior Software Engineer with React"
  }'
```

---

**Please share the exact error message you're seeing so I can help fix it!**
