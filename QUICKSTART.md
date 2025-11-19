# Quick Start Guide

Get started with Resume Optimizer in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Try Basic Version

Run the basic analyzer with sample data:

```bash
python basic_resume_analyzer.py
```

You should see output showing:
- Word count
- Top keywords
- Detected sections

## Step 3: Test with Your Resume

### Option A: Command Line (Intermediate)

1. Place your resume (PDF or DOCX) in the project folder
2. Create a job description file (or use `sample_job_description.txt`)
3. Run:

```bash
python resume_optimizer.py --resume your_resume.pdf --job_description sample_job_description.txt
```

### Option B: Web Interface (Advanced)

1. Start the web server:

```bash
python app.py
```

2. Open your browser: http://localhost:5000
3. Upload your resume and paste job description
4. Click "Analyze Resume"

## Step 4: (Optional) Enable AI Features

1. Get OpenAI API key from https://platform.openai.com/api-keys
2. Create `.env` file in project root:
   ```
   OPENAI_API_KEY=your_key_here
   ```
3. Use AI-powered version:

```bash
python resume_optimizer_ai.py --resume your_resume.pdf --job_description job.txt
```

## What to Expect

- **Quality Score**: How well-structured your resume is (0-100)
- **Match Score**: How well your resume matches the job (0-100%)
- **Keywords**: What keywords are found/missing
- **Suggestions**: Actionable improvements

## Next Steps

- Read the full README.md for detailed documentation
- Customize keywords in `utils/keyword_extractor.py`
- Modify scoring in `resume_optimizer.py`
- Style the web interface in `static/css/style.css`

Happy optimizing! 🚀

