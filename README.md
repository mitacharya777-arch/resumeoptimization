# Resume Optimizer

A progressive resume optimization tool that helps you tailor your resume for job applications. Built with Python, this tool progresses from basic text analysis to advanced AI-powered recommendations.

## 🚀 Features

### Basic Level
- ✅ Text-based resume parsing
- ✅ Keyword extraction and frequency analysis
- ✅ Section detection (Experience, Education, Skills, etc.)
- ✅ Word count and basic metrics

### Intermediate Level
- ✅ PDF and DOCX file parsing
- ✅ Job description analysis and matching
- ✅ Resume scoring against job requirements (0-100%)
- ✅ Keyword gap analysis (missing vs. found keywords)
- ✅ Technical skills detection
- ✅ Quality scoring and improvement suggestions
- ✅ ATS (Applicant Tracking System) optimization tips

### Advanced Level
- ✅ Beautiful web interface (Flask)
- ✅ File upload support (PDF, DOCX, TXT)
- ✅ Real-time analysis and visualization
- ✅ Interactive reports with color-coded scores
- ✅ AI-powered suggestions (optional, requires OpenAI API key)

### Groq-Powered Optimization (Recommended)
- ✅ **Fast AI-powered resume optimization using Groq API**
- ✅ **Job-specific resume generation** - Create tailored resumes for each application
- ✅ **Section-by-section optimization** - Optimize individual sections
- ✅ **Batch processing** - Optimize for multiple jobs at once
- ✅ **Complete resume rewriting** - AI generates optimized versions
- ✅ **Keyword integration** - Automatically adds relevant keywords
- ✅ **Web interface with Groq** - Easy-to-use web app for optimization

### Database Edition (Full-Featured) 🗄️
- ✅ **PostgreSQL database integration** - Store resumes, jobs, and optimizations
- ✅ **Resume management** - Upload, view, and manage multiple resumes
- ✅ **Job description management** - Save and organize job postings
- ✅ **Optimization history** - Track all optimizations with full history
- ✅ **Analytics dashboard** - View statistics and insights
- ✅ **Modern web UI** - Beautiful, responsive interface for testing
- ✅ **CRUD operations** - Full create, read, update, delete functionality

## 📦 Installation

1. **Install Python 3.8 or higher**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Clone or download this repository**
   ```bash
   cd resumeoptimization
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model** (optional, for advanced NLP)
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up OpenAI API key** (optional, for AI features)
   - Create a `.env` file in the project root
   - Add: `OPENAI_API_KEY=your_api_key_here`
   - Get your API key from: https://platform.openai.com/api-keys

## 📖 Usage

### Level 1: Basic Usage (Command Line)

Simple text analysis without file parsing:

```bash
python basic_resume_analyzer.py
```

This runs with a sample resume and shows:
- Word count
- Top keywords
- Detected sections

### Level 2: Intermediate Usage (File Parsing + Job Matching)

Analyze your resume file against a job description:

```bash
python resume_optimizer.py --resume your_resume.pdf --job_description job_description.txt
```

**Example:**
```bash
# With PDF resume
python resume_optimizer.py -r resume.pdf -j job.txt

# With DOCX resume
python resume_optimizer.py -r resume.docx -j job.txt

# Without job description (quality analysis only)
python resume_optimizer.py -r resume.pdf
```

**Output includes:**
- Resume quality score (0-100)
- Job match score (0-100%)
- Matching keywords
- Missing keywords
- Technical skills detected
- Improvement suggestions

### Level 3: Advanced Usage (Web Interface)

Launch the web application:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Features:**
- Upload resume files (PDF, DOCX, TXT)
- Paste job description directly
- View interactive analysis reports
- Color-coded scores and visualizations
- Download-ready format

### Level 4: Groq-Powered Optimization (Recommended) ⚡

**Fast AI-powered resume optimization for job applications:**

#### Single Job Optimization
```bash
python groq_resume_optimizer.py --resume resume.pdf --job_description job.txt --output optimized.txt
```

#### Create Job-Specific Resume
```bash
python resume_editor.py \
  -r resume.pdf \
  -j job.txt \
  -o optimized_resume.txt \
  --job-title "Software Engineer" \
  --company "Tech Corp"
```

#### Batch Process Multiple Jobs
```bash
python resume_editor.py \
  --batch \
  -r master_resume.pdf \
  --jobs-dir ./job_descriptions \
  --output-dir ./optimized_resumes
```

#### Web Interface with Groq
```bash
python app_groq.py
```
Then open http://localhost:5000 and use the "Optimize with AI" tab

**Requirements:**
- Groq API key (get from https://console.groq.com)
- Set `GROQ_API_KEY` environment variable or use `--api-key` flag
- Internet connection

**See `GROQ_GUIDE.md` for complete documentation!**

### Level 6: Database Edition (Full-Featured) 🗄️

**Complete web application with database support (SQLite or PostgreSQL):**

#### Option A: SQLite (Easiest - Recommended for Local Use) ⭐

**Zero setup required!**

```bash
# 1. Set environment variable
export DB_TYPE=sqlite

