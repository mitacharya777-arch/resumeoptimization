# Technical Documentation: Resume Optimization Application

## 📋 Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [AI Integration](#ai-integration)
7. [Frontend Implementation](#frontend-implementation)
8. [Backend Implementation](#backend-implementation)
9. [File Processing](#file-processing)
10. [Document Generation](#document-generation)
11. [Security & Production Features](#security--production-features)
12. [API Endpoints](#api-endpoints)
13. [Dependencies](#dependencies)
14. [Deployment Considerations](#deployment-considerations)
15. [Future Enhancements](#future-enhancements)

---

## Overview

This is a **Resume Optimization Application** that uses AI to analyze resumes against job descriptions, calculate match scores, and generate optimized resumes. The application supports multiple AI providers, file uploads (PDF, DOCX, TXT), and exports optimized resumes in multiple formats (PDF, DOCX, TXT).

### Key Features
- **Multi-AI Provider Support**: Groq, OpenAI, Claude, Gemini, Cohere
- **Resume Analysis**: Match score calculation with detailed breakdown
- **Resume Optimization**: AI-powered content rewriting with quantitative metrics
- **File Upload**: Support for PDF, DOCX, and TXT formats
- **Document Export**: PDF, DOCX, and TXT download options
- **Link Preservation**: Automatic extraction and preservation of LinkedIn/GitHub links
- **Score Comparison**: Before/after optimization score tracking
- **Section Analysis**: Detailed breakdown of improvements by section
- **Production-Ready**: Rate limiting, input validation, error handling

---

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: Flask 3.0.0
- **Web Server**: Flask Development Server (for local), Gunicorn/uWSGI (for production)
- **API Style**: RESTful API

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Variables, Flexbox, Grid
- **JavaScript (ES6+)**: Vanilla JavaScript (no frameworks)
- **Icons**: Font Awesome 6.0
- **Fonts**: Google Fonts (Inter, Poppins)

### AI/ML
- **Groq API**: Fast inference with Llama models
- **OpenAI API**: GPT models
- **Anthropic Claude API**: Claude models
- **Google Gemini API**: Gemini models
- **Cohere API**: Cohere models

### File Processing
- **PDF Parsing**: `pdfplumber` 0.10.0
- **DOCX Parsing**: `python-docx` 1.1.0
- **PDF Generation**: `reportlab` 4.0.7
- **DOCX Generation**: `python-docx` 1.1.0

### Utilities
- **Environment Variables**: `python-dotenv` 1.0.0
- **HTTP Requests**: `requests` 2.31.0 (for API calls)
- **CORS**: `flask-cors` 4.0.0
- **Rate Limiting**: `flask-limiter` 3.5.0

### Development Tools
- **Version Control**: Git
- **Package Management**: pip
- **Code Quality**: Python linting (implicit)

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│  (HTML/CSS/JavaScript - Vanilla JS, Font Awesome)          │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/HTTPS
                        │ REST API
┌───────────────────────▼─────────────────────────────────────┐
│                    Flask Application                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes & Endpoints                                  │  │
│  │  - / (UI)                                            │  │
│  │  - /api/analyze                                      │  │
│  │  - /api/optimize                                     │  │
│  │  - /api/upload-resume                                │  │
│  │  - /api/download                                     │  │
│  │  - /api/providers                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                │  │
│  │  - analyze_resume_match()                            │  │
│  │  - create_optimized_resume()                         │  │
│  │  - format_resume_line()                              │  │
│  │  - analyze_section_improvements()                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Utility Layer                                       │  │
│  │  - File Parser (PDF, DOCX, TXT)                      │  │
│  │  - Link Extractor (LinkedIn, GitHub)                 │  │
│  │  - AI Providers (Unified Interface)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   Groq API   │ │  OpenAI API │ │ Claude API  │ │ Gemini API  │
│              │ │             │ │             │ │             │
│ Llama 3.3    │ │ GPT-4/3.5   │ │ Claude 3.5  │ │ Gemini 2.5  │
│ 70B          │ │             │ │ Sonnet      │ │ Flash       │
└──────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### Request Flow

1. **User Uploads/Pastes Resume** → File Parser extracts text
2. **User Provides Job Description** → Stored in memory
3. **User Clicks "Analyze Resume"** → Backend calls AI provider
4. **AI Analyzes Resume** → Returns match score, strengths, improvements
5. **If Score < 70%** → "Optimize Resume" button appears
6. **User Clicks "Optimize"** → Backend calls AI provider with optimization prompt
7. **AI Generates Optimized Resume** → Returns formatted resume text
8. **Backend Re-analyzes** → Calculates new score and improvements
9. **Frontend Displays Results** → Shows before/after comparison
10. **User Downloads** → PDF/DOCX/TXT generation and download

---

## Project Structure

```
resumeoptimization/
├── app_web.py                      # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys)
├── .gitignore                      # Git ignore rules
│
├── templates/
│   └── resume_analyzer.html        # Main UI template
│
├── static/
│   ├── css/
│   │   └── (inline styles in HTML)
│   └── js/
│       └── (inline JavaScript in HTML)
│
├── utils/
│   ├── __init__.py
│   ├── ai_providers.py            # AI provider abstraction layer
│   ├── file_parser.py             # PDF/DOCX/TXT parsing
│   ├── link_extractor.py          # LinkedIn/GitHub link extraction
│   ├── groq_optimizer.py          # Legacy Groq-specific code
│   ├── keyword_extractor.py       # Keyword extraction utilities
│   └── ai_suggestions.py          # AI suggestion generation
│
├── config/
│   ├── __init__.py
│   └── celery_config.py           # Celery configuration (for scalability)
│
├── services/
│   ├── __init__.py
│   ├── optimization_tasks.py      # Celery tasks
│   ├── cache_manager.py           # Redis caching
│   ├── monitoring.py              # Performance monitoring
│   └── bulk_optimizer.py          # Bulk processing
│
├── database/
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy models
│   ├── db_utils.py                # Database utilities
│   └── indexes.py                 # Database indexes
│
└── Documentation/
    ├── TECHNICAL_DOCUMENTATION.md  # This file
    ├── GIT_SETUP.md
    ├── PRODUCTION_SETUP.md
    └── ... (other docs)
```

---

## Core Components

### 1. Flask Application (`app_web.py`)

**Purpose**: Main application entry point, handles all HTTP requests.

**Key Functions**:
- `analyze_resume_match()`: Analyzes resume against job description
- `create_optimized_resume()`: Generates optimized resume
- `format_resume_line()`: Categorizes resume lines for formatting
- `analyze_section_improvements()`: Compares original vs optimized resume

**Routes**:
- `GET /`: Renders main UI
- `POST /api/analyze`: Analyzes resume
- `POST /api/optimize`: Optimizes resume
- `POST /api/upload-resume`: Handles file uploads
- `POST /api/download`: Generates and downloads documents
- `GET /api/providers`: Returns available AI providers
- `GET /api/health`: Health check endpoint

**Key Features**:
- Automatic port detection
- CORS enabled
- Rate limiting (20/min for analyze, 10/min for optimize)
- Input validation (min/max length, file size)
- Error handling and logging
- Production mode detection

### 2. AI Provider Abstraction (`utils/ai_providers.py`)

**Purpose**: Unified interface for multiple AI providers.

**Design Pattern**: Abstract Base Class (ABC) with concrete implementations.

**Classes**:
- `AIProvider` (Abstract Base Class)
  - `is_available()`: Check if provider is configured
  - `analyze_resume()`: Analyze resume and return match score
  - `optimize_resume()`: Generate optimized resume

- `GroqProvider`: Groq API integration
  - Model: `llama-3.3-70b-versatile`
  - Fast inference, cost-effective

- `OpenAIProvider`: OpenAI API integration
  - Model: `gpt-4-turbo-preview` (fallback: `gpt-3.5-turbo`)
  - High quality, versatile

- `ClaudeProvider`: Anthropic Claude API integration
  - Model: `claude-3-5-sonnet-20240620` (with fallbacks)
  - Excellent reasoning, detailed analysis

- `GeminiProvider`: Google Gemini API integration
  - Model: `gemini-2.5-flash` (with fallbacks)
  - Fast, cost-effective

- `CohereProvider`: Cohere API integration
  - Model: `command-r-plus`
  - Good for text generation

**Key Features**:
- Standardized prompts across all providers
- Consistent scoring framework (50% skills match, 50% other factors)
- Temperature control (0.2 for analysis, 0.7 for optimization)
- Error handling and fallback mechanisms
- Social links preservation (LinkedIn/GitHub)

### 3. File Parser (`utils/file_parser.py`)

**Purpose**: Extract text from various file formats.

**Functions**:
- `parse_pdf(file_path)`: Extract text from PDF using pdfplumber
- `parse_docx(file_path)`: Extract text from DOCX using python-docx
- `parse_text_file(file_path)`: Read plain text files
- `parse_resume(file_path)`: Main function that detects format and parses

**Supported Formats**:
- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Plain Text (`.txt`)

**Error Handling**:
- Graceful degradation if libraries are missing
- Clear error messages
- File size validation (10MB max)

### 4. Link Extractor (`utils/link_extractor.py`)

**Purpose**: Extract LinkedIn and GitHub URLs from resume text.

**Functions**:
- `extract_social_links(resume_text)`: Main extraction function
- `format_contact_with_links()`: Format contact info with links

**Pattern Matching**:
- LinkedIn: `linkedin.com/in/...`, `www.linkedin.com/...`, `https://linkedin.com/...`
- GitHub: `github.com/...`, `www.github.com/...`, `https://github.com/...`

**Features**:
- Case-insensitive matching
- Handles various URL formats
- Auto-adds `https://` if missing
- Returns structured dictionary

### 5. Document Generation

#### PDF Generation (ReportLab)

**Library**: `reportlab` 4.0.7

**Features**:
- Professional formatting
- Custom fonts and styles
- Clickable hyperlinks (LinkedIn/GitHub)
- Black background for contact info
- Proper spacing and alignment
- Single-page optimization

**Styles**:
- `header_name_style`: Large, bold, centered name
- `header_title_style`: Medium, bold, centered title
- `header_contact_style`: White text on black background
- `main_section_style`: Section headers (SUMMARY, SKILLS, etc.)
- `experience_entry_style`: Bold company/job title/date
- `bullet_style`: Bullet points with proper indentation
- `project_entry_style`: Bold project names

#### DOCX Generation (python-docx)

**Library**: `python-docx` 1.1.0

**Features**:
- Microsoft Word compatible
- Clickable hyperlinks
- Custom formatting (fonts, colors, sizes)
- Paragraph shading (black background for contact)
- Proper spacing and alignment

**Formatting**:
- Header: Centered, bold, large font
- Contact: Black background, white text, clickable links
- Sections: Bold, black, proper spacing
- Experience: Bold entries, aligned bullets
- Projects: Bold project names

---

## AI Integration

### Prompt Engineering

#### Analysis Prompt Structure

```
SYSTEM MESSAGE:
"You are a strict resume analyst. Evaluate resumes using a structured scoring framework..."

USER PROMPT:
1. SCORING CRITERIA (6 factors, 100 points total):
   - Required Skills Match: 50 points (50%)
   - Experience Level Match: 20 points (20%)
   - Years of Experience: 12 points (12%)
   - Job Title Relevance: 10 points (10%)
   - Education Requirements: 5 points (5%)
   - Industry/Domain Experience: 3 points (3%)

2. SCORING GUIDELINES:
   - 0-40%: Missing most requirements
   - 40-70%: Some requirements met
   - 70-100%: Most/all requirements met

3. OUTPUT FORMAT:
   MATCH_SCORE: [number]
   STRENGTHS: [list]
   IMPROVEMENTS: [list]
   CONTENT_SUGGESTIONS: [list]
```

#### Optimization Prompt Structure

```
SYSTEM MESSAGE:
"You are an expert resume writer. CRITICAL: You must REWRITE experience bullet points..."

USER PROMPT:
1. EXPERIENCE SECTION RULES (MANDATORY):
   - Complete rewrite (not keyword addition)
   - Problem → Action → Result structure
   - Strong, varied action verbs
   - Quantitative metrics (numbers, percentages, $)
   - Qualitative achievements (leadership, innovation)
   - 4-6 bullet points per position
   - Natural ATS keyword integration

2. FORMATTING REQUIREMENTS:
   - Header: Name, Title, Contact (with LinkedIn/GitHub)
   - Sections: SUMMARY, SKILLS, EXPERIENCE, EDUCATION, PROJECTS
   - Experience format: "Company, Location | Dates | Job Title"
   - Projects format: "Project Name | Technologies | Date"

3. CONTENT REQUIREMENTS:
   - Maintain original information
   - Enhance with job-relevant content
   - Add quantifiable achievements
   - Use natural, professional tone
```

### Scoring Framework

**Structured Scoring (100 points total)**:

1. **Required Skills Match (50 points - 50%)**
   - Count all required skills/technologies
   - Match against resume skills
   - Calculate percentage match
   - Most critical factor

2. **Experience Level Match (20 points - 20%)**
   - Junior vs Senior alignment
   - Years of experience relevance
   - Responsibility level match

3. **Years of Experience (12 points - 12%)**
   - Compare required vs actual
   - Partial credit for close matches

4. **Job Title Relevance (10 points - 10%)**
   - Exact match: 10 points
   - Related title: 7 points
   - Transferable skills: 3 points

5. **Education Requirements (5 points - 5%)**
   - Degree level match
   - Field relevance

6. **Industry/Domain Experience (3 points - 3%)**
   - Same industry: 3 points
   - Related industry: 2 points

**Temperature Settings**:
- Analysis: `0.2` (strict, deterministic)
- Optimization: `0.7` (creative, varied)

---

## Frontend Implementation

### HTML Structure

**Template**: `templates/resume_analyzer.html`

**Sections**:
1. **Header**: CareerVest logo, "Resume Match" title
2. **Input Section**: 
   - Resume upload/textarea
   - Job description textarea
   - AI provider selector
3. **Analysis Results**:
   - Match score (circular progress)
   - Strengths list
   - Improvements list
   - Content suggestions
   - Optimize button (conditional)
4. **Optimization Results**:
   - Score comparison (before/after)
   - Section breakdown
   - Optimized resume display
   - Download options (PDF/DOCX/TXT)
   - Additional suggestions (if score < 60%)

### CSS Styling

**Design System**:
- **Colors**:
  - Primary: Maroon `#682A53`
  - Accent: Yellow `#FDC500`
  - Background: Dark gradients
  - Text: White/Light gray

- **Typography**:
  - Font Family: 'Inter', 'Poppins', sans-serif
  - Headings: Bold, larger sizes
  - Body: Regular, readable sizes

- **Layout**:
  - Flexbox for component layout
  - Grid for card layouts
  - Responsive design (mobile-friendly)

- **Effects**:
  - Glassmorphism (frosted glass effect)
  - Smooth transitions
  - Hover effects
  - Gradient backgrounds

**Key CSS Classes**:
- `.resume-header-name`: Large, bold, centered name
- `.resume-header-title`: Medium, bold, centered title
- `.resume-header-contact`: Contact info with clickable links
- `.resume-main-section`: Section headers (SUMMARY, SKILLS, etc.)
- `.resume-experience-entry`: Bold company/job/date
- `.resume-bullet`: Bullet points with proper alignment
- `.resume-project-entry`: Bold project names

### JavaScript Functionality

**Key Functions**:

1. **`handleResumeUpload(file)`**:
   - Handles file selection
   - Validates file type and size
   - Uploads to backend
   - Parses and displays text

2. **`analyzeResume()`**:
   - Collects resume and job description
   - Calls `/api/analyze` endpoint
   - Displays results (score, strengths, improvements)
   - Shows/hides optimize button based on score

3. **`optimizeResume()`**:
   - Collects original score and suggestions
   - Calls `/api/optimize` endpoint
   - Displays optimized resume
   - Shows score comparison
   - Shows section breakdown

4. **`formatResumeForDisplay(resumeText)`**:
   - Parses resume text line by line
   - Categorizes lines (header, section, bullet, etc.)
   - Applies appropriate CSS classes
   - Formats contact info with clickable links

5. **`formatContactWithLinks(contactLine)`**:
   - Detects LinkedIn/GitHub URLs
   - Converts to clickable `<a>` tags
   - Styles links (yellow, underlined)

6. **`downloadOptimizedResume(format)`**:
   - Sends optimized resume to `/api/download`
   - Specifies format (PDF/DOCX/TXT)
   - Triggers browser download

7. **`displayScoreComparison(comparison)`**:
   - Shows before/after scores
   - Calculates improvement percentage
   - Color-codes status (improved/declined)

8. **`displaySectionBreakdown(breakdown)`**:
   - Lists improved sections
   - Shows specific improvements
   - Highlights keywords added

---

## Backend Implementation

### Flask Configuration

```python
# Key configurations
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB file limit
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for downloads
app.config['DEBUG'] = False  # Production mode
```

### Rate Limiting

**Library**: `flask-limiter` 3.5.0

**Limits**:
- `/api/analyze`: 20 requests per minute
- `/api/optimize`: 10 requests per minute
- `/api/upload-resume`: 30 requests per hour
- `/api/download`: 30 requests per hour

**Storage**: In-memory (for simple setup), Redis (for production)

### Input Validation

**Resume Text**:
- Minimum: 50 characters
- Maximum: 50,000 characters

**Job Description**:
- Minimum: 20 characters
- Maximum: 20,000 characters

**File Uploads**:
- Maximum size: 10MB
- Allowed extensions: `.pdf`, `.docx`, `.doc`, `.txt`
- Filename validation (prevents path traversal)

### Error Handling

**Error Types**:
- `400 Bad Request`: Invalid input, missing parameters
- `413 Payload Too Large`: File too large
- `415 Unsupported Media Type`: Invalid file type
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server errors

**Error Response Format**:
```json
{
  "success": false,
  "error": "User-friendly error message"
}
```

**Logging**:
- Errors logged to console
- Generic messages returned to client (security)
- Detailed errors in server logs only

---

## File Processing

### PDF Parsing (pdfplumber)

```python
import pdfplumber

def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()
```

**Features**:
- Extracts text from all pages
- Preserves basic formatting
- Handles multi-column layouts
- Error handling for corrupted PDFs

### DOCX Parsing (python-docx)

```python
from docx import Document

def parse_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text
```

**Features**:
- Extracts text from paragraphs
- Preserves line breaks
- Handles formatted text
- Error handling for corrupted files

### Text File Parsing

```python
def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**Features**:
- UTF-8 encoding support
- Handles various line endings
- Error handling for encoding issues

---

## Document Generation

### PDF Generation (ReportLab)

**Key Components**:
- `SimpleDocTemplate`: Main document template
- `Paragraph`: Text with formatting
- `Table`: For contact info background
- `Spacer`: For spacing control
- `ParagraphStyle`: Reusable styles

**Hyperlink Support**:
```python
from reportlab.platypus import Paragraph

# LinkedIn link
contact_html = 'LinkedIn: <link href="https://linkedin.com/in/username" color="#FDC500">https://linkedin.com/in/username</link>'
para = Paragraph(contact_html, style)
```

**Features**:
- Clickable hyperlinks
- Custom fonts and colors
- Table-based backgrounds
- Precise spacing control
- Single-page optimization

### DOCX Generation (python-docx)

**Key Components**:
- `Document`: Main document object
- `Paragraph`: Text paragraphs
- `Run`: Formatted text runs
- `Hyperlink`: Clickable links (via XML)

**Hyperlink Support**:
```python
from docx.oxml import parse_xml

# Create hyperlink element
hyperlink = parse_xml(
    '<w:hyperlink r:id="rId1" xmlns:w="..."/>'
)
hyperlink_run = hyperlink.add_r()
hyperlink_run.text = url
hyperlink_run.rPr.color = RGBColor(253, 197, 0)  # Yellow
```

**Features**:
- Clickable hyperlinks
- Paragraph shading (black background)
- Custom fonts and colors
- Proper spacing and alignment
- Microsoft Word compatible

---

## Security & Production Features

### Security Measures

1. **Input Validation**:
   - Length limits (prevent DoS)
   - File size limits (10MB)
   - File type validation
   - Filename sanitization

2. **Error Handling**:
   - Generic error messages to clients
   - Detailed errors in server logs only
   - No stack traces exposed

3. **Rate Limiting**:
   - Prevents abuse
   - Protects API endpoints
   - Configurable limits

4. **CORS**:
   - Controlled cross-origin requests
   - Security headers

5. **Environment Variables**:
   - API keys stored in `.env`
   - Not committed to Git
   - `.gitignore` protection

### Production Features

1. **Production Mode Detection**:
   ```python
   if os.getenv('FLASK_ENV') == 'production' or os.getenv('ENVIRONMENT') == 'production':
       app.config['DEBUG'] = False
   ```

2. **Automatic Port Detection**:
   ```python
   def find_free_port():
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.bind(('', 0))
           return s.getsockname()[1]
   ```

3. **Health Check Endpoint**:
   ```python
   @app.route('/api/health')
   def health():
       return jsonify({'status': 'healthy'})
   ```

4. **Logging**:
   - Structured logging
   - Error tracking
   - Performance monitoring

---

## API Endpoints

### `GET /`
**Purpose**: Render main UI

**Response**: HTML page

---

### `POST /api/analyze`
**Purpose**: Analyze resume against job description

**Request Body**:
```json
{
  "resume_text": "Resume content...",
  "job_description": "Job description...",
  "provider": "groq",
  "api_key": "optional_api_key_override"
}
```

**Response**:
```json
{
  "success": true,
  "match_score": 65,
  "strengths": ["Strong technical skills", ...],
  "improvements_needed": ["Add more metrics", ...],
  "content_suggestions": ["Emphasize Python experience", ...],
  "show_optimization": true,
  "provider": "groq"
}
```

**Rate Limit**: 20 requests/minute

---

### `POST /api/optimize`
**Purpose**: Generate optimized resume

**Request Body**:
```json
{
  "resume_text": "Original resume...",
  "job_description": "Job description...",
  "suggestions": ["Add metrics", ...],
  "original_score": 65,
  "provider": "groq",
  "api_key": "optional_api_key_override"
}
```

**Response**:
```json
{
  "success": true,
  "optimized_resume": "Optimized resume text...",
  "original_resume": "Original resume text...",
  "provider": "groq",
  "score_comparison": {
    "original_score": 65,
    "new_score": 78,
    "improvement": 13,
    "improvement_percent": 20.0,
    "status": "improved",
    "status_message": "Score improved by 20.0%"
  },
  "section_breakdown": {
    "sections_improved": 3,
    "improvements": [...]
  },
  "additional_suggestions": {
    "provider": "claude",
    "suggestions": [...]
  }
}
```

**Rate Limit**: 10 requests/minute

---

### `POST /api/upload-resume`
**Purpose**: Upload and parse resume file

**Request**: Multipart form data
- `file`: Resume file (PDF, DOCX, TXT)

**Response**:
```json
{
  "success": true,
  "resume_text": "Extracted text...",
  "filename": "resume.pdf"
}
```

**Rate Limit**: 30 requests/hour

---

### `POST /api/download`
**Purpose**: Generate and download optimized resume

**Request Body**:
```json
{
  "resume_text": "Optimized resume...",
  "format": "pdf"
}
```

**Response**: File download (PDF, DOCX, or TXT)

**Rate Limit**: 30 requests/hour

---

### `GET /api/providers`
**Purpose**: Get available AI providers

**Response**:
```json
{
  "providers": [
    {
      "id": "groq",
      "name": "Groq",
      "available": true,
      "api_key_env": "GROQ_API_KEY"
    },
    ...
  ]
}
```

---

### `GET /api/health`
**Purpose**: Health check

**Response**:
```json
{
  "status": "healthy"
}
```

---

## Dependencies

### Core Dependencies

```
Flask==3.0.0                    # Web framework
flask-cors==4.0.0               # CORS support
flask-limiter==3.5.0            # Rate limiting
python-dotenv==1.0.0            # Environment variables
requests==2.31.0                # HTTP requests
```

### AI Provider Dependencies

```
groq==0.9.0                     # Groq API
openai==1.12.0                  # OpenAI API
anthropic==0.34.2               # Claude API
google-generativeai==0.8.3      # Gemini API
cohere==4.47                    # Cohere API
```

### File Processing Dependencies

```
pdfplumber==0.10.0              # PDF parsing
python-docx==1.1.0              # DOCX parsing/generation
reportlab==4.0.7                # PDF generation
```

### Optional Dependencies (for scalability)

```
celery==5.3.4                   # Task queue
redis==5.0.1                    # Cache/broker
prometheus-client==0.19.0       # Monitoring
python-json-logger==2.0.7       # Structured logging
```

### Development Dependencies

```
pytest==7.4.0                   # Testing (optional)
black==23.0.0                   # Code formatting (optional)
flake8==6.0.0                   # Linting (optional)
```

---

## Deployment Considerations

### Local Development

**Requirements**:
- Python 3.8+
- pip
- Virtual environment (recommended)

**Setup**:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run application
python app_web.py
```

**Access**: `http://localhost:5001` (or auto-detected port)

### Production Deployment

**Recommended Stack**:
- **Web Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Process Manager**: systemd or supervisor
- **Database**: PostgreSQL (if using database features)
- **Cache**: Redis (for rate limiting and caching)
- **Task Queue**: Celery + Redis (for bulk processing)

**Gunicorn Configuration**:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app_web:app
```

**Nginx Configuration**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Environment Variables**:
```bash
export FLASK_ENV=production
export GROQ_API_KEY=your_key
export OPENAI_API_KEY=your_key
# ... other API keys
```

### Docker Deployment (Optional)

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_web:app"]
```

**Docker Compose**:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./uploads:/app/uploads
```

### Scaling Considerations

1. **Horizontal Scaling**:
   - Multiple Gunicorn workers
   - Load balancer (Nginx)
   - Stateless application (no session storage)

2. **Caching**:
   - Redis for rate limiting
   - Cache optimization results
   - Reduce API calls

3. **Task Queue**:
   - Celery for background processing
   - Redis as broker
   - Separate worker processes

4. **Database** (if needed):
   - PostgreSQL for production
   - Connection pooling
   - Indexes for performance

---

## Future Enhancements

### Planned Features

1. **Database Integration**:
   - Store resume history
   - User accounts
   - Job description library
   - Analytics dashboard

2. **Advanced Features**:
   - Resume templates
   - ATS compatibility checker
   - Cover letter generation
   - Interview preparation

3. **Performance**:
   - Response caching
   - Batch processing
   - Async processing
   - CDN for static assets

4. **User Experience**:
   - Real-time preview
   - Undo/redo functionality
   - Export to multiple formats simultaneously
   - Resume comparison tool

5. **AI Enhancements**:
   - Custom prompt templates
   - Fine-tuned models
   - Multi-language support
   - Industry-specific optimization

---

## Conclusion

This Resume Optimization Application is a **production-ready, scalable solution** built with modern web technologies and AI integration. It provides a comprehensive platform for resume analysis and optimization with support for multiple AI providers, file formats, and export options.

### Key Strengths

- ✅ **Multi-AI Provider Support**: Flexible, unified interface
- ✅ **Production-Ready**: Security, rate limiting, error handling
- ✅ **User-Friendly**: Modern UI, intuitive workflow
- ✅ **Extensible**: Modular architecture, easy to extend
- ✅ **Well-Documented**: Comprehensive documentation

### Technology Highlights

- **Backend**: Python 3.8+, Flask 3.0.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Groq, OpenAI, Claude, Gemini, Cohere
- **File Processing**: pdfplumber, python-docx
- **Document Generation**: reportlab, python-docx
- **Security**: Rate limiting, input validation, CORS

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-27  
**Author**: Resume Optimization Team

