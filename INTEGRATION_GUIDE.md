# Simple Resume Optimizer - Integration Guide

## What This Does

Just one thing: **Optimize a resume for a job posting**.

That's it. No dashboard, no complex UI, just a simple API endpoint.

---

## API Endpoint

### POST `/api/optimize`

**Request:**
```json
{
  "resume_text": "Your resume content here...",
  "job_description": "Full job description...",
  "job_title": "Junior Full Stack Developer",
  "job_requirements": ["SQL Server", "C#", ".NET", "JavaScript"]
}
```

**Response:**
```json
{
  "success": true,
  "optimized_resume": "Optimized resume content...",
  "suggestions": ["Added keywords", "Improved formatting"],
  "quality_score": 85,
  "match_score": 78
}
```

---

## How to Use with Your Job Board

### 1. Start the API:
```bash
python app_simple.py
```

### 2. In your job board, when user clicks "Optimize Resume":

```javascript
async function optimizeResume(resumeText, jobData) {
  const response = await fetch('http://localhost:5000/api/optimize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobData.description,
      job_title: jobData.title,
      job_requirements: jobData.requirements || []
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    // Show optimized resume to user
    displayOptimizedResume(result.optimized_resume);
  } else {
    alert('Error: ' + result.error);
  }
}
```

---

## That's It!

No complex setup, no dashboard, just:
1. Send resume + job description
2. Get optimized resume back
3. Show it to the user

Simple and clean! 🎯

