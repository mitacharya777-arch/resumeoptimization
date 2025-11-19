# Production Setup Guide - Scalable System for 1000+ Resumes/Day

## Overview

This production-ready system includes:
- ✅ **Async Processing** (Celery + Redis)
- ✅ **Caching** (Redis)
- ✅ **Rate Limiting** (Flask-Limiter)
- ✅ **Monitoring** (Prometheus metrics)
- ✅ **Database Indexes** (Optimized queries)
- ✅ **Error Handling** (Retries, logging)

---

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
```

**Windows:**
Download from: https://redis.io/download

### 3. Verify Redis

```bash
redis-cli ping
# Should return: PONG
```

---

## Quick Start

### Option 1: Start Everything Automatically

```bash
chmod +x scripts/start_all.sh
./scripts/start_all.sh
```

### Option 2: Start Services Manually

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

---

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_BACKEND_URL=redis://localhost:6379/0

# Groq API
GROQ_API_KEY=your_groq_api_key

# Database (if using)
DB_TYPE=postgresql
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=resume_optimizer

# Logging
LOG_LEVEL=INFO
```

---

## Database Setup

### 1. Create Tables

```bash
python -c "from database import create_tables; create_tables()"
```

### 2. Create Indexes (IMPORTANT for performance)

```bash
python database/indexes.py
```

This creates indexes for:
- Fast candidate queries
- Fast job queries
- Fast optimization lookups
- Fast sorting by match score

---

## API Endpoints

### Health Check
```bash
GET /api/health
```

### Bulk Optimize (Async)
```bash
POST /api/recruiter/optimize/bulk
{
  "candidate_ids": [1, 2, 3],
  "job_id": 1
}

# Returns:
{
  "success": true,
  "task_id": "abc123...",
  "status": "queued",
  "check_status_url": "/api/recruiter/tasks/abc123..."
}
```

### Check Task Status
```bash
GET /api/recruiter/tasks/{task_id}
```

### Get Statistics
```bash
GET /api/recruiter/stats
```

---

## Monitoring

### Performance Metrics

Access metrics at: `http://localhost:5000/api/recruiter/stats`

Metrics include:
- Total optimizations
- Success rate
- Cache hit rate
- Average processing time
- Error count

### Prometheus Metrics

If using Prometheus, metrics are available at:
- `optimization_requests_total`
- `optimization_duration_seconds`
- `cache_hits_total`
- `cache_misses_total`
- `api_errors_total`

---

## Scaling

### For 1000 Resumes/Day

**Current Setup:**
- 1 Flask app
- 1 Celery worker (10 concurrent tasks)
- 1 Redis instance

**Capacity:** ~2000-3000/day ✅

### For 5000+ Resumes/Day

**Recommended:**
- 2-3 Flask apps (behind load balancer)
- 3-5 Celery workers (10 concurrent each)
- Redis cluster or managed Redis

**Capacity:** 5000-10000/day ✅

---

## Performance Tuning

### Celery Workers

Adjust concurrency:
```bash
celery -A config.celery_config worker --concurrency=20
```

### Redis Memory

Set max memory in `redis.conf`:
```
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### Database Connection Pool

In `database/models.py`, adjust pool size:
```python
create_engine(
    database_url,
    pool_size=20,
    max_overflow=40
)
```

---

## Troubleshooting

### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

### Celery Worker Not Processing

```bash
# Check worker status
celery -A config.celery_config inspect active

# Restart worker
pkill -f celery
celery -A config.celery_config worker --loglevel=info
```

### High Memory Usage

1. Reduce Celery worker concurrency
2. Enable Redis memory limits
3. Reduce cache TTL
4. Clean up old results

### Slow Queries

1. Verify indexes are created: `python database/indexes.py`
2. Check database connection pool size
3. Monitor slow queries in database logs

---

## Production Deployment

### Using Docker

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app_recruiter_production.py"]
```

### Using Systemd (Linux)

Create `/etc/systemd/system/resume-optimizer.service`:

```ini
[Unit]
Description=Resume Optimizer API
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/resume-optimizer
ExecStart=/usr/bin/python3 app_recruiter_production.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Using Supervisor

Create `/etc/supervisor/conf.d/resume-optimizer.conf`:

```ini
[program:resume-optimizer-api]
command=/usr/bin/python3 app_recruiter_production.py
directory=/opt/resume-optimizer
autostart=true
autorestart=true
user=www-data

[program:resume-optimizer-worker]
command=/usr/bin/celery -A config.celery_config worker --loglevel=info
directory=/opt/resume-optimizer
autostart=true
autorestart=true
user=www-data
```

---

## Cost Estimate (1000 Resumes/Day)

### Infrastructure:
- **Single Server:** $40-60/month
- **Managed Redis:** $15/month (optional)
- **Managed Database:** $25/month (optional)

### API Costs:
- **Groq:** $12-15/month
- **With 30% cache hit:** $8-10/month

**Total: $40-110/month** ✅

---

## Security

### Rate Limiting
- Default: 1000 requests/day, 100/hour
- Bulk operations: 10/minute
- Single operations: 30/minute

### API Keys
- Store in environment variables
- Never commit to git
- Rotate regularly

### Database
- Use connection pooling
- Parameterized queries (SQLAlchemy handles this)
- Regular backups

---

## Next Steps

1. ✅ Set up Redis
2. ✅ Create database indexes
3. ✅ Start Celery worker
4. ✅ Start Flask app
5. ✅ Test with small batch
6. ✅ Monitor performance
7. ✅ Scale as needed

---

## Support

For issues:
1. Check logs: `celery.log`
2. Check Redis: `redis-cli monitor`
3. Check health: `/api/health`
4. Check stats: `/api/recruiter/stats`

