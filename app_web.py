"""
Resume Analyzer Web Application
Full web app with UI for analyzing and optimizing resumes.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load .env file manually if dotenv not available
def load_env_file():
    """Load environment variables from .env file."""
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip().strip('"').strip("'")
                        os.environ[key.strip()] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")

# Try to use python-dotenv, fallback to manual loading
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    load_env_file()  # Manual loading if dotenv not available

from utils.groq_optimizer import GroqResumeOptimizer
from utils.file_parser import parse_resume
from utils.ai_providers import get_ai_provider, get_provider_info

app = Flask(__name__)
CORS(app)

# Production configuration
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for downloads

# Rate limiting (if flask-limiter is available)
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"  # In-memory for simple setup (use Redis for production)
    )
    RATE_LIMITING_ENABLED = True
except ImportError:
    limiter = None
    RATE_LIMITING_ENABLED = False
    print("⚠️  Flask-Limiter not installed. Rate limiting disabled. Install with: pip install flask-limiter")

# Initialize optimizer (for backward compatibility)
groq_optimizer = GroqResumeOptimizer()

# Input validation constants
MAX_RESUME_LENGTH = 50000  # 50K characters max
MAX_JOB_DESCRIPTION_LENGTH = 20000  # 20K characters max
MIN_RESUME_LENGTH = 50  # Minimum resume length
MIN_JOB_DESCRIPTION_LENGTH = 20  # Minimum job description length


def analyze_resume_match(resume_text, job_description, provider_name="groq", api_key=None):
    """
    Analyze resume against job description using selected AI provider.
    Returns match score and content-based suggestions.
    """
    # Input validation
    if not resume_text or not isinstance(resume_text, str):
        return {
            "error": "Resume text is required and must be a string.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    if not job_description or not isinstance(job_description, str):
        return {
            "error": "Job description is required and must be a string.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    # Length validation
    if len(resume_text) < MIN_RESUME_LENGTH:
        return {
            "error": f"Resume text is too short. Minimum {MIN_RESUME_LENGTH} characters required.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    if len(resume_text) > MAX_RESUME_LENGTH:
        return {
            "error": f"Resume text is too long. Maximum {MAX_RESUME_LENGTH} characters allowed.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    if len(job_description) < MIN_JOB_DESCRIPTION_LENGTH:
        return {
            "error": f"Job description is too short. Minimum {MIN_JOB_DESCRIPTION_LENGTH} characters required.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    if len(job_description) > MAX_JOB_DESCRIPTION_LENGTH:
        return {
            "error": f"Job description is too long. Maximum {MAX_JOB_DESCRIPTION_LENGTH} characters allowed.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    # Get the selected AI provider
    provider = get_ai_provider(provider_name, api_key)
    
    if not provider:
        return {
            "error": f"AI provider '{provider_name}' not found or not available.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    if not provider.is_available():
        provider_info = next((p for p in get_provider_info() if p["id"] == provider_name), None)
        api_key_env = provider_info["api_key_env"] if provider_info else "API_KEY"
        return {
            "error": f"{provider_name.upper()} API is not available. Please set {api_key_env} environment variable.",
            "match_score": 0,
            "strengths": [],
            "improvements_needed": [],
            "content_suggestions": [],
            "show_optimization": False
        }
    
    try:
        # Use the provider to analyze
        result = provider.analyze_resume(resume_text, job_description)
        
        if "error" in result:
            return {
                "error": result["error"],
                "match_score": 0,
                "strengths": [],
                "improvements_needed": [],
                "content_suggestions": [],
                "show_optimization": False
            }
        
        analysis_text = result.get("raw_analysis", "")
        parsed = parse_analysis(analysis_text, resume_text, job_description)
        parsed["provider"] = result.get("provider", provider_name)
        return parsed
        
    except Exception as e:
        return {"error": f"Error analyzing resume with {provider_name}: {str(e)}"}


def parse_analysis(analysis_text, resume_text, job_description):
    """Parse the Groq analysis response into structured format."""
    result = {
        "match_score": 0,
        "strengths": [],
        "improvements_needed": [],
        "content_suggestions": [],
        "show_optimization": False,
        "raw_analysis": analysis_text
    }
    
    # Extract match score - try multiple formats
    score_found = False
    
    # Try format: MATCH_SCORE: 85 or MATCH_SCORE:85
    if "MATCH_SCORE" in analysis_text.upper():
        try:
            import re
            # Look for MATCH_SCORE: followed by a number
            pattern = r'MATCH_SCORE[:\s]+(\d+)'
            match = re.search(pattern, analysis_text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                # Ensure score is in valid range and not inflated
                if 0 <= score <= 100:
                    result["match_score"] = score
                    score_found = True
        except Exception as e:
            pass
    
    # Try format: Match Score: 85% or match score is 85
    if not score_found:
        try:
            import re
            # Look for patterns like "85%", "score: 85", "85 percent", etc.
            patterns = [
                r'match\s+score[:\s]+(\d+)',
                r'score[:\s]+(\d+)',
                r'(\d+)\s*%',
                r'(\d+)\s+out\s+of\s+100',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, analysis_text, re.IGNORECASE)
                if matches:
                    score = float(matches[0])
                    if 0 <= score <= 100:
                        result["match_score"] = score
                        score_found = True
                        break
        except:
            pass
    
    # If still no score found, calculate a reasonable default based on content
    if not score_found:
        # Fallback: intelligent keyword matching
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract important keywords (tech skills, tools, etc.)
        tech_keywords = {
            'python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 
            'kubernetes', 'sql', 'mongodb', 'postgresql', 'git', 'agile', 
            'scrum', 'typescript', 'angular', 'vue', 'spring', 'django', 
            'flask', 'express', 'redis', 'jenkins', 'ci/cd', 'microservices',
            'azure', 'gcp', 'terraform', 'ansible', 'linux', 'unix'
        }
        
        # Find matching tech keywords
        job_tech = {kw for kw in tech_keywords if kw in job_lower}
        resume_tech = {kw for kw in tech_keywords if kw in resume_lower}
        
        # Calculate base score from tech overlap
        if job_tech:
            tech_match = len(job_tech & resume_tech) / len(job_tech)
            base_score = int(tech_match * 100)
        else:
            # No tech keywords, use general word overlap
            job_words = set(re.findall(r'\b\w{5,}\b', job_lower))
            resume_words = set(re.findall(r'\b\w{5,}\b', resume_lower))
            if job_words:
                word_match = len(job_words & resume_words) / len(job_words)
                base_score = int(word_match * 100)
            else:
                base_score = 30
        
        # Adjust for experience level mismatch
        if 'senior' in job_lower and 'senior' not in resume_lower and 'junior' in resume_lower:
            base_score = max(0, base_score - 30)
        elif 'junior' in job_lower and 'senior' in resume_lower:
            base_score = min(100, base_score + 20)
        
        # Penalize for very short resumes
        if len(resume_text) < 200:
            base_score = max(0, base_score - 20)
        
        result["match_score"] = max(5, min(95, base_score))
    
    # Extract strengths
    if "STRENGTHS:" in analysis_text:
        strengths_section = analysis_text.split("STRENGTHS:")[1]
        if "IMPROVEMENTS_NEEDED:" in strengths_section:
            strengths_section = strengths_section.split("IMPROVEMENTS_NEEDED:")[0]
        
        strengths = [
            line.strip().lstrip("- ").strip()
            for line in strengths_section.split("\n")
            if line.strip() and line.strip().startswith("-")
        ]
        result["strengths"] = strengths[:10]
    
    # Extract improvements needed
    if "IMPROVEMENTS_NEEDED:" in analysis_text:
        improvements_section = analysis_text.split("IMPROVEMENTS_NEEDED:")[1]
        if "CONTENT_SUGGESTIONS:" in improvements_section:
            improvements_section = improvements_section.split("CONTENT_SUGGESTIONS:")[0]
        
        improvements = [
            line.strip().lstrip("- ").strip()
            for line in improvements_section.split("\n")
            if line.strip() and line.strip().startswith("-")
        ]
        result["improvements_needed"] = improvements[:10]
    
    # Extract content suggestions
    if "CONTENT_SUGGESTIONS:" in analysis_text:
        suggestions_section = analysis_text.split("CONTENT_SUGGESTIONS:")[1]
        
        suggestions = []
        for line in suggestions_section.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                clean_line = line.lstrip("0123456789.-) ").strip()
                if clean_line and len(clean_line) > 20:
                    suggestions.append(clean_line)
        
        result["content_suggestions"] = suggestions[:15]
    
    result["show_optimization"] = result["match_score"] < 70
    
    return result


def get_dummy_analysis(resume_text, job_description):
    """Generate realistic dummy analysis for testing when Groq API is not available."""
    import re
    import time
    time.sleep(0.5)  # Simulate processing time for smooth UX
    
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Extended keyword lists
    tech_keywords = {
        'python': ['python', 'django', 'flask', 'pandas', 'numpy'],
        'javascript': ['javascript', 'js', 'node', 'nodejs', 'express'],
        'react': ['react', 'reactjs', 'redux', 'next.js'],
        'java': ['java', 'spring', 'hibernate', 'maven'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud', 's3', 'ec2', 'lambda'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
        'devops': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'git'],
        'frontend': ['html', 'css', 'typescript', 'angular', 'vue'],
        'mobile': ['ios', 'android', 'react native', 'swift', 'kotlin']
    }
    
    # Calculate match score more intelligently
    resume_keywords_found = []
    job_keywords_found = []
    
    for category, keywords in tech_keywords.items():
        for keyword in keywords:
            if keyword in resume_lower:
                resume_keywords_found.append(category)
                break
        for keyword in keywords:
            if keyword in job_lower:
                job_keywords_found.append(category)
                break
    
    # Calculate match
    matched_categories = set(resume_keywords_found) & set(job_keywords_found)
    total_job_categories = len(set(job_keywords_found))
    
    if total_job_categories > 0:
        # Calculate percentage match
        match_ratio = len(matched_categories) / total_job_categories
        base_score = int(match_ratio * 100)
        
        # If no matches at all, give very low score
        if len(matched_categories) == 0:
            base_score = max(0, base_score - 20)
    else:
        # No tech keywords in job, check general relevance
        if len(resume_text) < 100:
            base_score = 20  # Very short resume
        else:
            base_score = 40  # Default for non-tech jobs
    
    # Adjust for experience level
    experience_keywords = {
        'senior': ['senior', 'lead', 'principal', 'architect', '5+', '7+', '10+'],
        'mid': ['mid', 'intermediate', '3+', '4+'],
        'junior': ['junior', 'entry', 'graduate', 'intern', '0-2', '1+']
    }
    
    job_level = None
    resume_level = None
    
    for level, keywords in experience_keywords.items():
        if any(kw in job_lower for kw in keywords):
            job_level = level
        if any(kw in resume_lower for kw in keywords):
            resume_level = level
    
    # Level matching adjustments
    if job_level == 'senior' and resume_level != 'senior':
        base_score = max(0, base_score - 20)
    elif job_level == 'junior' and resume_level == 'senior':
        base_score = min(100, base_score + 15)
    elif job_level == resume_level:
        base_score = min(100, base_score + 10)
    
    # Boost for strong matches
    if len(matched_categories) >= total_job_categories * 0.7 and total_job_categories > 0:
        base_score = min(100, base_score + 15)
    
    # Ensure reasonable range - but don't cap at 95, allow full range
    match_score = max(0, min(100, base_score))
    
    # Generate contextual suggestions
    missing_categories = set(job_keywords_found) - set(resume_keywords_found)
    
    if match_score < 70:
        suggestions = []
        improvements = []
        strengths = []
        
        # Strengths
        if matched_categories:
            strengths.append(f"Strong foundation in {', '.join(list(matched_categories)[:3])}")
        if 'experience' in resume_lower or 'worked' in resume_lower or 'developed' in resume_lower:
            strengths.append("Demonstrated work experience with relevant technologies")
        if any(word in resume_lower for word in ['project', 'led', 'managed', 'team']):
            strengths.append("Leadership and project management experience")
        if not strengths:
            strengths = ["Solid technical background", "Relevant educational foundation"]
        
        # Improvements
        if missing_categories:
            missing_list = list(missing_categories)[:2]
            improvements.append(f"Add experience or skills related to: {', '.join(missing_list)}")
        if 'quantify' not in resume_lower and 'improved' not in resume_lower and '%' not in resume_text:
            improvements.append("Add quantifiable achievements and metrics to demonstrate impact")
        if len(resume_text) < 500:
            improvements.append("Expand experience descriptions with more detail and context")
        if not improvements:
            improvements = ["Enhance content to better match job requirements"]
        
        # Suggestions
        if missing_categories:
            cat = list(missing_categories)[0]
            suggestions.append(f"Experience Section: Add a project or role highlighting your {cat} experience. Include specific technologies, your contributions, and measurable outcomes.")
        
        suggestions.append("Skills Section: Reorder your skills list to prioritize technologies mentioned in the job description. Add any relevant tools or frameworks you've used.")
        
        if 'summary' not in resume_lower[:200] and 'objective' not in resume_lower[:200]:
            suggestions.append("Summary Section: Add a professional summary at the top that highlights your most relevant experience for this role. Keep it concise (2-3 lines) and impactful.")
        else:
            suggestions.append("Summary Section: Tailor your existing summary to emphasize the experience and skills most relevant to this specific role.")
        
        suggestions.append("Achievements: Add bullet points with quantifiable results. For example: 'Increased system performance by 40%' or 'Led a team of 5 developers to deliver project 2 weeks ahead of schedule'.")
        
        if 'action' not in resume_lower or not any(verb in resume_lower for verb in ['developed', 'created', 'implemented', 'designed', 'built']):
            suggestions.append("Action Verbs: Start bullet points with strong action verbs like 'Developed', 'Implemented', 'Designed', 'Led', 'Optimized' to make your experience more impactful.")
        
    else:
        suggestions = [
            "Your resume is well-matched! Consider minor refinements: emphasize your strongest relevant experiences and ensure all key technologies are prominently featured."
        ]
        improvements = []
        strengths = [
            "Excellent alignment with job requirements",
            "Strong technical skills match",
            "Relevant experience and qualifications"
        ]
    
    return {
        "match_score": match_score,
        "strengths": strengths[:4],
        "improvements_needed": improvements[:3],
        "content_suggestions": suggestions[:5],
        "show_optimization": match_score < 70,
        "raw_analysis": f"Analysis complete - Match Score: {match_score}%"
    }


def analyze_section_improvements(original_resume, optimized_resume, job_description):
    """Analyze which sections improved between original and optimized resume."""
    import re
    
    sections = {
        'SUMMARY': {'original': '', 'optimized': '', 'improved': False},
        'SKILLS': {'original': '', 'optimized': '', 'improved': False},
        'EXPERIENCE': {'original': '', 'optimized': '', 'improved': False},
        'EDUCATION': {'original': '', 'optimized': '', 'improved': False},
        'PROJECTS': {'original': '', 'optimized': '', 'improved': False}
    }
    
    # Extract sections from both resumes
    for section_name in sections.keys():
        # Extract from original
        pattern = rf'{section_name}[:\s]*\n(.*?)(?=\n(?:{"|".join(sections.keys())})[:\s]*\n|\Z)'
        match = re.search(pattern, original_resume, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section_name]['original'] = match.group(1).strip()
        
        # Extract from optimized
        match = re.search(pattern, optimized_resume, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section_name]['optimized'] = match.group(1).strip()
    
    # Analyze improvements
    job_lower = job_description.lower()
    improvements = []
    
    for section_name, section_data in sections.items():
        original = section_data['original'].lower()
        optimized = section_data['optimized'].lower()
        
        if not original or not optimized:
            continue
        
        # Check for keyword improvements
        job_keywords = set(re.findall(r'\b\w{4,}\b', job_lower))
        original_keywords = set(re.findall(r'\b\w{4,}\b', original))
        optimized_keywords = set(re.findall(r'\b\w{4,}\b', optimized))
        
        original_matches = len(job_keywords & original_keywords)
        optimized_matches = len(job_keywords & optimized_keywords)
        
        if optimized_matches > original_matches:
            section_data['improved'] = True
            improvements.append({
                'section': section_name,
                'improvement': f"Added {optimized_matches - original_matches} more relevant keywords",
                'keywords_added': list((job_keywords & optimized_keywords) - (job_keywords & original_keywords))[:5]
            })
        
        # Check for length/content improvements
        if len(optimized) > len(original) * 1.2 and section_name in ['EXPERIENCE', 'SUMMARY']:
            section_data['improved'] = True
            if not any(imp['section'] == section_name for imp in improvements):
                improvements.append({
                    'section': section_name,
                    'improvement': "Enhanced with more detailed descriptions",
                    'keywords_added': []
                })
    
    return {
        'sections': sections,
        'improvements': improvements,
        'total_sections_improved': sum(1 for s in sections.values() if s['improved'])
    }


def create_optimized_resume(resume_text, job_description, suggestions, provider_name="groq", api_key=None):
    """Create optimized resume based on suggestions using selected AI provider."""
    # Extract LinkedIn and GitHub links from original resume
    social_links = extract_social_links(resume_text)
    
    # Get the selected AI provider
    provider = get_ai_provider(provider_name, api_key)
    
    if not provider:
        return {
            "error": f"AI provider '{provider_name}' not found or not available.",
            "optimized_resume": "",
            "original_resume": resume_text
        }
    
    if not provider.is_available():
        provider_info = next((p for p in get_provider_info() if p["id"] == provider_name), None)
        api_key_env = provider_info["api_key_env"] if provider_info else "API_KEY"
        return {
            "error": f"{provider_name.upper()} API is not available. Please set {api_key_env} environment variable.",
            "optimized_resume": "",
            "original_resume": resume_text
        }
    
    try:
        # Use the provider to optimize
        optimized_resume = provider.optimize_resume(resume_text, job_description, suggestions, social_links)
        
        # Clean up the response
        if "OPTIMIZED RESUME:" in optimized_resume:
            optimized_resume = optimized_resume.split("OPTIMIZED RESUME:")[-1].strip()
        elif "RESUME:" in optimized_resume:
            optimized_resume = optimized_resume.split("RESUME:")[-1].strip()
        
        return {
            "optimized_resume": optimized_resume,
            "original_resume": resume_text,
            "provider": provider_name
        }
        
    except Exception as e:
        return {
            "error": f"Error creating optimized resume with {provider_name}: {str(e)}",
            "optimized_resume": "",
            "original_resume": resume_text
        }


def get_dummy_optimized_resume(resume_text, job_description, suggestions):
    """Generate realistic optimized resume for testing."""
    import re
    import time
    time.sleep(0.8)  # Simulate processing time
    
    # Create an improved version with actual enhancements
    optimized_lines = resume_text.split('\n')
    improved_lines = []
    
    # Add summary if missing
    if not any(word in resume_text[:300].lower() for word in ['summary', 'objective', 'profile']):
        job_lower = job_description.lower()
        # Extract key technologies from job
        key_techs = []
        for tech in ['python', 'javascript', 'react', 'java', 'aws', 'docker', 'sql']:
            if tech in job_lower:
                key_techs.append(tech.title())
        
        if key_techs:
            summary = f"PROFESSIONAL SUMMARY\nExperienced software engineer with expertise in {', '.join(key_techs[:3])}. Proven track record of developing scalable solutions and leading technical initiatives."
            improved_lines.append(summary)
            improved_lines.append("")
    
    # Enhance existing content
    for i, line in enumerate(optimized_lines):
        original_line = line
        
        # Enhance bullet points with action verbs
        if line.strip().startswith('-') or line.strip().startswith('•'):
            line = line.strip()
            if not any(verb in line.lower() for verb in ['developed', 'created', 'implemented', 'designed', 'built', 'led', 'optimized']):
                if 'improved' not in line.lower() and 'increased' not in line.lower():
                    # Add action verb
                    if 'application' in line.lower() or 'system' in line.lower():
                        line = line.replace('-', '- Developed', 1) if line.startswith('-') else line.replace('•', '• Developed', 1)
                    elif 'team' in line.lower():
                        line = line.replace('-', '- Led', 1) if line.startswith('-') else line.replace('•', '• Led', 1)
            
            # Add metrics if missing
            if '%' not in line and 'improved' not in line.lower() and 'increased' not in line.lower():
                if 'performance' in line.lower() or 'efficiency' in line.lower():
                    line += " by 30-40%"
                elif 'team' in line.lower() or 'managed' in line.lower():
                    line += " resulting in improved productivity"
        
        # Enhance experience headers
        if any(word in line.lower() for word in ['experience', 'work', 'employment']) and ':' in line:
            if 'years' not in line.lower() and any(char.isdigit() for char in line):
                pass  # Already has years
            elif 'experience' in line.lower():
                line = line.replace('Experience', 'Professional Experience', 1)
        
        improved_lines.append(line)
    
    optimized = '\n'.join(improved_lines)
    
    # Add optimization notes at the end
    notes = "\n\n--- OPTIMIZATION NOTES ---\n"
    notes += "✓ Enhanced experience descriptions with stronger action verbs\n"
    notes += "✓ Added quantifiable achievements where applicable\n"
    notes += "✓ Improved content structure and flow\n"
    notes += "✓ Tailored content to better match job requirements\n"
    notes += "\nNote: This is an enhanced version. For AI-powered optimization, set GROQ_API_KEY environment variable."
    
    optimized += notes
    
    return {
        "optimized_resume": optimized,
        "original_resume": resume_text
    }


@app.route('/')
def index():
    """Main application page."""
    return render_template('resume_analyzer.html')


@app.route('/api/analyze', methods=['POST'])
@limiter.limit("20 per minute") if RATE_LIMITING_ENABLED else lambda f: f
def analyze():
    """Analyze resume against job description."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        provider_name = data.get('provider', 'groq').lower()
        api_key = data.get('api_key')  # Optional API key override
        
        # Input validation
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description are required'
            }), 400
        
        analysis = analyze_resume_match(resume_text, job_description, provider_name, api_key)
        
        if 'error' in analysis:
            return jsonify({
                'success': False,
                'error': analysis['error']
            }), 500
        
        return jsonify({
            'success': True,
            'match_score': analysis['match_score'],
            'show_optimization': analysis['show_optimization'],
            'strengths': analysis['strengths'],
            'improvements_needed': analysis['improvements_needed'],
            'content_suggestions': analysis['content_suggestions'],
            'message': 'Resume is well-matched!' if analysis['match_score'] >= 70 
                      else 'Resume needs optimization to better match this job.'
        })
        
    except Exception as e:
        # Log error but don't expose internal details
        import logging
        logging.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing the resume. Please try again.'
        }), 500


