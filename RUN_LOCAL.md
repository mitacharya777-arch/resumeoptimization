# 🚀 Run Locally - Quick Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

## Step 3: Start Services

### Option A: Automatic (Easiest) ✅

```bash
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

### Option B: Manual (3 Terminals)

**Terminal 1 - Start Redis:**
```bash
redis-server
```

**Terminal 2 - Start Celery Worker:**
```bash
celery -A config.celery_config worker --loglevel=info --concurrency=10
```

**Terminal 3 - Start Flask App:**
```bash
python app_recruiter_production.py
```

## Step 4: Access the Application

Once started, the app will show you the URL. Typically:

### 🌐 Main Dashboard:
```
http://localhost:5000
```

### 📊 Health Check:
```
http://localhost:5000/api/health
```

### 📈 Statistics:
```
http://localhost:5000/api/recruiter/stats
```

---

## Quick Test

### Test Health:
```bash
curl http://localhost:5000/api/health
```

### Test Bulk Optimize:
```bash
curl -X POST http://localhost:5000/api/recruiter/optimize/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_ids": [1, 2, 3],
    "job_id": 1
  }'
```

---

## Troubleshooting

### Port Already in Use?
The app automatically finds a free port. Check the console output for the actual port number.

### Redis Not Running?
```bash
redis-cli ping
# If not PONG, start Redis:
redis-server
```

### Celery Worker Not Starting?
Make sure Redis is running first, then:
```bash
celery -A config.celery_config worker --loglevel=info
```

---

## Alternative: Demo Mode (No Redis/Celery Needed)

If you just want to see the UI without setting up Redis/Celery:

```bash
python app_recruiter_demo.py
```

Then access: `http://localhost:5000`

---

## 📝 Notes

- The production app uses **async processing** (requires Redis + Celery)
- The demo app uses **synchronous processing** (no setup needed)
- For 1000+ resumes/day, use the production app
- For testing/development, either works

---

**Ready! Open http://localhost:5000 in your browser** 🎉

