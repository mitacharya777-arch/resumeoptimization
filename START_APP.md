# 🚀 Start the Beautiful UI - Quick Guide

## Option 1: Production App (Recommended - Beautiful New UI) ✨

### Start the app:
```bash
python app_recruiter_production.py
```

### Access the dashboard:
```
http://localhost:5000
```

**Note:** The app will automatically find a free port if 5000 is busy. Check the console output for the actual URL.

---

## Option 2: Demo App (No Redis/Celery needed)

If you just want to see the UI without setting up Redis/Celery:

```bash
python app_recruiter_demo.py
```

Then open: `http://localhost:5000`

---

## What You'll See

✨ **Beautiful Modern UI** with:
- Dark theme with gradient accents
- Smooth animations
- Modern icons
- Professional design
- Interactive elements

---

## Quick Start Commands

**Terminal 1 - Start Flask App:**
```bash
cd /Users/mitacharya/Desktop/resumeoptimization
python app_recruiter_production.py
```

**Terminal 2 - Start Redis (if using production):**
```bash
redis-server
```

**Terminal 3 - Start Celery Worker (if using production):**
```bash
celery -A config.celery_config worker --loglevel=info --concurrency=10
```

---

## Access URLs

Once started, you'll see output like:
```
🚀 Production Recruiter Tool - Starting...
============================================================
📊 Monitoring: http://localhost:5000/api/recruiter/stats
❤️  Health: http://localhost:5000/api/health
📱 Dashboard: http://localhost:5000/
============================================================
```

**Main Dashboard:** `http://localhost:5000`  
**Health Check:** `http://localhost:5000/api/health`  
**Statistics:** `http://localhost:5000/api/recruiter/stats`

---

## Troubleshooting

### Port Already in Use?
The app automatically finds a free port. Check the console output.

### Redis Not Running?
For demo mode, you don't need Redis. For production:
```bash
redis-server
```

### Can't Access?
Make sure the app is running and check the console for the actual port number.

---

**Ready! Open http://localhost:5000 in your browser** 🎉