@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get list of available AI providers."""
    try:
        providers = get_provider_info()
        return jsonify({
            'success': True,
            'providers': providers
        })
    except Exception as e:
        # Log error but don't expose internal details
        import logging
        logging.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing the resume. Please try again.'
        }), 500


@app.route('/api/optimize', methods=['POST'])
@limiter.limit("10 per minute") if RATE_LIMITING_ENABLED else lambda f: f
def optimize():
    """Optimize resume based on analysis with automatic score comparison."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        suggestions = data.get('suggestions', [])
        provider_name = data.get('provider', 'groq').lower()
        api_key = data.get('api_key')  # Optional API key override
        original_score = data.get('original_score')  # Original match score from analysis
        
        # Input validation
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description are required'
            }), 400
        
        # Length validation
        if len(resume_text) > MAX_RESUME_LENGTH:
            return jsonify({
                'success': False,
                'error': f'Resume text is too long. Maximum {MAX_RESUME_LENGTH} characters allowed.'
            }), 400
        
        if len(job_description) > MAX_JOB_DESCRIPTION_LENGTH:
            return jsonify({
                'success': False,
                'error': f'Job description is too long. Maximum {MAX_JOB_DESCRIPTION_LENGTH} characters allowed.'
            }), 400
        
        if not suggestions:
            analysis = analyze_resume_match(resume_text, job_description, provider_name, api_key)
            if 'error' in analysis:
                return jsonify({
                    'success': False,
                    'error': analysis['error']
                }), 500
            suggestions = analysis.get('content_suggestions', [])
            # Get original score if not provided
            if original_score is None:
                original_score = analysis.get('match_score', 0)
        
        # Create optimized resume
        result = create_optimized_resume(resume_text, job_description, suggestions, provider_name, api_key)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        optimized_resume = result['optimized_resume']
        
        # Re-analyze optimized resume to get new score
        new_analysis = analyze_resume_match(optimized_resume, job_description, provider_name, api_key)
        new_score = new_analysis.get('match_score', 0) if 'error' not in new_analysis else 0
        
        # Calculate improvement
        if original_score is None:
            original_score = 0
        
        improvement = new_score - original_score
        improvement_percent = (improvement / original_score * 100) if original_score > 0 else 0
        
        # Analyze section-by-section improvements
        section_analysis = analyze_section_improvements(resume_text, optimized_resume, job_description)
        
        # Determine improvement status
        if improvement > 20:
            status = "significant_improvement"
            status_message = "Significant Improvement! 🎉"
        elif improvement > 10:
            status = "moderate_improvement"
            status_message = "Moderate Improvement ✓"
        elif improvement > 0:
            status = "minor_improvement"
            status_message = "Minor Improvement"
        elif improvement == 0:
            status = "no_change"
            status_message = "No Change"
        else:
            status = "decreased"
            status_message = "Score Decreased"
        
        # If new score < 60%, try with different provider for additional suggestions
        additional_suggestions = []
        fallback_provider = None
        
        if new_score < 60 and provider_name != 'claude':
            # Try Claude as fallback (usually more thorough)
            fallback_providers = ['claude', 'gemini', 'openai']
            for fallback_name in fallback_providers:
                if fallback_name != provider_name:
                    fallback_provider_obj = get_ai_provider(fallback_name)
                    if fallback_provider_obj and fallback_provider_obj.is_available():
                        try:
                            # Get additional analysis from fallback provider
                            fallback_analysis = analyze_resume_match(
                                optimized_resume, 
                                job_description, 
                                fallback_name
                            )
                            if 'error' not in fallback_analysis:
                                additional_suggestions = fallback_analysis.get('content_suggestions', [])[:5]
                                fallback_provider = fallback_name
                                break
                        except Exception:
                            continue
        
        response_data = {
            'success': True,
            'optimized_resume': optimized_resume,
            'original_resume': result['original_resume'],
            'provider': result.get('provider', provider_name),
            'score_comparison': {
                'original_score': original_score,
                'new_score': new_score,
                'improvement': improvement,
                'improvement_percent': round(improvement_percent, 1),
                'status': status,
                'status_message': status_message
            },
            'section_breakdown': {
                'sections_improved': section_analysis['total_sections_improved'],
                'improvements': section_analysis['improvements']
            }
        }
        
        # Add fallback suggestions if available
        if additional_suggestions:
            response_data['additional_suggestions'] = {
                'provider': fallback_provider,
                'suggestions': additional_suggestions,
                'message': f'Score is below 60%. Here are additional suggestions from {fallback_provider.upper()}:'
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        # Log error but don't expose internal details
        import logging
        logging.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing the resume. Please try again.'
        }), 500


