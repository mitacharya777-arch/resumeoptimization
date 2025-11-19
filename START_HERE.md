# 👋 START HERE - Beginner's Quick Start Guide

Welcome! This guide will get you up and running in **5 minutes**!

## 🎯 The Easiest Way (Recommended for Beginners)

### Method 1: Automatic Setup (Easiest!)

1. **Open Terminal**
   - Mac: Press `Cmd + Space`, type "Terminal"
   - Windows: Press `Win + R`, type "cmd"

2. **Go to your project folder:**
   ```bash
   cd Desktop/resumeoptimization
   ```

3. **Run the setup script:**
   ```bash
   python3 setup_easy.py
   ```
   
   Or if that doesn't work:
   ```bash
   python setup_easy.py
   ```

4. **That's it!** The script will:
   - ✅ Check Python installation
   - ✅ Install all dependencies
   - ✅ Set up the database
   - ✅ Create configuration files

5. **Start the app:**
   ```bash
   python3 app_db.py
   ```

6. **Open your browser:**
   ```
   http://localhost:5000
   ```

**Done!** 🎉

---

### Method 2: Manual Setup (If Method 1 doesn't work)

#### Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or:
```bash
pip install -r requirements.txt
```

#### Step 2: Set Database Type

**Mac/Linux:**
```bash
export DB_TYPE=sqlite
```

**Windows:**
```bash
set DB_TYPE=sqlite
```

#### Step 3: Run the App

```bash
python3 app_db.py
```

Or:
```bash
python app_db.py
```

#### Step 4: Open Browser

Go to: `http://localhost:5000`

---

## ❓ Common Questions

### Q: What is SQLite?
**A:** It's a simple database that doesn't need installation. Perfect for beginners!

### Q: Do I need to install PostgreSQL?
**A:** No! SQLite works great and requires zero setup.

### Q: Where is my data stored?
**A:** In a file called `resume_optimizer.db` in your project folder.

### Q: How do I backup my data?
**A:** Just copy the `resume_optimizer.db` file!

### Q: What if I get an error?
**A:** Check the error message. Common fixes:
- "python3 not found" → Try `python` instead
- "No module named flask" → Run `pip install -r requirements.txt`
- "Port 5000 in use" → Close other apps or change port

---

## 🆘 Need Help?

1. Check `BEGINNER_SETUP.md` for detailed step-by-step instructions
2. Check `TROUBLESHOOTING.md` for common problems
3. Look at the error message - it usually tells you what's wrong

---

## ✅ Quick Checklist

Before starting, make sure you have:
- [ ] Python installed (check with `python --version`)
- [ ] You're in the project folder
- [ ] You've run the setup script OR installed dependencies manually

---

## 🎓 What You'll See

When everything works, you'll see:
```
🚀 Starting Resume Optimizer with Database...
📱 Open http://localhost:5000 in your browser
✅ Database connection successful!
============================================================
🌐 Application URL: http://localhost:5000
============================================================
```

Then open that URL in your browser and you'll see the Resume Optimizer interface!

---

## 🚀 Ready?

Just run:
```bash
python3 setup_easy.py
```

Then:
```bash
python3 app_db.py
```

**That's it!** Good luck! 🎉

