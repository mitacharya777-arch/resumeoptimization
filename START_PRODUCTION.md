# 🚀 Start Production System - Quick Guide

## Prerequisites

1. **Install Redis:**
   ```bash
   # macOS
   brew install redis
   
   # Linux
   sudo apt-get install redis-server
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Start Services

### Option 1: Automatic (Easiest) ✅

```bash
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

This will:
- Start Redis
- Start Celery worker
- Start Flask app

### Option 2: Manual (3 Terminals)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Celery Worker:**
```bash
celery -A config.celery_config worker --loglevel=info --concurrency=10
```

**Terminal 3 - Flask App:**
```bash
python app_recruiter_production.py
```

## Verify It's Working

1. **Check Health:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Check Stats:**
   ```bash
   curl http://localhost:5000/api/recruiter/stats
   ```

3. **Open Dashboard:**
   ```
   http://localhost:5000
   ```

## Test Optimization

```bash
curl -X POST http://localhost:5000/api/recruiter/optimize/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_ids": [1, 2, 3],
    "job_id": 1
  }'
```

This returns a `task_id`. Check status:
```bash
curl http://localhost:5000/api/recruiter/tasks/{task_id}
```

## Troubleshooting

### Redis Not Running
```bash
redis-cli ping
# Should return: PONG

# If not:
redis-server
```

### Celery Worker Not Starting
```bash
# Check if Redis is running first
redis-cli ping

# Then start worker
celery -A config.celery_config worker --loglevel=info
```

### Port Already in Use
The app automatically finds a free port. Check the console output for the actual port number.

## Next Steps

- Read `PRODUCTION_SETUP.md` for detailed configuration
- Read `PRODUCTION_READY.md` for full documentation
- Check `SCALABILITY_ANALYSIS.md` for performance details

---

**You're ready to process 1000+ resumes/day!** 🎉