@app.route('/api/upload-resume', methods=['POST'])
@limiter.limit("30 per hour") if RATE_LIMITING_ENABLED else lambda f: f
def upload_resume():
    """Upload and parse resume file."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
            }), 400
        
        # Check file size (additional check beyond Flask's MAX_CONTENT_LENGTH)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.1f}MB'
            }), 400
        
        # Validate filename (prevent path traversal)
        import re
        if not re.match(r'^[a-zA-Z0-9._-]+$', os.path.basename(file.filename)):
            return jsonify({
                'success': False,
                'error': 'Invalid filename. Only alphanumeric characters, dots, dashes, and underscores are allowed.'
            }), 400
        
        # Save file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Parse the resume
            resume_text = parse_resume(tmp_path)
            
            if not resume_text or len(resume_text.strip()) < 50:
                return jsonify({
                    'success': False,
                    'error': 'Could not extract text from file. Please ensure the file is not corrupted.'
                }), 400
            
            return jsonify({
                'success': True,
                'resume_text': resume_text,
                'filename': file.filename
            })
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
    except Exception as e:
        # Log error but don't expose internal details to user
        import logging
        logging.error(f"Error processing file upload: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error processing file. Please ensure the file is valid and try again.'
        }), 500


def format_resume_line(line, prev_line_type=None, line_index=0, header_processed=False):
    """Parse and categorize a resume line for proper formatting."""
    line = line.strip()
    if not line:
        return {'type': 'empty', 'text': ''}
    
    # Main section headers (all caps, common resume sections)
    main_sections = ['CONTACT', 'PROFESSIONAL SUMMARY', 'SUMMARY', 'OBJECTIVE', 'EXPERIENCE', 
                     'WORK EXPERIENCE', 'EDUCATION', 'SKILLS', 'TECHNICAL SKILLS', 'CERTIFICATIONS',
                     'PROJECTS', 'ACHIEVEMENTS', 'AWARDS', 'PUBLICATIONS', 'LANGUAGES', 'REFERENCES']
    
    # Header detection (first 2-3 lines) - Only check if header not yet processed
    # This ensures we catch all header lines but don't interfere with experience entries
    if not header_processed and line_index < 3:
        # Check if it's contact info first (can be on line 2 or 3)
        is_contact_info = ('|' in line or 
                          'location:' in line.lower() or 
                          'email:' in line.lower() or 
                          'phone:' in line.lower() or
                          'linkedin:' in line.lower() or
                          'github:' in line.lower() or
                          'linkedin.com' in line.lower() or
                          'github.com' in line.lower())
        
        # First line - Name (if not a section header and not contact info)
        if line_index == 0:
            if (line.upper() not in main_sections and 
                not is_contact_info and
                not line.startswith(('•', '-', '*', '·'))):
                return {'type': 'header_name', 'text': line}
        # Second line - Could be Job Title OR Contact Info
        elif line_index == 1:
            if is_contact_info:
                if line.upper() not in main_sections and not line.startswith(('•', '-', '*', '·')):
                    return {'type': 'header_contact', 'text': line}
            else:
                # Job Title (if not contact info and not section header)
                if (line.upper() not in main_sections and 
                    not line.startswith(('•', '-', '*', '·'))):
                    return {'type': 'header_title', 'text': line}
        # Third line - Contact Info (if not already processed)
        elif line_index == 2:
            if is_contact_info:
                if line.upper() not in main_sections and not line.startswith(('•', '-', '*', '·')):
                    return {'type': 'header_contact', 'text': line}
    
    # Check if it's a main section header
    if line.upper() in main_sections or (line.isupper() and len(line.split()) <= 3 and not line.endswith(':')):
        return {'type': 'main_section', 'text': line}
    
    # Bullet points (check before experience entry to avoid confusion)
    if line.startswith(('•', '-', '*', '·')):
        return {'type': 'bullet', 'text': line.lstrip('•-*· ')}
    
    # Category headers within sections (ends with colon, not all caps, or specific patterns)
    if line.endswith(':') and not line.isupper() and len(line) < 60:
        return {'type': 'category', 'text': line}
    
    # Experience entry detection: Contains "|" and date patterns (e.g., "Company, Location | Jan 2020 - Dec 2022 | Job Title")
    # Check if it looks like an experience entry (has pipe separator and date patterns)
    import re
    has_pipe = '|' in line
    
    # More comprehensive date pattern matching
    date_patterns = [
        r'\d{4}',  # Years like 2022, 2025
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # "Mar 2022", "January 2022"
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
        r'\d{1,2}[/-]\d{4}',  # "03/2022", "3-2022"
        r'Current|Present'  # Current employment indicators
    ]
    
    has_date_pattern = any(re.search(pattern, line, re.IGNORECASE) for pattern in date_patterns)
    
    # Project entry detection: Check if we're in PROJECTS section
    # We need to track the current section - this will be done by the caller
    # For now, we'll detect project entries as lines with "|" that come right after PROJECTS section
    # Project entries format: "Project Name | Technologies | Date/Duration"
    # They may or may not have full date patterns like experience entries
    
    # Check if previous line was PROJECTS section header
    # We'll use a simple heuristic: if prev_line_type is 'main_section' and the text was "PROJECTS"
    # Actually, we need to pass the previous line text, not just type
    # For now, let's detect project entries as lines with "|" that don't match experience patterns
    
    # Experience entry: has pipe AND date pattern, AND not a bullet point, AND not contact info
    # Don't require prev_line_type to be specific - experience entries can follow other experience entries
    if (has_pipe and has_date_pattern and 
        not line.startswith(('•', '-', '*', '·')) and
        not ('email:' in line.lower() and 'phone:' in line.lower()) and  # Not contact info
        len(line) > 20):  # Reasonable length for experience entry
        # Additional check: make sure it's not just contact info
        # Contact info usually has "Location:" or multiple contact fields together
        is_likely_contact = (
            line.lower().count('location:') > 0 and 
            (line.lower().count('email:') > 0 or line.lower().count('phone:') > 0)
        )
        if not is_likely_contact:
            return {'type': 'experience_entry', 'text': line}
    
    # Project entry detection: Lines with "|" that might be project entries
    # Project entries typically come after PROJECTS section and have format: "Project Name | Technologies | Date"
    # They may have dates but are less likely to have company-like words
    if (has_pipe and 
        not line.startswith(('•', '-', '*', '·')) and
        len(line) > 15 and  # Reasonable length
        not ('email:' in line.lower() and 'phone:' in line.lower()) and
        not ('location:' in line.lower() and 'email:' in line.lower())):
        # Check if it looks like a project entry (has "|" but doesn't have strong company indicators)
        # Project entries are less likely to have words like "Company", "Corporation", "Inc", "LLC", "Client:"
        has_company_indicators = any(word in line.lower() for word in ['company', 'corporation', 'inc', 'llc', 'ltd', 'client:', 'client'])
        # If it has "|" but doesn't have company indicators and doesn't have strong date patterns, it might be a project
        # OR if prev_line_type suggests we're in PROJECTS section
        # We'll need to track this in the calling function - for now, let's add a simple check
        # Actually, the best approach is to track current_section in the download function
        # For now, we'll return project_entry for lines with "|" that don't match experience patterns
        # and don't have company indicators
        if not has_company_indicators:
            # This could be a project entry - we'll let the caller decide based on current section
            # For now, return as normal and let the caller handle it
            pass
    
    # Regular text
    return {'type': 'normal', 'text': line}


@app.route('/api/download', methods=['POST'])
def download_resume():
    """Download optimized resume in PDF, DOCX, or TXT format."""
    try:
        data = request.get_json()
        
        if not data or not data.get('resume_text'):
            return jsonify({'success': False, 'error': 'No resume content provided'}), 400
        
        from flask import Response
        import io
        
        resume_text = data.get('resume_text', '')
        file_format = data.get('format', 'txt').lower()  # pdf, docx, or txt
        
        if file_format == 'pdf':
            # Generate PDF
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.enums import TA_LEFT
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                from reportlab.lib.colors import black, white
                import re
                
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter,
                                      rightMargin=72, leftMargin=72,
                                      topMargin=72, bottomMargin=18)
                
                # Container for the 'Flowable' objects
                elements = []
                
                # Define styles
                styles = getSampleStyleSheet()
                
                from reportlab.lib.enums import TA_CENTER
                
                # Header styles (centered, larger, bold) - matching the image format
                header_name_style = ParagraphStyle(
                    'HeaderName',
                    parent=styles['Heading1'],
                    fontSize=20,
                    textColor='#000000',
                    spaceAfter=4,
                    spaceBefore=0,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold',
                    leading=24
                )
                
                header_title_style = ParagraphStyle(
                    'HeaderTitle',
                    parent=styles['Normal'],
                    fontSize=15,
                    textColor='#000000',
                    spaceAfter=6,
                    spaceBefore=0,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold',
                    leading=18
                )
                
                header_contact_style = ParagraphStyle(
                    'HeaderContact',
                    parent=styles['Normal'],
                    fontSize=11,
                    textColor='#FFFFFF',  # White text
                    backColor='#000000',  # Black background
                    spaceAfter=14,
                    spaceBefore=0,
                    alignment=TA_CENTER,
                    fontName='Helvetica',
                    leading=14,
                    fontStyle='normal'
                )
                
                # Main section header style (SKILLS, EXPERIENCE, etc.)
                main_section_style = ParagraphStyle(
                    'MainSection',
                    parent=styles['Heading1'],
                    fontSize=13,
                    textColor='#000000',  # Black color instead of maroon
                    spaceAfter=4,
                    spaceBefore=10,
                    alignment=TA_LEFT,
                    fontName='Helvetica-Bold'
                )
                
                # Category header style (Data Engineering:, Cloud & Big Data:, etc.)
                category_style = ParagraphStyle(
                    'Category',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor='#000000',
                    spaceAfter=1,
                    spaceBefore=3,
                    alignment=TA_LEFT,
                    fontName='Helvetica-Bold',
                    leftIndent=0
                )
                
                # Experience entry style (Company, Location | Dates | Job Title)
                experience_entry_style = ParagraphStyle(
                    'ExperienceEntry',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor='#000000',
                    spaceAfter=1,
                    spaceBefore=3,
                    alignment=TA_LEFT,
                    fontName='Helvetica-Bold',
                    leftIndent=0,
                    rightIndent=0,
                    firstLineIndent=0
                )
                
                # Project entry style (Project Name | Technologies | Date)
                project_entry_style = ParagraphStyle(
                    'ProjectEntry',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor='#000000',  # Black color instead of maroon
                    spaceAfter=1,
                    spaceBefore=3,
                    alignment=TA_LEFT,
                    fontName='Helvetica-Bold',  # Bold
                    leftIndent=0,
                    rightIndent=0,
                    firstLineIndent=0
                )
                
                # Bullet point style - aligned with company name (matching Word format)
                bullet_style = ParagraphStyle(
                    'Bullet',
                    parent=styles['Normal'],
                    fontSize=10,
                    leading=12,
                    spaceAfter=1,
                    spaceBefore=0,
                    leftIndent=0,
                    rightIndent=0,
                    firstLineIndent=0,
                    bulletIndent=0,
                    alignment=TA_LEFT,
                    fontName='Helvetica'
                )
                
                # Normal text style
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontSize=10,
                    leading=13,
                    spaceAfter=2,
                    spaceBefore=0,
                    alignment=TA_LEFT,
                    fontName='Helvetica',
                    leftIndent=0,
                    rightIndent=0,
                    firstLineIndent=0
                )
                
                # Parse and format lines
                lines = [l.strip() for l in resume_text.split('\n') if l.strip()]  # Remove empty lines
                prev_type = None
                formatted_lines = []
                header_processed = False
                
                for idx, line in enumerate(lines):
                    line_data = format_resume_line(line, prev_type, idx, header_processed)
                    formatted_lines.append(line_data)
                    if line_data['type'] != 'empty':
                        prev_type = line_data['type']
                        # Only mark header as processed after we've seen all header lines or a main section
                        if line_data['type'] == 'main_section':
                            header_processed = True
                        elif line_data['type'] == 'header_contact':
                            # Contact is usually the last header line
                            header_processed = True
                        elif idx >= 2 and line_data['type'] in ['header_name', 'header_title']:
                            # If we're past line 2 and still seeing header, mark as processed
                            header_processed = True
                
                for line_data in formatted_lines:
                    if line_data['type'] == 'empty':
                        elements.append(Spacer(1, 3))
                    elif line_data['type'] == 'header_name':
                        para = Paragraph(line_data['text'], header_name_style)
                        elements.append(para)
                    elif line_data['type'] == 'header_title':
                        para = Paragraph(line_data['text'], header_title_style)
                        elements.append(para)
                    elif line_data['type'] == 'header_contact':
                        # Parse contact line and create clickable hyperlinks for LinkedIn/GitHub
                        contact_text = line_data['text']
                        # Find LinkedIn and GitHub URLs
                        linkedin_match = re.search(r'(LinkedIn:\s*)(https?://)?(www\.)?(linkedin\.com/[^\s|,;]+)', contact_text, re.IGNORECASE)
                        github_match = re.search(r'(GitHub:\s*)(https?://)?(www\.)?(github\.com/[^\s|,;]+)', contact_text, re.IGNORECASE)
                        
                        # Build HTML with hyperlinks
                        contact_html = contact_text
                        if linkedin_match:
                            label = linkedin_match.group(1)
                            protocol = linkedin_match.group(2) or 'https://'
                            www = linkedin_match.group(3) or ''
                            path = linkedin_match.group(4)
                            url = protocol + www + path
                            contact_html = contact_html.replace(linkedin_match.group(0), 
                                f'{label}<link href="{url}" color="#FDC500">{url}</link>')
                        if github_match:
                            label = github_match.group(1)
                            protocol = github_match.group(2) or 'https://'
                            www = github_match.group(3) or ''
                            path = github_match.group(4)
                            url = protocol + www + path
                            contact_html = contact_html.replace(github_match.group(0),
                                f'{label}<link href="{url}" color="#FDC500">{url}</link>')
                        
                        # Create a table with black background for the contact info
                        # Calculate width: page width (8.5") - left margin (1") - right margin (1") = 6.5"
                        page_width = 8.5 * 72  # 8.5 inches in points
                        margins = 2 * 72  # 1 inch left + 1 inch right
                        table_width = page_width - margins
                        contact_para = Paragraph(contact_html, header_contact_style)
                        contact_table = Table([[contact_para]], colWidths=[table_width])
                        contact_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), '#000000'),  # Black background
                            ('TEXTCOLOR', (0, 0), (-1, -1), '#FFFFFF'),  # White text
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 0), (-1, -1), 11),
                            ('LEFTPADDING', (0, 0), (-1, -1), 12),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                            ('TOPPADDING', (0, 0), (-1, -1), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ]))
                        elements.append(contact_table)
                        elements.append(Spacer(1, 6))  # Add some space after
                    elif line_data['type'] == 'main_section':
                        para = Paragraph(line_data['text'], main_section_style)
                        elements.append(para)
                        elements.append(Spacer(1, 1))
                    elif line_data['type'] == 'category':
                        para = Paragraph(line_data['text'], category_style)
                        elements.append(para)
                    elif line_data['type'] == 'experience_entry':
                        para = Paragraph(line_data['text'], experience_entry_style)
                        elements.append(para)
                    elif line_data['type'] == 'project_entry':
                        para = Paragraph(line_data['text'], project_entry_style)
                        elements.append(para)
                    elif line_data['type'] == 'bullet':
                        para = Paragraph(f"• {line_data['text']}", bullet_style)
                        elements.append(para)
                    else:  # normal
                        para = Paragraph(line_data['text'], normal_style)
                        elements.append(para)
                
                # Build PDF
                doc.build(elements)
                buffer.seek(0)
                
                filename = data.get('filename', 'optimized_resume.pdf')
                if not filename.endswith('.pdf'):
                    filename = filename.rsplit('.', 1)[0] + '.pdf'
                
                response = Response(
                    buffer.getvalue(),
                    mimetype='application/pdf',
                    headers={
                        'Content-Disposition': f'attachment; filename={filename}'
                    }
                )
                return response
                
            except ImportError:
                return jsonify({'success': False, 'error': 'PDF generation requires reportlab. Install with: pip install reportlab'}), 500
                
        elif file_format == 'docx':
            # Generate DOCX
            try:
                from docx import Document
                from docx.shared import Pt, RGBColor, Inches
                from docx.enum.text import WD_ALIGN_PARAGRAPH
                
                doc = Document()
                
                # Set default font
                style = doc.styles['Normal']
                font = style.font
                font.name = 'Calibri'
                font.size = Pt(11)
                
                # Parse and format lines
                lines = [l.strip() for l in resume_text.split('\n') if l.strip()]  # Remove empty lines
                prev_type = None
                formatted_lines = []
                header_processed = False
                current_section = None  # Track current section (EXPERIENCE, PROJECTS, etc.)
                
                for idx, line in enumerate(lines):
                    line_data = format_resume_line(line, prev_type, idx, header_processed)
                    
                    # Track current section
                    if line_data['type'] == 'main_section':
                        current_section = line_data['text'].upper()
                    # If we're in PROJECTS section, detect project names
                    # Project names are typically:
                    # - Lines that come right after PROJECTS section header
                    # - OR lines with "|" separator (Project Name | Technologies | Date)
                    # - NOT lines ending with ":" (like "Technologies:", "Status:")
                    # - NOT bullet points
                    elif current_section == 'PROJECTS' and not line.startswith(('•', '-', '*', '·')):
                        # Check if it's not already classified as something else (like category, main_section, etc.)
                        if line_data['type'] in ['normal', 'experience_entry']:
                            # Project name detection:
                            # 1. Line with "|" separator (Project Name | Technologies | Date)
                            # 2. Line that comes right after PROJECTS section (first line after header)
                            # 3. Line that comes after bullet points (new project after previous project's bullets)
                            # 4. Line that doesn't end with ":" (not "Technologies:", "Status:", etc.)
                            # 5. Line that doesn't start with common metadata keywords
                            is_metadata = any(line.lower().startswith(keyword) for keyword in ['technologies:', 'status:', 'duration:', 'date:', 'tools:', 'stack:'])
                            # Check if it looks like a project name (not too long, doesn't have common words)
                            looks_like_project_name = (
                                not line.endswith(':') and 
                                not is_metadata and
                                len(line.split()) <= 5 and  # Project names are usually short
                                not any(word in line.lower() for word in ['developed', 'built', 'created', 'designed', 'implemented'])  # Not a description
                            )
                            if (('|' in line) or 
                                (prev_type == 'main_section' and looks_like_project_name) or
                                (prev_type == 'bullet' and looks_like_project_name) or  # New project after bullets
                                (prev_type == 'project_entry' and '|' in line)):
                                # Convert to project entry
                                line_data = {'type': 'project_entry', 'text': line}
                    
                    formatted_lines.append(line_data)
                    if line_data['type'] != 'empty':
                        prev_type = line_data['type']
                        # Only mark header as processed after we've seen all header lines or a main section
                        if line_data['type'] == 'main_section':
                            header_processed = True
                        elif line_data['type'] == 'header_contact':
                            # Contact is usually the last header line
                            header_processed = True
                        elif idx >= 2 and line_data['type'] in ['header_name', 'header_title']:
                            # If we're past line 2 and still seeing header, mark as processed
                            header_processed = True
                
                for line_data in formatted_lines:
                    if line_data['type'] == 'empty':
                        doc.add_paragraph()  # Empty paragraph
                    elif line_data['type'] == 'header_name':
                        para = doc.add_paragraph()
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(20)
                        para.paragraph_format.space_after = Pt(4)
                    elif line_data['type'] == 'header_title':
                        para = doc.add_paragraph()
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(15)
                        para.paragraph_format.space_after = Pt(6)
                    elif line_data['type'] == 'header_contact':
                        para = doc.add_paragraph()
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        # Set paragraph shading to black background
                        para.paragraph_format.shading.background_color.rgb = RGBColor(0, 0, 0)  # Black background
                        
                        # Parse contact line and create clickable hyperlinks for LinkedIn/GitHub
                        contact_text = line_data['text']
                        # Split by | to preserve structure
                        parts = contact_text.split('|')
                        for i, part in enumerate(parts):
                            part = part.strip()
                            if not part:
                                continue
                            
                            # Check for LinkedIn
                            linkedin_match = re.search(r'(LinkedIn:\s*)(https?://)?(www\.)?(linkedin\.com/[^\s|,;]+)', part, re.IGNORECASE)
                            if linkedin_match:
                                label = linkedin_match.group(1)
                                protocol = linkedin_match.group(2) or 'https://'
                                www = linkedin_match.group(3) or ''
                                path = linkedin_match.group(4)
                                url = protocol + www + path
                                # Add label
                                run = para.add_run(label)
                                run.font.size = Pt(11)
                                run.font.color.rgb = RGBColor(255, 255, 255)  # White text
                                # Add hyperlink using python-docx hyperlink method
                                from docx.oxml import parse_xml
                                from docx.oxml.ns import nsdecls, qn
                                # Create hyperlink element
                                hyperlink = parse_xml(
                                    f'<w:hyperlink r:id="rId1" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                                    f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
                                )
                                hyperlink_run = hyperlink.add_r()
                                hyperlink_run.text = url
                                hyperlink_run.rPr = parse_xml(
                                    f'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                                    f'<w:color w:val="FDC500"/><w:u w:val="single"/></w:rPr>'
                                )
                                para._element.append(hyperlink)
                            # Check for GitHub
                            elif re.search(r'(GitHub:\s*)(https?://)?(www\.)?(github\.com/[^\s|,;]+)', part, re.IGNORECASE):
                                github_match = re.search(r'(GitHub:\s*)(https?://)?(www\.)?(github\.com/[^\s|,;]+)', part, re.IGNORECASE)
                                label = github_match.group(1)
                                protocol = github_match.group(2) or 'https://'
                                www = github_match.group(3) or ''
                                path = github_match.group(4)
                                url = protocol + www + path
                                # Add label
                                run = para.add_run(label)
                                run.font.size = Pt(11)
                                run.font.color.rgb = RGBColor(255, 255, 255)  # White text
                                # Add hyperlink
                                hyperlink = parse_xml(
                                    f'<w:hyperlink r:id="rId2" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                                    f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
                                )
                                hyperlink_run = hyperlink.add_r()
                                hyperlink_run.text = url
                                hyperlink_run.rPr = parse_xml(
                                    f'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                                    f'<w:color w:val="FDC500"/><w:u w:val="single"/></w:rPr>'
                                )
                                para._element.append(hyperlink)
                            else:
                                # Regular text
                                run = para.add_run(part)
                                run.font.size = Pt(11)
                                run.font.color.rgb = RGBColor(255, 255, 255)  # White text
                            
                            # Add separator if not last part
                            if i < len(parts) - 1:
                                run = para.add_run(' | ')
                                run.font.size = Pt(11)
                                run.font.color.rgb = RGBColor(255, 255, 255)  # White text
                        
                        para.paragraph_format.space_after = Pt(14)
                        para.paragraph_format.space_before = Pt(0)
                        # Add padding by adjusting left/right indents
                        para.paragraph_format.left_indent = Pt(12)
                        para.paragraph_format.right_indent = Pt(12)
                    elif line_data['type'] == 'main_section':
                        para = doc.add_paragraph()
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(13)
                        run.font.color.rgb = RGBColor(0, 0, 0)  # Black color instead of maroon
                        para.paragraph_format.space_before = Pt(10)
                        para.paragraph_format.space_after = Pt(4)
                    elif line_data['type'] == 'category':
                        para = doc.add_paragraph()
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(0, 0, 0)  # Black
                        para.paragraph_format.space_before = Pt(3)
                        para.paragraph_format.space_after = Pt(1)
                    elif line_data['type'] == 'experience_entry':
                        para = doc.add_paragraph()
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(0, 0, 0)  # Black
                        para.paragraph_format.space_before = Pt(3)
                        para.paragraph_format.space_after = Pt(1)
                    elif line_data['type'] == 'project_entry':
                        para = doc.add_paragraph()
                        run = para.add_run(line_data['text'])
                        run.bold = True
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(0, 0, 0)  # Black color instead of maroon
                        para.paragraph_format.space_before = Pt(3)
                        para.paragraph_format.space_after = Pt(1)
                    elif line_data['type'] == 'bullet':
                        para = doc.add_paragraph()
                        run = para.add_run('• ' + line_data['text'])
                        run.font.size = Pt(10)
                        para.paragraph_format.left_indent = Pt(0)
                        para.paragraph_format.space_after = Pt(1)
                    else:  # normal
                        para = doc.add_paragraph()
                        run = para.add_run(line_data['text'])
                        run.font.size = Pt(10)
                        para.paragraph_format.space_after = Pt(1)
                
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                
                filename = data.get('filename', 'optimized_resume.docx')
                if not filename.endswith('.docx'):
                    filename = filename.rsplit('.', 1)[0] + '.docx'
                
                response = Response(
                    buffer.getvalue(),
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    headers={
                        'Content-Disposition': f'attachment; filename={filename}'
                    }
                )
                return response
                
            except ImportError:
                return jsonify({'success': False, 'error': 'DOCX generation requires python-docx. Install with: pip install python-docx'}), 500
                
        else:
            # Default to TXT
            filename = data.get('filename', 'optimized_resume.txt')
            if not filename.endswith('.txt'):
                filename = filename.rsplit('.', 1)[0] + '.txt'
            
            response = Response(
                resume_text,
                mimetype='text/plain',
                headers={
                    'Content-Disposition': f'attachment; filename={filename}'
                }
            )
            return response
        
    except Exception as e:
        # Log error but don't expose internal details
        import logging
        logging.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing the resume. Please try again.'
        }), 500


if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5000, max_port=5100):
        """Find a free port."""
        for port in range(start_port, max_port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No free port found")
    
    port = find_free_port()
    
    print(f"\n{'='*60}")
    print(f"🚀 Resume Analyzer Web App")
    print(f"{'='*60}")
    print(f"📱 Open in browser: http://localhost:{port}")
    print(f"{'='*60}")
    
    # Check Groq connection status
    if groq_optimizer.is_available():
        print(f"\n✅ Groq API Connected - Using real AI analysis!")
    else:
        print(f"\n⚠️  Using dummy data (no Groq API key)")
        print(f"   To enable Groq AI:")
        print(f"   1. Get API key: https://console.groq.com/")
        print(f"   2. Install: pip install groq")
        print(f"   3. Set: export GROQ_API_KEY=your_key_here")
        print(f"   4. Or create .env file with: GROQ_API_KEY=your_key_here\n")
    
    # Production vs Development mode
    is_production = os.getenv('FLASK_ENV') == 'production' or os.getenv('ENVIRONMENT') == 'production'
    debug_mode = not is_production
    
    if is_production:
        print("\n🚀 Running in PRODUCTION mode")
        print("   - Debug mode: DISABLED")
        print("   - Rate limiting: ENABLED" if RATE_LIMITING_ENABLED else "   - Rate limiting: DISABLED")
        print("   - File size limit: 10MB")
        print("   - Input validation: ENABLED\n")
    else:
        print("\n🔧 Running in DEVELOPMENT mode")
        print("   - Debug mode: ENABLED")
        print("   - Rate limiting: ENABLED" if RATE_LIMITING_ENABLED else "   - Rate limiting: DISABLED\n")
    
    app.run(host='127.0.0.1', port=port, debug=debug_mode, use_reloader=False)

