"""
Resume Analyzer & Optimizer API
Analyzes resume against job description and provides content-based suggestions.
Only shows optimization option if match score < 70%.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.groq_optimizer import GroqResumeOptimizer

app = Flask(__name__)
CORS(app)

# Initialize optimizer
groq_optimizer = GroqResumeOptimizer()


def analyze_resume_match(resume_text, job_description):
    """
    Analyze resume against job description using Groq API.
    Returns match score and content-based suggestions.
    """
    if not groq_optimizer.is_available():
        # Use dummy data for testing
        return get_dummy_analysis(resume_text, job_description)
    
    try:
        prompt = f"""Analyze this resume against the job description and provide:
1. A match score (0-100%) - be strict and accurate
2. Specific content changes needed (not just keywords, but actual content improvements)
3. Areas where the resume is strong
4. Areas where the resume needs improvement

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide your analysis in this exact format:

MATCH_SCORE: [number between 0-100]
STRENGTHS:
- [strength 1]
- [strength 2]
- ...

IMPROVEMENTS_NEEDED:
- [specific content change 1 - be detailed about what needs to change]
- [specific content change 2 - be detailed about what needs to change]
- ...

CONTENT_SUGGESTIONS:
For each improvement, provide specific content suggestions:
1. [Section/Area]: [What to change] - [Why] - [How to improve it with actual content example]
2. [Section/Area]: [What to change] - [Why] - [How to improve it with actual content example]
...

Be specific about CONTENT changes, not just keywords. Focus on:
- Experience descriptions that better match the job
- Skills that should be emphasized or added
- Achievements that should be highlighted
- Sections that need restructuring
- Missing relevant experience or projects
"""

        response = groq_optimizer.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert resume analyst. Analyze resumes against job descriptions 
                    and provide specific, actionable content improvement suggestions. Focus on meaningful 
                    content changes, not keyword stuffing. Be accurate and strict with match scores."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent scoring
            max_tokens=3000
        )
        
        analysis_text = response.choices[0].message.content
        
        # Parse the response
        return parse_analysis(analysis_text, resume_text, job_description)
        
    except Exception as e:
        return {"error": f"Error analyzing resume: {str(e)}"}


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
    
    # Extract match score
    if "MATCH_SCORE:" in analysis_text:
        try:
            score_line = analysis_text.split("MATCH_SCORE:")[1].split("\n")[0].strip()
            # Extract number from the line
            score = float(''.join(filter(str.isdigit, score_line.split()[0])))
            result["match_score"] = min(100, max(0, score))
        except:
            pass
    
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
        result["strengths"] = strengths[:10]  # Limit to 10
    
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
        result["improvements_needed"] = improvements[:10]  # Limit to 10
    
    # Extract content suggestions
    if "CONTENT_SUGGESTIONS:" in analysis_text:
        suggestions_section = analysis_text.split("CONTENT_SUGGESTIONS:")[1]
        
        # Parse numbered suggestions
        suggestions = []
        for line in suggestions_section.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                # Remove numbering/bullets
                clean_line = line.lstrip("0123456789.-) ").strip()
                if clean_line and len(clean_line) > 20:  # Only substantial suggestions
                    suggestions.append(clean_line)
        
        result["content_suggestions"] = suggestions[:15]  # Limit to 15
    
    # Determine if optimization should be shown
    result["show_optimization"] = result["match_score"] < 70
    
    return result


def get_dummy_analysis(resume_text, job_description):
    """
    Generate dummy analysis for testing when Groq API is not available.
    """
    # Simple keyword matching to calculate a dummy score
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Extract common tech keywords
    tech_keywords = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
                     'java', 'c#', '.net', 'angular', 'vue', 'typescript', 'mongodb',
                     'postgresql', 'kubernetes', 'git', 'agile', 'scrum']
    
    resume_keywords = [kw for kw in tech_keywords if kw in resume_lower]
    job_keywords = [kw for kw in tech_keywords if kw in job_lower]
    
    # Calculate match score (simple algorithm)
    if job_keywords:
        matched = len(set(resume_keywords) & set(job_keywords))
        match_score = min(100, int((matched / len(job_keywords)) * 100))
        # Boost score if there are many matches
        if matched >= len(job_keywords) * 0.7:
            match_score = min(100, match_score + 10)
    else:
        match_score = 65  # Default score
    
    # Adjust score based on experience mentions
    if 'senior' in job_lower and 'senior' not in resume_lower:
        match_score = max(0, match_score - 15)
    if 'junior' in job_lower and 'senior' in resume_lower:
        match_score = min(100, match_score + 10)
    
    # Ensure score is reasonable (not 0 unless really bad match)
    if match_score == 0 and len(resume_keywords) > 0:
        match_score = 30  # Minimum score if there's some overlap
    
    # Generate dummy suggestions based on score
    if match_score < 70:
        suggestions = [
            f"Experience Section: Add more details about your {job_keywords[0] if job_keywords else 'relevant'} projects - Explain the impact and results - Example: 'Developed {job_keywords[0] if job_keywords else 'web'} application that improved efficiency by 30%'",
            "Skills Section: Emphasize your most relevant technical skills - Move the most relevant skills to the top of your skills list",
            "Summary Section: Tailor your professional summary to highlight experience most relevant to this role",
            "Achievements: Add quantifiable achievements that demonstrate your impact in similar roles"
        ]
        
        improvements = [
            f"Missing or insufficient experience with {job_keywords[0] if job_keywords else 'key technologies'} mentioned in job description",
            "Need to highlight relevant projects and achievements more prominently",
            "Professional summary could better align with job requirements"
        ]
        
        strengths = [
            "Good technical foundation in relevant areas",
            "Relevant work experience",
            "Strong educational background"
        ]
    else:
        suggestions = [
            "Your resume is well-matched! Consider minor tweaks to emphasize your strongest relevant experiences."
        ]
        improvements = []
        strengths = [
            "Strong alignment with job requirements",
            "Relevant technical skills",
            "Good experience match"
        ]
    
    return {
        "match_score": match_score,
        "strengths": strengths,
        "improvements_needed": improvements,
        "content_suggestions": suggestions,
        "show_optimization": match_score < 70,
        "raw_analysis": f"Dummy analysis - Match Score: {match_score}%"
    }


def create_optimized_resume(resume_text, job_description, suggestions):
    """
    Create optimized resume based on suggestions.
    """
    if not groq_optimizer.is_available():
        # Use dummy optimized resume for testing
        return get_dummy_optimized_resume(resume_text, job_description, suggestions)
    
    try:
        prompt = f"""Based on the analysis and suggestions, create an optimized version of this resume.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SUGGESTIONS TO IMPLEMENT:
{chr(10).join(suggestions[:10])}

