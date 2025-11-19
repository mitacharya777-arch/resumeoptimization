# 🚀 Start Resume Analyzer Locally

## Quick Start

### 1. Set Groq API Key (if you have one):
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

**Note:** If you don't have a Groq API key yet, the app will still start but won't be able to analyze resumes. You can get a free key from https://console.groq.com/

### 2. Start the App:
```bash
python app_resume_analyzer.py
```

### 3. You'll see:
```
🚀 Resume Analyzer API running on http://localhost:5000
📊 POST /api/analyze - Analyze resume match score
✨ POST /api/optimize - Optimize resume
❤️  GET  /api/health - Health check
```

---

## Test It

### Test Health Endpoint:
```bash
curl http://localhost:5000/api/health
```

### Test Analyze Endpoint:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\n5 years experience in Python and JavaScript",
    "job_description": "Looking for Senior Software Engineer with 5+ years in Python, JavaScript, and React"
  }'
```

---

## Access URLs

- **API Base:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health
- **Analyze:** http://localhost:5000/api/analyze (POST)
- **Optimize:** http://localhost:5000/api/optimize (POST)

---

## Troubleshooting

### Port Already in Use?
The app will automatically find a free port. Check the console output for the actual port number.

### Groq API Not Available?
- Make sure you set `GROQ_API_KEY` environment variable
- Or the app will show a warning but still start (won't be able to analyze)

### Can't Access?
- Make sure the app is running (check console)
- Try `http://127.0.0.1:5000` instead of `localhost:5000`

---

## Ready!

Just run:
```bash
python app_resume_analyzer.py
```

Then test with the curl commands above or integrate with your job board! 🎯

