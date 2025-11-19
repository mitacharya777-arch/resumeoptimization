# Complete Integration Guide - Resume Analyzer & Optimizer

## Overview

This API analyzes resumes against job descriptions and provides intelligent, content-based suggestions. It only shows the optimization option if the match score is below 70%.

---

## API Endpoints

### 1. Analyze Resume (`POST /api/analyze`)

Analyzes resume against job description and returns match score + suggestions.

**Request:**
```json
{
  "resume_text": "User's resume content...",
  "job_description": "Full job description from posting..."
}
```

**Response:**
```json
{
  "success": true,
  "match_score": 65,
  "show_optimization": true,
  "strengths": [
    "Strong experience in relevant technologies",
    "Good educational background"
  ],
  "improvements_needed": [
    "Missing experience with specific framework",
    "Need to highlight relevant projects"
  ],
  "content_suggestions": [
    "Experience Section: Add more details about your full-stack projects - Explain how you used React and Node.js together - Example: 'Developed full-stack web application using React frontend and Node.js backend, improving user engagement by 40%'",
    "Skills Section: Emphasize your JavaScript expertise - Move JavaScript to top of skills list - Add specific frameworks you've used"
  ],
  "message": "Resume needs optimization to better match this job."
}
```

**Key Points:**
- `match_score`: 0-100 (strict scoring)
- `show_optimization`: `true` if score < 70%, `false` if >= 70%
- `content_suggestions`: Specific content changes (not just keywords)

---

### 2. Optimize Resume (`POST /api/optimize`)

Creates optimized resume based on suggestions.

**Request:**
```json
{
  "resume_text": "Original resume...",
  "job_description": "Job description...",
  "suggestions": ["suggestion 1", "suggestion 2"]  // Optional - will analyze if not provided
}
```

**Response:**
```json
{
  "success": true,
  "optimized_resume": "Complete optimized resume content...",
  "original_resume": "Original resume content..."
}
```

---

## Integration Flow

### Step 1: User clicks "Optimize Resume" button

```javascript
async function handleOptimizeResume(resumeText, jobDescription) {
  // First, analyze the resume
  const analysis = await analyzeResume(resumeText, jobDescription);
  
  // Check match score
  if (analysis.match_score >= 70) {
    // Don't show optimization option
    showMessage(`Great! Your resume matches ${analysis.match_score}% with this job. No optimization needed.`);
    return;
  }
  
  // Score < 70%, show optimization option
  showOptimizationOption(analysis);
}
```

### Step 2: Show analysis results

```javascript
function showOptimizationOption(analysis) {
  // Show match score
  displayMatchScore(analysis.match_score);
  
  // Show strengths
  displayStrengths(analysis.strengths);
  
  // Show improvements needed
  displayImprovements(analysis.improvements_needed);
  
  // Show content suggestions
  displayContentSuggestions(analysis.content_suggestions);
  
  // Show "Optimize Resume" button
  showOptimizeButton();
}
```

### Step 3: User clicks "Optimize" button

```javascript
async function optimizeResume(resumeText, jobDescription, suggestions) {
  const result = await fetch('http://localhost:5000/api/optimize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
      suggestions: suggestions  // From analysis
    })
  });
  
  const data = await result.json();
  
  if (data.success) {
    // Show optimized resume
    showOptimizedResume(data.optimized_resume, data.original_resume);
  }
}
```

---

## Complete JavaScript Example

```javascript
const API_BASE = 'http://localhost:5000';

// Step 1: Analyze resume when user clicks button
async function onOptimizeResumeClick() {
  const resumeText = getUserResume(); // Get from your system
  const jobDescription = getCurrentJobDescription(); // Get from job posting
  
  try {
    // Show loading
    showLoading('Analyzing resume...');
    
    // Analyze
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription
      })
    });
    
    const analysis = await response.json();
    
    if (!analysis.success) {
      throw new Error(analysis.error);
    }
    
    // Check score
    if (analysis.match_score >= 70) {
      // Good match - don't show optimization
      hideLoading();
      showSuccessMessage(
        `Your resume matches ${analysis.match_score}% with this job! ` +
        `No optimization needed.`
      );
      return;
    }
    
    // Score < 70% - show optimization option
    hideLoading();
    showOptimizationPanel(analysis);
    
  } catch (error) {
    hideLoading();
    showError('Error analyzing resume: ' + error.message);
  }
}

// Step 2: Show optimization panel
function showOptimizationPanel(analysis) {
  const panel = document.getElementById('optimization-panel');
  
  panel.innerHTML = `
    <div class="match-score">
      <h3>Match Score: ${analysis.match_score}%</h3>
      <p>${analysis.message}</p>
    </div>
    
    <div class="strengths">
      <h4>Strengths:</h4>
      <ul>
        ${analysis.strengths.map(s => `<li>${s}</li>`).join('')}
      </ul>
    </div>
    
    <div class="improvements">
      <h4>Improvements Needed:</h4>
      <ul>
        ${analysis.improvements_needed.map(i => `<li>${i}</li>`).join('')}
      </ul>
    </div>
    
    <div class="suggestions">
      <h4>Content Suggestions:</h4>
      <ol>
        ${analysis.content_suggestions.map(s => `<li>${s}</li>`).join('')}
      </ol>
    </div>
    
    <button onclick="proceedWithOptimization()" class="btn-optimize">
      Optimize Resume
    </button>
  `;
  
  panel.style.display = 'block';
}

// Step 3: Optimize resume
async function proceedWithOptimization() {
  const resumeText = getUserResume();
  const jobDescription = getCurrentJobDescription();
  const suggestions = getContentSuggestions(); // From analysis panel
  
  try {
    showLoading('Optimizing resume...');
    
    const response = await fetch(`${API_BASE}/api/optimize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
        suggestions: suggestions
      })
    });
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    hideLoading();
    showOptimizedResume(result.optimized_resume, result.original_resume);
    
  } catch (error) {
    hideLoading();
    showError('Error optimizing resume: ' + error.message);
  }
}

// Helper: Show optimized resume with comparison
function showOptimizedResume(optimized, original) {
  // Show side-by-side comparison or tabs
  // Let user review and accept/reject changes
}
```

---

## UI Flow

1. **User clicks "Optimize Resume" button** on job posting
2. **System analyzes** resume vs job description
3. **If score >= 70%**: Show success message, hide optimization option
4. **If score < 70%**: 
   - Show match score
   - Show strengths
   - Show improvements needed
   - Show content suggestions
   - Show "Optimize Resume" button
5. **User clicks "Optimize"**: Show optimized resume
6. **User reviews** and can accept/reject changes

---

## Key Features

✅ **Intelligent Analysis**: Uses Groq API for smart content analysis  
✅ **Strict Scoring**: Accurate 0-100% match score  
✅ **Content-Based**: Focuses on meaningful content changes, not keywords  
✅ **Conditional Display**: Only shows optimization if score < 70%  
✅ **Specific Suggestions**: Detailed, actionable content improvement suggestions  

---

## Setup

1. **Set Groq API Key:**
   ```bash
   export GROQ_API_KEY=your_key_here
   ```

2. **Start API:**
   ```bash
   python app_resume_analyzer.py
   ```

3. **Integrate with your job board** using the JavaScript examples above.

---

## That's It!

Simple, intelligent, and focused on content quality - not keyword stuffing! 🎯

