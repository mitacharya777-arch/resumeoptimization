# Quick Start: Groq Resume Optimizer

Get started optimizing your resume for job applications in 3 steps!

## Step 1: Install & Setup (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Get your Groq API key from https://console.groq.com/keys

# Set API key (choose one method)
export GROQ_API_KEY="your_api_key_here"
# OR create .env file with: GROQ_API_KEY=your_api_key_here
```

## Step 2: Optimize Your First Resume (1 minute)

```bash
# Single job optimization
python groq_resume_optimizer.py \
  --resume your_resume.pdf \
  --job_description job.txt \
  --output optimized_resume.txt
```

That's it! The optimized resume will be saved to `optimized_resume.txt`.

## Step 3: Use for Multiple Jobs (Optional)

### Option A: One at a time
```bash
python resume_editor.py \
  -r master_resume.pdf \
  -j job1.txt \
  -o optimized_job1.txt \
  --job-title "Software Engineer" \
  --company "Tech Corp"
```

### Option B: Batch process
```bash
# Put all job descriptions in a folder
mkdir job_descriptions
# Add job1.txt, job2.txt, etc.

# Process all at once
python resume_editor.py \
  --batch \
  -r master_resume.pdf \
  --jobs-dir ./job_descriptions \
  --output-dir ./optimized_resumes
```

## Web Interface (Alternative)

```bash
python app_groq.py
```

Then open http://localhost:5000 and use the "Optimize with AI" tab.

## What You Get

✅ **Job-specific resume** - Tailored for each application  
✅ **Keyword optimization** - Automatically adds relevant keywords  
✅ **ATS-friendly** - Optimized for applicant tracking systems  
✅ **Professional formatting** - Clean, readable output  
✅ **Fast processing** - Seconds per resume  

## Example Workflow

1. **Prepare your master resume** (with all your experience)
2. **Save job descriptions** as text files
3. **Run optimization** for each job
4. **Review and customize** the output
5. **Apply with confidence!**

## Need Help?

- 📖 Full guide: `GROQ_GUIDE.md`
- 💡 Examples: `example_groq_usage.py`
- 📚 Main docs: `README.md`

## Common Commands

```bash
# Quick optimization
python groq_resume_optimizer.py -r resume.pdf -j job.txt -o output.txt

# With job details
python resume_editor.py -r resume.pdf -j job.txt -o output.txt \
  --job-title "Software Engineer" --company "Tech Corp"

# Batch mode
python resume_editor.py --batch -r resume.pdf \
  --jobs-dir ./jobs --output-dir ./output

# Web interface
python app_groq.py
```

Happy optimizing! 🚀

