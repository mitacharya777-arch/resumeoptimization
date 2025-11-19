# Groq-Powered Resume Optimizer - Complete Guide

## Overview

This guide explains how to use the Groq-powered resume optimization features to create job-specific resumes for each application.

## What is Groq?

Groq is a fast LLM API provider that offers high-speed inference. It's perfect for resume optimization because:
- **Fast**: Processes resumes in seconds
- **Cost-effective**: Competitive pricing
- **High quality**: Uses state-of-the-art models like Llama 3.1

## Setup

### 1. Get Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key

### 2. Set API Key

**Option A: Environment Variable (Recommended)**
```bash
export GROQ_API_KEY="your_api_key_here"
```

**Option B: .env File**
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

**Option C: Command Line**
Use `--api-key` flag when running scripts

## Usage Methods

### Method 1: Command Line - Single Job

Optimize your resume for one job application:

```bash
python groq_resume_optimizer.py \
  --resume your_resume.pdf \
  --job_description job.txt \
  --output optimized_resume.txt
```

**With job details:**
```bash
python groq_resume_optimizer.py \
  -r resume.pdf \
  -j job.txt \
  -o optimized_resume.txt \
  --job-title "Software Engineer" \
  --company "Tech Corp"
```

### Method 2: Command Line - Batch Processing

Optimize resume for multiple jobs at once:

```bash
python resume_editor.py \
  --batch \
  -r original_resume.pdf \
  --jobs-dir ./job_descriptions \
  --output-dir ./optimized_resumes
```

**Directory structure:**
```
job_descriptions/
  ├── job1_tech_corp.txt
  ├── job2_startup_inc.txt
  └── job3_big_company.txt

optimized_resumes/
  ├── resume_TechCorp_SoftwareEngineer.txt
  ├── resume_StartupInc_FullStackDeveloper.txt
  └── resume_BigCompany_SeniorEngineer.txt
```

**With job info file (optional):**
Create `job_info.json`:
```json
{
  "job1_tech_corp": {
    "title": "Software Engineer",
    "company": "Tech Corp"
  },
  "job2_startup_inc": {
    "title": "Full Stack Developer",
    "company": "Startup Inc"
  }
}
```

Then run:
```bash
python resume_editor.py \
  --batch \
  -r resume.pdf \
  --jobs-dir ./job_descriptions \
  --output-dir ./optimized_resumes \
  --job-info job_info.json
```

### Method 3: Web Interface

Launch the enhanced web interface:

```bash
python app_groq.py
```

Then:
1. Open http://localhost:5000
2. Go to "Optimize with AI" tab
3. Enter your Groq API key (or set environment variable)
4. Upload resume and paste job description
5. Choose optimization type
6. Click "Optimize Resume"
7. Download the optimized version

## Optimization Types

### 1. Complete Resume Optimization
- Rewrites entire resume
- Incorporates all relevant keywords
- Reorders content for relevance
- Optimizes all sections
- **Best for**: Creating a new version for each job

### 2. Keyword Suggestions
- Identifies missing keywords
- Suggests where to add them
- Provides example phrases
- **Best for**: Quick improvements

### 3. Overall Analysis
- Comprehensive analysis
- Section-by-section recommendations
- ATS optimization tips
- **Best for**: Understanding what to improve

### 4. Section-by-Section
- Optimize individual sections
- Detailed change explanations
- **Best for**: Targeted improvements

## Workflow for Job Applications

### Recommended Workflow

1. **Prepare Your Base Resume**
   - Have a master resume with all your experience
   - Save it in a standard format (PDF or DOCX)

2. **Collect Job Descriptions**
   - Save each job description as a text file
   - Name them descriptively (e.g., `tech_corp_software_engineer.txt`)

3. **Optimize for Each Job**
   ```bash
   python resume_editor.py \
     -r master_resume.pdf \
     -j tech_corp_software_engineer.txt \
     -o optimized/tech_corp_resume.txt \
     --job-title "Software Engineer" \
     --company "Tech Corp"
   ```

4. **Review and Customize**
   - Review the optimized resume
   - Make any manual adjustments
   - Ensure all information is accurate