Create a complete, optimized resume that:
1. Implements the content suggestions naturally
2. Maintains all truthful information
3. Improves content (not just adds keywords)
4. Better matches the job requirements
5. Is ATS-friendly
6. Uses action verbs and quantifiable achievements

Provide the complete optimized resume text."""

        response = groq_optimizer.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert resume writer. Create optimized resumes that implement 
                    content improvements naturally. Focus on meaningful changes, not keyword stuffing. 
                    Always maintain truthfulness."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        optimized_resume = response.choices[0].message.content
        
        # Clean up the response
        if "OPTIMIZED RESUME:" in optimized_resume:
            optimized_resume = optimized_resume.split("OPTIMIZED RESUME:")[-1].strip()
        elif "RESUME:" in optimized_resume:
            optimized_resume = optimized_resume.split("RESUME:")[-1].strip()
        
        return {
            "optimized_resume": optimized_resume,
            "original_resume": resume_text
        }
        
    except Exception as e:
        return {"error": f"Error creating optimized resume: {str(e)}"}


def get_dummy_optimized_resume(resume_text, job_description, suggestions):
    """
    Generate dummy optimized resume for testing when Groq API is not available.
    """
    # Simple optimization: add a note at the top
    optimized = f"""[OPTIMIZED VERSION - Based on suggestions]

{resume_text}

---
OPTIMIZATION NOTES:
- Enhanced experience descriptions with quantifiable achievements
- Reordered content to highlight most relevant experience first
- Added relevant keywords naturally throughout the resume
- Improved action verbs and impact statements
- Tailored summary to better match job requirements

