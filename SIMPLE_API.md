# Simple Resume Optimizer API

## What This Does

**Just one thing:** Optimize a resume for a job posting.

No dashboard, no complex UI, no unnecessary features. Just a simple API endpoint.

---

## Quick Start

### 1. Start the API:
```bash
python app_simple.py
```

### 2. API Endpoint:

**POST** `/api/optimize`

**Request:**
```json
{
  "resume_text": "Your resume content here...",
  "job_description": "Full job description here..."
}
```

**Response:**
```json
{
  "success": true,
  "optimized_resume": "Optimized resume content...",
  "original_resume": "Original resume content..."
}
```

---

## Integration with Your Job Board

### JavaScript Example:

```javascript
async function optimizeResume(resumeText, jobDescription) {
  try {
    const response = await fetch('http://localhost:5000/api/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      // Show optimized resume to user
      return result.optimized_resume;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Optimization error:', error);
    throw error;
  }
}

// Usage in your job board:
document.getElementById('optimize-btn').addEventListener('click', async () => {
  const resumeText = getUserResume(); // Get from your system
  const jobDescription = getCurrentJobDescription(); // Get from job posting
  
  try {
    const optimized = await optimizeResume(resumeText, jobDescription);
    showOptimizedResume(optimized); // Display to user
  } catch (error) {
    alert('Error optimizing resume: ' + error.message);
  }
});
```

---

## Setup

1. **Set Groq API Key:**
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```

2. **Start the API:**
   ```bash
   python app_simple.py
   ```

3. **That's it!** The API is ready to use.

---

## API Details

- **URL:** `http://localhost:5000/api/optimize`
- **Method:** POST
- **Content-Type:** application/json
- **CORS:** Enabled (can be called from any domain)

---

## Error Handling

If something goes wrong, you'll get:
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## That's It!

Simple, clean, and focused. Just optimize resumes for jobs. Nothing more, nothing less.