5. **Save and Apply**
   - Save with a clear filename
   - Use for your application

### Batch Workflow

For multiple applications:

1. **Organize Job Descriptions**
   ```
   job_descriptions/
     ├── job1.txt
     ├── job2.txt
     └── job3.txt
   ```

2. **Run Batch Optimization**
   ```bash
   python resume_editor.py \
     --batch \
     -r master_resume.pdf \
     --jobs-dir ./job_descriptions \
     --output-dir ./optimized_resumes
   ```

3. **Review All Versions**
   - Check the `batch_summary.json` for results
   - Review each optimized resume
   - Make final adjustments

## Advanced Features

### Custom Models

Groq offers different models. You can specify which to use:

```bash
python groq_resume_optimizer.py \
  -r resume.pdf \
  -j job.txt \
  --model "llama-3.1-70b-versatile"  # or "mixtral-8x7b-32768"
```

### Section-Specific Optimization

Optimize just one section:

```python
from utils.groq_optimizer import GroqResumeOptimizer

optimizer = GroqResumeOptimizer(api_key="your_key")

result = optimizer.optimize_section(
    section_name="Experience",
    section_content="Your current experience section...",
    job_description="Job description text..."
)

print(result["optimized_content"])
print(result["changes"])
```

### Programmatic Usage

```python
from resume_editor import ResumeEditor

editor = ResumeEditor(groq_api_key="your_key")

result = editor.create_job_specific_resume(
    original_resume_path="resume.pdf",
    job_description_path="job.txt",
    output_path="optimized.txt",
    job_title="Software Engineer",
    company_name="Tech Corp"
)

if "error" not in result:
    print(f"Saved to: {result['output_path']}")
```

## Tips for Best Results

1. **Detailed Job Descriptions**: The more detail in the job description, the better the optimization

2. **Complete Base Resume**: Include all your experience, skills, and achievements in your master resume

3. **Review Outputs**: Always review AI-generated content for accuracy

4. **Maintain Truthfulness**: Never add skills or experience you don't have

5. **Customize Further**: Use AI output as a starting point, then customize

6. **Save Versions**: Keep track of which resume version you used for which application

## Troubleshooting

### API Key Issues
```
Error: Groq API not available
```
- Check that `GROQ_API_KEY` is set correctly
- Verify the API key is valid at console.groq.com
- Make sure you have API credits

### Rate Limits
If you hit rate limits:
- Add delays between requests
- Use batch processing during off-peak hours
- Consider upgrading your Groq plan

### Quality Issues
If optimization quality is poor:
- Try a different model (e.g., `llama-3.1-70b-versatile`)
- Provide more detailed job description
- Break down into section-by-section optimization

### File Parsing Issues
```
Error: Could not parse resume file
```
- Ensure file is not corrupted
- Try converting PDF to DOCX first
- Check file size (should be < 16MB)

## Cost Considerations

Groq pricing is typically:
- Very affordable for resume optimization
- Pay-per-use model
- Free tier available for testing

Each optimization uses approximately:
- Complete resume: ~2000-4000 tokens
- Section optimization: ~1000-2000 tokens
- Keyword suggestions: ~500-1000 tokens

## Examples

### Example 1: Single Job Application

```bash
# 1. Save job description
echo "Software Engineer position..." > tech_corp_job.txt

# 2. Optimize resume
python groq_resume_optimizer.py \
  -r my_resume.pdf \
  -j tech_corp_job.txt \
  -o tech_corp_optimized.txt

# 3. Review and use
cat tech_corp_optimized.txt
```

### Example 2: Multiple Applications

```bash
# 1. Create job descriptions directory
mkdir job_descriptions
# Add job description files

# 2. Batch optimize
python resume_editor.py \
  --batch \
  -r master_resume.pdf \
  --jobs-dir ./job_descriptions \
  --output-dir ./applications

# 3. Review summary
cat applications/batch_summary.json
```

## Next Steps

1. Set up your Groq API key
2. Prepare your master resume
3. Try optimizing for one job
4. Review the results
5. Scale up to batch processing

Happy optimizing! 🚀