This is a dummy optimized version. For real optimization, set GROQ_API_KEY environment variable.
"""
    
    return {
        "optimized_resume": optimized,
        "original_resume": resume_text
    }


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze resume against job description.
    
    Expected JSON:
    {
        "resume_text": "resume content...",
        "job_description": "job description..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description are required'
            }), 400
        
        # Analyze resume
        analysis = analyze_resume_match(resume_text, job_description)
        
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize', methods=['POST'])
def optimize():
    """
    Optimize resume based on analysis.
    
    Expected JSON:
    {
        "resume_text": "resume content...",
        "job_description": "job description...",
        "suggestions": ["suggestion 1", "suggestion 2", ...]  # Optional
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        suggestions = data.get('suggestions', [])
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description are required'
            }), 400
        
        # If no suggestions provided, analyze first
        if not suggestions:
            analysis = analyze_resume_match(resume_text, job_description)
            if 'error' in analysis:
                return jsonify({
                    'success': False,
                    'error': analysis['error']
                }), 500
            suggestions = analysis.get('content_suggestions', [])
        
        # Create optimized resume
        result = create_optimized_resume(resume_text, job_description, suggestions)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        return jsonify({
            'success': True,
            'optimized_resume': result['optimized_resume'],
            'original_resume': result['original_resume']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/')
def index():
    """API information page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Analyzer API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #28a745; font-weight: bold; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
            .test-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .test-btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>🚀 Resume Analyzer & Optimizer API</h1>
        <p>API is running! Use the endpoints below to analyze and optimize resumes.</p>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <code>/api/health</code></h3>
            <p>Health check endpoint</p>
            <button class="test-btn" onclick="testHealth()">Test Health</button>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <code>/api/analyze</code></h3>
            <p>Analyze resume against job description</p>
            <p><strong>Body:</strong> <code>{"resume_text": "...", "job_description": "..."}</code></p>
            <button class="test-btn" onclick="testAnalyze()">Test Analyze</button>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <code>/api/optimize</code></h3>
            <p>Optimize resume based on analysis</p>
            <p><strong>Body:</strong> <code>{"resume_text": "...", "job_description": "..."}</code></p>
            <button class="test-btn" onclick="testOptimize()">Test Optimize</button>
        </div>
        
        <div id="result" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; display: none;">
            <h3>Result:</h3>
            <pre id="result-content"></pre>
        </div>
        
        <script>
            function showResult(data) {
                document.getElementById('result').style.display = 'block';
                document.getElementById('result-content').textContent = JSON.stringify(data, null, 2);
            }
            
            async function testHealth() {
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    showResult(data);
                } catch (error) {
                    showResult({error: error.message});
                }
            }
            
            async function testAnalyze() {
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            resume_text: 'John Doe\\nSoftware Engineer\\n5 years Python and JavaScript',
                            job_description: 'Senior Software Engineer with React, Node.js, AWS'
                        })
                    });
                    const data = await response.json();
                    showResult(data);
                } catch (error) {
                    showResult({error: error.message});
                }
            }
            
            async function testOptimize() {
                try {
                    const response = await fetch('/api/optimize', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            resume_text: 'John Doe\\nSoftware Engineer\\nPython, JavaScript',
                            job_description: 'Senior Software Engineer with React, Node.js'
                        })
                    });
                    const data = await response.json();
                    showResult(data);
                } catch (error) {
                    showResult({error: error.message});
                }
            }
        </script>
    </body>
    </html>
    """


@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        'status': 'healthy',
        'service': 'Resume Analyzer & Optimizer API',
        'groq_available': groq_optimizer.is_available()
    })


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
    
    print(f"\n🚀 Resume Analyzer API running on http://localhost:{port}")
    print(f"📊 POST /api/analyze - Analyze resume match score")
    print(f"✨ POST /api/optimize - Optimize resume")
    print(f"❤️  GET  /api/health - Health check")
    print(f"\n✅ Using dummy data (no Groq API key needed for testing)\n")
    app.run(host='127.0.0.1', port=port, debug=True, use_reloader=False)

