# Recruiter Tool - Quick Start Guide

## ✅ This is the CORRECT Version!

**For:** Internal recruiters (not job seekers)  
**Purpose:** Bulk optimize candidate resumes from your database  
**No file parsing needed** - uses structured data

---

## 🚀 Quick Start

### Step 1: Run the Recruiter Tool

```bash
python3 app_recruiter_demo.py
```

### Step 2: Open Browser

Go to: `http://localhost:5001` (or port shown in terminal)

---

## 📋 What You'll See

### Dashboard
- Total candidates: 50 (dummy data)
- Job postings: 3
- Optimization statistics

### Candidates Tab
- Browse 50+ candidates
- Search and filter
- Select multiple candidates (bulk selection)
- See candidate skills and experience

### Bulk Optimize Tab
1. Select a job posting
2. See selected candidates
3. Click "Optimize Selected Candidates"
4. Watch progress bar
5. See results summary

### Review Queue Tab
- View all optimized candidates
- See match scores
- Click "Review" for before/after comparison
- Approve or reject optimizations
- Bulk approve option

---

## 🎯 Workflow

1. **Select Candidates**
   - Go to "Candidates" tab
   - Search/filter candidates
   - Select multiple (checkboxes)
   - See "X selected" count

2. **Optimize**
   - Go to "Bulk Optimize" tab
   - Select job posting
   - Click "Optimize Selected Candidates"
   - Wait for processing (progress bar)

3. **Review**
   - Go to "Review Queue" tab
   - Select job posting
   - See all optimized candidates
   - Click "Review" to see before/after
   - Approve or reject

4. **Approve**
   - Individual: Click "Approve" button
   - Bulk: Select multiple and approve all
   - Approved optimizations are saved

---

## 💡 Features

### Bulk Selection
- Select all candidates at once
- Deselect all
- See count of selected
- Visual indication (highlighted cards)

### Progress Tracking
- Real-time progress bar
- Percentage complete
- Status updates

### Before/After Comparison
- Side-by-side view
- Original vs Optimized
- Easy to compare changes
- Approve/reject buttons

### Match Scoring
- Match score: How well candidate matches job
- Quality score: Resume quality (0-100)
- Color-coded badges

---

## 📊 Dummy Data Included

**50 Candidates:**
- Various skills (Python, JavaScript, React, AWS, etc.)
- Different experience levels
- Multiple companies
- Structured data format

**3 Job Postings:**
- Senior Software Engineer
- Full Stack Developer
- Machine Learning Engineer

---

## 🔄 How It Works

1. **Candidate Data** (from your database - simulated)
   - Structured fields: name, email, experience, skills, education
   - No file parsing needed!

2. **Optimization**
   - Converts structured data to resume text
   - Uses Groq API (or fallback) to optimize
   - Stores results

3. **Review**
   - Shows original and optimized versions
   - Recruiter reviews changes
   - Approves or rejects

4. **Approval**
   - Approved optimizations saved
   - Can be exported or used in your platform

---

## 🎨 UI Features

- **Modern sidebar navigation**
- **Card-based candidate display**
- **Bulk selection interface**
- **Progress tracking**
- **Side-by-side comparison**
- **Color-coded scores**
- **Responsive design**

---

## ⚙️ Configuration

### Use Groq AI (Optional)

Set environment variable:
```bash
export GROQ_API_KEY=your_key_here
```

Or enter in the UI when optimizing.

### Port Configuration

Automatically finds available port (5001, 5002, etc.)

---

## 📝 Notes

- **Dummy data** - No real database connection
- **Simulated optimization** - Uses simple text enhancement
- **All features work** - Full workflow functional
- **Ready for integration** - Easy to connect to real database

---

## 🚀 Try It Now!

```bash
python3 app_recruiter_demo.py
```

Then open the URL shown in terminal!

**This is the correct version for recruiters!** 🎯

