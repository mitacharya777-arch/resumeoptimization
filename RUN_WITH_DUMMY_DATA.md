# 🚀 Run with Dummy Data - No API Key Needed!

## ✅ Good News!

The app now works with **dummy data** - you can test it immediately without a Groq API key!

---

## Quick Start

### Just run:
```bash
python app_resume_analyzer.py
```

**That's it!** No API key needed for testing.

---

## Test It

### 1. Start the app:
```bash
python app_resume_analyzer.py
```

### 2. Test analyze endpoint:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\n5 years experience in Python and JavaScript",
    "job_description": "Looking for Senior Software Engineer with 5+ years in Python, JavaScript, React, and Node.js"
  }'
```

### 3. You'll get a response like:
```json
{
  "success": true,
  "match_score": 65,
  "show_optimization": true,
  "strengths": ["Good technical foundation", "Relevant work experience"],
  "improvements_needed": ["Missing React experience", "Need to highlight projects"],
  "content_suggestions": [
    "Experience Section: Add more details about your Python projects...",
    "Skills Section: Emphasize your most relevant technical skills..."
  ],
  "message": "Resume needs optimization to better match this job."
}
```

---

## How Dummy Data Works

- **Match Score**: Calculated based on keyword matching between resume and job
- **Suggestions**: Generated based on missing keywords and experience level
- **Optimization**: Creates a dummy optimized version with notes

**Note:** For real AI-powered analysis, set `GROQ_API_KEY` environment variable. But for testing, dummy data works perfectly!

---

## Test Different Scenarios

### Low Match Score (< 70%):
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nPython Developer",
    "job_description": "Senior Full Stack Engineer with React, Node.js, AWS, Docker, Kubernetes"
  }'
```
**Result:** `show_optimization: true` (score will be low)

### High Match Score (>= 70%):
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSenior Software Engineer\n10 years Python, JavaScript, React, Node.js, AWS, Docker",
    "job_description": "Senior Full Stack Engineer with React, Node.js, AWS, Docker"
  }'
```
**Result:** `show_optimization: false` (score will be high)

---

## Ready to Test!

Just run:
```bash
python app_resume_analyzer.py
```

Then test with the curl commands above or integrate with your job board! 🎯

