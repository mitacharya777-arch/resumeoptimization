# Beginner's Guide: Database Setup (Super Easy!)

Don't worry! This is much easier than it sounds. Follow these steps one by one.

## 🎯 Option 1: SQLite (EASIEST - Recommended for Beginners!)

SQLite requires **ZERO installation** - it's built into Python!

### Step-by-Step Instructions:

#### Step 1: Open Terminal

- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Press `Win + R`, type "cmd", press Enter
- **Linux**: Press `Ctrl + Alt + T`

#### Step 2: Go to Your Project Folder

Type this command (press Enter after each line):

```bash
cd Desktop/resumeoptimization
```

**What this does:** This takes you to your project folder.

#### Step 3: Set Database Type to SQLite

Type this command:

```bash
export DB_TYPE=sqlite
```

**What this does:** Tells the app to use SQLite (the easy database).

**Note for Windows users:** Use this instead:
```bash
set DB_TYPE=sqlite
```

#### Step 4: Run the App!

Type this command:

```bash
python3 app_db.py
```

**Or if that doesn't work, try:**
```bash
python app_db.py
```

#### Step 5: You're Done! 🎉

You should see:
```
🚀 Starting Resume Optimizer with Database...
📱 Open http://localhost:5000 in your browser
✅ Database connection successful!
```

#### Step 6: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

**That's it!** The database file (`resume_optimizer.db`) will be created automatically in your project folder.

---

## 🎯 Option 2: PostgreSQL (If You Need It Later)

Only use this if you specifically need PostgreSQL. SQLite is usually enough!

### Step 1: Install PostgreSQL

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
1. Download from: https://www.postgresql.org/download/windows/
2. Run the installer
3. Follow the installation wizard
4. Remember the password you set!

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

Open terminal and type:

```bash
createdb resume_optimizer
```

**If that doesn't work, try:**
```bash
psql postgres
```

Then inside psql, type:
```sql
CREATE DATABASE resume_optimizer;
\q
```

### Step 3: Set Environment Variables

**Mac/Linux:**
```bash
export DB_TYPE=postgresql
export DB_USER=postgres
export DB_PASSWORD=your_password_here
export DB_NAME=resume_optimizer
```

**Windows:**
```bash
set DB_TYPE=postgresql
set DB_USER=postgres
set DB_PASSWORD=your_password_here
set DB_NAME=resume_optimizer
```

### Step 4: Run Setup Script

```bash
python3 setup_database.py
```

### Step 5: Run the App

```bash
python3 app_db.py
```

---

## 🆘 Troubleshooting for Beginners

### Problem: "python3: command not found"

**Solution:** Try `python` instead of `python3`:
```bash
python app_db.py
```

### Problem: "No module named 'flask'"

**Solution:** Install dependencies:
```bash
pip3 install -r requirements.txt
```

Or:
```bash
pip install -r requirements.txt
```

### Problem: "Permission denied"

**Solution:** Make sure you're in the right folder:
```bash
cd Desktop/resumeoptimization
pwd  # This shows your current folder
```

### Problem: "Port 5000 already in use"

**Solution:** Something else is using port 5000. Close other apps or change the port in `app_db.py` (line 497) to `5001`.

### Problem: Can't find the project folder

**Solution:** 
1. Open Finder (Mac) or File Explorer (Windows)
2. Go to Desktop
3. Find the `resumeoptimization` folder
4. Right-click and "Open in Terminal" (Mac) or "Open PowerShell here" (Windows)

---

## ✅ Quick Checklist

Before running the app, make sure:

- [ ] You're in the project folder (`Desktop/resumeoptimization`)
- [ ] You've set `DB_TYPE=sqlite` (for easiest setup)
- [ ] You've installed dependencies: `pip install -r requirements.txt`
- [ ] You have Python installed (check with `python --version`)

---

## 🎓 What Happens Behind the Scenes?

When you run the app with SQLite:
1. A file called `resume_optimizer.db` is created in your project folder
2. This file stores all your resumes, job descriptions, and optimizations
3. You can see this file in your project folder
4. To backup, just copy this file!

---

## 💡 Pro Tips for Beginners

1. **Start with SQLite** - It's the easiest and works great for learning
2. **Don't worry about PostgreSQL** - You can learn it later if needed
3. **The database file is safe** - It's just a file on your computer
4. **To reset everything** - Just delete `resume_optimizer.db` and run the app again

---

## 🚀 Ready to Start?

Just follow Option 1 (SQLite) above - it's super simple!

If you get stuck, check the error message and look it up, or ask for help!

Good luck! 🎉

