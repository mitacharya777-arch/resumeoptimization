# Run Project Locally - Step by Step Guide

Follow these steps to run the Resume Optimizer on your computer!

## 🎯 Option 1: Demo Mode (EASIEST - No Database!)

Perfect for seeing how it looks and works!

### Step 1: Open Terminal

**Mac:**
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

**Windows:**
- Press `Win + R`
- Type "cmd"
- Press Enter

### Step 2: Go to Project Folder

Type this command and press Enter:

```bash
cd Desktop/resumeoptimization
```

**Verify you're in the right place:**
```bash
pwd
```

Should show: `/Users/mitacharya/Desktop/resumeoptimization`

### Step 3: Check Python

```bash
python3 --version
```

Should show Python 3.8 or higher. If not, try:
```bash
python --version
```

### Step 4: Install Dependencies

```bash
pip3 install flask flask-cors
```

Or if that doesn't work:
```bash
pip install flask flask-cors
```

**Wait for installation to complete!**

### Step 5: Run Demo App

```bash
python3 app_demo.py
```

Or:
```bash
python app_demo.py
```

### Step 6: Look for This Message

You should see:
```
🎨 Starting Resume Optimizer - DEMO MODE
📱 Open http://localhost:5000 in your browser
💡 This is a demo with dummy data - no database needed!

============================================================
🌐 Application URL: http://localhost:5000
============================================================

 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 7: Open Browser

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: **http://localhost:5000**
3. You should see the Resume Optimizer interface!

**🎉 Done!** You're now running the app!

---

## 🎯 Option 2: Full Version with Database (SQLite)

If you want to save data and use all features:

### Step 1-3: Same as above

### Step 4: Install All Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 5: Set Database Type

```bash
export DB_TYPE=sqlite
```

**Windows users:**
```bash
set DB_TYPE=sqlite
```

### Step 6: Run Full App

```bash
python3 app_db.py
```

### Step 7: Open Browser

Go to: **http://localhost:5000**

---

## 🆘 Troubleshooting

### Problem: "python3: command not found"

**Solution:**
```bash
python app_demo.py
```
(Use `python` instead of `python3`)

### Problem: "No module named 'flask'"

**Solution:**
```bash
pip3 install flask flask-cors
```

Or:
```bash
pip install flask flask-cors
```

### Problem: "Port 5000 already in use"

**Solution:**
1. Find what's using it:
   ```bash
   lsof -i :5000
   ```
2. Kill the process, or
3. Change port in the code to 5001

### Problem: "Permission denied"

**Solution:**
Make sure you're in the right folder:
```bash
cd Desktop/resumeoptimization
pwd  # Check current folder
```

### Problem: Can't find the folder

**Solution:**
1. Open Finder (Mac) or File Explorer (Windows)
2. Go to Desktop
3. Find `resumeoptimization` folder
4. Right-click → "Open in Terminal" (Mac) or "Open PowerShell here" (Windows)

---

## ✅ Quick Checklist

Before running, make sure:
- [ ] You're in the project folder (`Desktop/resumeoptimization`)
- [ ] Python is installed (`python3 --version` works)
- [ ] Flask is installed (`pip3 install flask`)
- [ ] Terminal is open and ready

---

## 🚀 Quick Start Commands

**For Demo (Easiest):**
```bash
cd Desktop/resumeoptimization
pip3 install flask flask-cors
python3 app_demo.py
```
Then open: http://localhost:5000

**For Full Version:**
```bash
cd Desktop/resumeoptimization
pip3 install -r requirements.txt
export DB_TYPE=sqlite
python3 app_db.py
```
Then open: http://localhost:5000

---

## 📝 What You'll See

When it works, you'll see:
- Beautiful sidebar navigation
- Dashboard with statistics
- Resumes tab (with sample data in demo mode)
- Jobs tab (with sample data in demo mode)
- Optimize tab (to optimize resumes)
- History tab (to see past optimizations)

---

## 🎓 Next Steps

1. **Explore the UI** - Click around and see all features
2. **Try optimizing** - Select a resume and job, click Optimize
3. **View results** - See match scores and suggestions
4. **Read the docs** - Check README.md for more info

---

## 💡 Pro Tips

- **Start with demo mode** - Easiest way to see everything
- **Keep terminal open** - The app runs in the terminal
- **Check terminal for errors** - If something doesn't work, look at terminal output
- **Use Ctrl+C** - To stop the app when you're done

---

**Ready? Let's go!** 🚀