# 2. Run the app
python app_db.py
```

That's it! Database file will be created automatically.

**See `QUICKSTART_SQLITE.md` for details!**

#### Option B: PostgreSQL (For Production)

```bash
# 1. Install and start PostgreSQL
# 2. Create database
createdb resume_optimizer

# 3. Set environment variables
export DB_TYPE=postgresql
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_NAME=resume_optimizer

# 4. Initialize tables
python setup_database.py

# 5. Run application
python app_db.py
```

#### Run Application
```bash
python app_db.py
```

Then open http://localhost:5000

**Features:**
- 📊 Dashboard with analytics
- 📄 Resume management (upload, view, delete)
- 💼 Job description management
- 🚀 One-click optimization
- 📜 Full optimization history
- 💾 All data persisted in database
- 🔄 Supports both SQLite and PostgreSQL

**Database Choice:**
- **SQLite**: Perfect for local development, zero setup
- **PostgreSQL**: Better for production, multiple users

**See `DATABASE_COMPARISON.md` for database options!**

### Level 5: OpenAI-Powered (Alternative)

Use OpenAI for intelligent suggestions:

```bash
python resume_optimizer_ai.py --resume resume.pdf --job_description job.txt
```

**Requirements:**
- OpenAI API key in `.env` file
- Internet connection

## 📁 Project Structure

```
resumeoptimization/
├── basic_resume_analyzer.py    # Basic text analysis
├── resume_optimizer.py          # Intermediate version (file parsing + matching)
├── resume_optimizer_ai.py       # Advanced version with OpenAI
├── groq_resume_optimizer.py     # Groq-powered optimizer (Recommended)
├── resume_editor.py             # Resume editor for job-specific optimization
├── app.py                       # Web interface (Flask)
├── app_groq.py                  # Web interface with Groq integration
├── example_usage.py             # Usage examples
├── example_groq_usage.py        # Groq usage examples
├── GROQ_GUIDE.md                # Complete Groq optimization guide
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── utils/
│   ├── file_parser.py          # PDF/DOCX parsing utilities
│   ├── keyword_extractor.py    # Keyword extraction and analysis
│   └── ai_suggestions.py       # AI-powered suggestions
├── templates/
│   └── index.html              # Web interface template
└── static/
    └── css/
        └── style.css           # Web interface styles
```

## 🎯 How It Works

### Basic Level
1. Parses text input
2. Extracts words and counts frequency
3. Identifies common resume sections
4. Provides basic statistics

### Intermediate Level
1. Parses PDF/DOCX files to extract text
2. Analyzes resume structure and content
3. Compares resume keywords with job description
4. Calculates match score and identifies gaps
5. Generates actionable suggestions

### Advanced Level
1. All intermediate features
2. Beautiful web interface for easy use
3. Real-time analysis and visualization
4. Optional AI-powered recommendations

## 💡 Example Output

```
======================================================================
RESUME OPTIMIZATION REPORT
======================================================================

📊 RESUME QUALITY SCORE: 75/100
   Word Count: 450
   Sections: 4
   Technical Skills: 12

🎯 JOB MATCH SCORE: 68.5%
   Matching Keywords: 27/40

   ✅ Keywords Found in Resume:
      python, javascript, react, aws, docker, kubernetes...

   ❌ Missing Keywords (Top 10):
      microservices, graphql, typescript, jenkins...

💻 TECHNICAL SKILLS DETECTED:
   python, javascript, react, aws, docker, kubernetes...

💡 IMPROVEMENT SUGGESTIONS:
   1. Add missing keywords: microservices, graphql, typescript
   2. Increase usage of 'cloud' (current density: 0.05%)
   3. Resume is too short (recommended: 400-800 words)
```

## 🔧 Customization

### Adding Custom Keywords
Edit `utils/keyword_extractor.py` to add domain-specific keywords to the `TECH_KEYWORDS` set.

### Adjusting Scoring
Modify scoring weights in `resume_optimizer.py` in the `analyze_resume_quality()` method.

### Styling Web Interface
Edit `static/css/style.css` to customize the appearance.

## 🐛 Troubleshooting

**Issue: PDF parsing fails**
- Ensure `pdfplumber` is installed: `pip install pdfplumber`
- Try converting PDF to DOCX first

**Issue: DOCX parsing fails**
- Ensure `python-docx` is installed: `pip install python-docx`

**Issue: AI suggestions not working**
- Check that `OPENAI_API_KEY` is set in `.env` file
- Verify you have API credits on OpenAI account
- Check internet connection

**Issue: Web interface won't start**
- Ensure Flask is installed: `pip install flask flask-cors`
- Check if port 5000 is available
- Try: `python app.py --port 5001`

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Feel free to fork, modify, and improve this tool for your needs!

## 📧 Support

For issues or questions, please check the code comments or create an issue in the repository.

## 📚 Complete Documentation

For detailed, comprehensive documentation covering all aspects of the project:

**👉 See [COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md)**

This includes:
- Complete architecture overview
- Detailed API documentation
- Database schema details
- Frontend architecture
- Technical implementation details
- Troubleshooting guide
- And much more!

