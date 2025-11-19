"""
Demo Version - No Database Required!
Shows the UI with dummy data so you can see how it looks.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Dummy data - no database needed!
DUMMY_RESUMES = [
    {
        'id': 1,
        'name': 'My Software Engineer Resume',
        'filename': 'resume_software_engineer.pdf',
        'file_type': 'pdf',
        'word_count': 450,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=2)).isoformat(),
        'content': '''John Doe
Software Engineer
Email: john.doe@email.com | Phone: (555) 123-4567

SUMMARY
Experienced software engineer with 5 years of experience in Python, JavaScript, 
and cloud technologies. Strong background in full-stack development and machine learning.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020 - Present
- Developed scalable web applications using Python and React
- Led team of 5 developers on multiple projects
- Implemented CI/CD pipelines using Docker and Kubernetes
- Reduced deployment time by 40%

Software Engineer | Startup Inc | 2018 - 2020
- Built RESTful APIs using Flask and Django
- Worked with PostgreSQL and MongoDB databases
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014 - 2018

SKILLS
Programming Languages: Python, JavaScript, Java, SQL
Frameworks: React, Django, Flask, Node.js
Tools: Git, Docker, Kubernetes, AWS, Jenkins'''
    },
    {
        'id': 2,
        'name': 'Data Scientist Resume',
        'filename': 'resume_data_scientist.pdf',
        'file_type': 'pdf',
        'word_count': 520,
        'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
        'updated_at': (datetime.now() - timedelta(days=1)).isoformat(),
        'content': '''Jane Smith
Data Scientist
Email: jane.smith@email.com | Phone: (555) 987-6543

SUMMARY
Data scientist with expertise in machine learning, statistical analysis, and 
big data technologies. Passionate about turning data into actionable insights.

EXPERIENCE
Senior Data Scientist | DataCorp | 2019 - Present
- Built predictive models using Python and TensorFlow
- Analyzed large datasets using Spark and Hadoop
- Improved model accuracy by 25%

Data Analyst | Analytics Inc | 2017 - 2019
- Created dashboards using Tableau and Power BI
- Performed statistical analysis using R and Python

EDUCATION
Master of Science in Data Science
Tech University | 2015 - 2017

SKILLS
Languages: Python, R, SQL
ML/AI: TensorFlow, PyTorch, Scikit-learn
Tools: Spark, Hadoop, Tableau, Jupyter'''
    }
]

DUMMY_JOBS = [
    {
        'id': 1,
        'title': 'Senior Software Engineer',
        'company': 'Tech Corp',
        'content': '''We are looking for a Senior Software Engineer to join our dynamic team.

Requirements:
- 5+ years of experience in software development
- Proficiency in Python and JavaScript
- Experience with React framework
- Strong knowledge of RESTful API development
- Experience with cloud platforms (AWS, Azure, or GCP)
- Familiarity with Docker and Kubernetes
- Knowledge of SQL and NoSQL databases
- Experience with CI/CD pipelines

Responsibilities:
- Develop and maintain scalable web applications
- Design and implement RESTful APIs
- Work with cross-functional teams
- Participate in code reviews
- Deploy applications to cloud infrastructure''',
        'source_url': 'https://techcorp.com/careers',
        'created_at': (datetime.now() - timedelta(days=3)).isoformat()
    },
    {
        'id': 2,
        'title': 'Full Stack Developer',
        'company': 'StartupXYZ',
        'content': '''Join our fast-growing startup as a Full Stack Developer!

Requirements:
- 3+ years of full-stack development experience
- Strong skills in Python, JavaScript, and React
- Experience with Django or Flask
- Knowledge of PostgreSQL
- Understanding of microservices architecture
- Agile/Scrum experience

What we offer:
- Competitive salary
- Equity options
- Remote work flexibility
- Great team culture''',
        'source_url': 'https://startupxyz.com/jobs',
        'created_at': (datetime.now() - timedelta(days=7)).isoformat()
    },
    {
        'id': 3,
        'title': 'Machine Learning Engineer',
        'company': 'AI Innovations',
        'content': '''Machine Learning Engineer position at cutting-edge AI company.

Requirements:
- Master's degree in Computer Science or related field
- Experience with TensorFlow or PyTorch
- Strong Python programming skills
- Knowledge of deep learning architectures
- Experience with cloud ML platforms
- Published research papers (preferred)

Responsibilities:
- Develop and deploy ML models
- Optimize model performance
- Collaborate with data scientists
- Productionize ML pipelines''',
        'source_url': 'https://aiinnovations.com/careers',
        'created_at': (datetime.now() - timedelta(days=1)).isoformat()
    }
]

DUMMY_OPTIMIZATIONS = [
    {
        'id': 1,
        'resume_id': 1,
        'job_description_id': 1,
        'quality_score': 85.0,
        'match_score': 78.5,
        'optimization_type': 'complete',
        'model_used': 'llama-3.1-70b-versatile',
        'api_provider': 'groq',
        'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
        'has_optimized_resume': True,
        'suggestions_count': 5,
        'optimized_resume': '''John Doe
Senior Software Engineer
Email: john.doe@email.com | Phone: (555) 123-4567

SUMMARY
Senior Software Engineer with 5+ years of experience in Python, JavaScript, 
React, and cloud technologies. Proven track record in full-stack development, 
CI/CD implementation, and team leadership. Expert in building scalable web 
applications and deploying to AWS using Docker and Kubernetes.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020 - Present
- Developed and maintained scalable web applications using Python and React
- Led cross-functional team of 5 developers on multiple projects
- Implemented and optimized CI/CD pipelines using Docker and Kubernetes
- Reduced deployment time by 40% through automation
- Designed and developed RESTful APIs serving 1M+ requests daily

Software Engineer | Startup Inc | 2018 - 2020
- Built robust RESTful APIs using Flask and Django frameworks
- Worked extensively with PostgreSQL and MongoDB databases
- Collaborated with cross-functional teams in Agile environment

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014 - 2018

SKILLS
Programming Languages: Python, JavaScript, Java, SQL
Frameworks: React, Django, Flask, Node.js
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git
Databases: PostgreSQL, MongoDB, MySQL''',
        'suggestions': [
            'Added more specific metrics (1M+ requests, 40% reduction)',
            'Emphasized cloud technologies (AWS) more prominently',
            'Added "Agile" keyword to match job requirements',
            'Enhanced summary with more relevant keywords',
            'Reordered skills to highlight cloud and DevOps experience'
        ],
        'matching_keywords': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes', 'RESTful API', 'PostgreSQL'],
        'missing_keywords': ['Microservices', 'GraphQL', 'TypeScript']
    },
    {
        'id': 2,
        'resume_id': 1,
        'job_description_id': 2,
        'quality_score': 82.0,
        'match_score': 72.0,
        'optimization_type': 'complete',
        'model_used': 'llama-3.1-70b-versatile',
        'api_provider': 'groq',
        'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
        'has_optimized_resume': True,
        'suggestions_count': 4,
        'suggestions': [
            'Emphasized startup experience',
            'Added microservices architecture mention',
            'Highlighted Agile/Scrum experience',
            'Reordered content to match job priorities'
        ],
        'matching_keywords': ['Python', 'JavaScript', 'React', 'Django', 'Flask', 'PostgreSQL'],
        'missing_keywords': ['Microservices', 'Agile', 'Scrum']
    }
]

@app.route('/')
def index():
    """Render main page."""
    return render_template('app_db.html')

# ==================== Resume Management ====================

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """Get all resumes (dummy data)."""
    return jsonify({
        'success': True,
        'resumes': [
            {
                'id': r['id'],
                'name': r['name'],
                'filename': r['filename'],
                'file_type': r['file_type'],
                'word_count': r['word_count'],
                'created_at': r['created_at'],
                'updated_at': r['updated_at']
            }
            for r in DUMMY_RESUMES
        ]
    })

@app.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume by ID (dummy data)."""
    resume = next((r for r in DUMMY_RESUMES if r['id'] == resume_id), None)
    if not resume:
        return jsonify({'success': False, 'error': 'Resume not found'}), 404
    
    return jsonify({
        'success': True,
        'resume': resume
    })

@app.route('/api/resumes', methods=['POST'])
def create_resume():
    """Create resume (demo - returns success but doesn't save)."""
    return jsonify({
        'success': True,
        'message': 'Demo mode: Resume would be saved in real mode',
        'resume': {
            'id': len(DUMMY_RESUMES) + 1,
            'name': 'New Resume',
            'filename': 'new_resume.pdf'
        }
    })

@app.route('/api/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete resume (demo - returns success but doesn't delete)."""
    return jsonify({
        'success': True,
        'message': 'Demo mode: Resume would be deleted in real mode'
    })

# ==================== Job Description Management ====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all job descriptions (dummy data)."""
    return jsonify({
        'success': True,
        'jobs': [
            {
                'id': j['id'],
                'title': j['title'],
                'company': j['company'],
                'content': j['content'][:500] + '...' if len(j['content']) > 500 else j['content'],
                'source_url': j['source_url'],
                'created_at': j['created_at']
            }
            for j in DUMMY_JOBS
        ]
    })

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job description by ID (dummy data)."""
    job = next((j for j in DUMMY_JOBS if j['id'] == job_id), None)
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job': job
    })

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create job (demo - returns success but doesn't save)."""
    return jsonify({
        'success': True,
        'message': 'Demo mode: Job would be saved in real mode',
        'job': {
            'id': len(DUMMY_JOBS) + 1,
            'title': 'New Job',
            'company': 'New Company'
        }
    })

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete job (demo - returns success but doesn't delete)."""
    return jsonify({
        'success': True,
        'message': 'Demo mode: Job would be deleted in real mode'
    })

# ==================== Optimization ====================

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Optimize resume (dummy data)."""
    import json
    data = json.loads(request.data) if request.data else {}
    resume_id = data.get('resume_id', 1)
    job_id = data.get('job_id', 1)
    
    # Find matching optimization or create new one
    optimization = next(
        (opt for opt in DUMMY_OPTIMIZATIONS 
         if opt['resume_id'] == resume_id and opt['job_description_id'] == job_id),
        None
    )
    
    if not optimization:
        # Create a new dummy optimization
        resume = next((r for r in DUMMY_RESUMES if r['id'] == resume_id), DUMMY_RESUMES[0])
        job = next((j for j in DUMMY_JOBS if j['id'] == job_id), DUMMY_JOBS[0])
        
        optimization = {
            'id': len(DUMMY_OPTIMIZATIONS) + 1,
            'resume_id': resume_id,
            'job_description_id': job_id,
            'quality_score': round(random.uniform(75, 95), 1),
            'match_score': round(random.uniform(65, 90), 1),
            'optimization_type': data.get('optimization_type', 'complete'),
            'model_used': 'llama-3.1-70b-versatile',
            'api_provider': 'groq',
            'created_at': datetime.now().isoformat(),
            'has_optimized_resume': True,
            'suggestions_count': random.randint(3, 7),
            'optimized_resume': resume['content'] + '\n\n[OPTIMIZED VERSION - This is demo data]',
            'suggestions': [
                'Added relevant keywords from job description',
                'Improved action verbs and quantifiable achievements',
                'Reordered sections to match job priorities',
                'Enhanced technical skills section',
                'Optimized summary for ATS systems'
            ],
            'matching_keywords': ['Python', 'JavaScript', 'React', 'AWS'],
            'missing_keywords': ['TypeScript', 'GraphQL']
        }
    
    # Get basic analysis
    analysis = {
        'resume_quality': {
            'quality_score': optimization['quality_score'],
            'word_count': 450,
            'section_count': 4,
            'technical_skills_count': 12,
            'issues': []
        },
        'job_match': {
            'score': optimization['match_score'],
            'matching_keywords': optimization.get('matching_keywords', []),
            'missing_keywords': optimization.get('missing_keywords', []),
            'match_count': len(optimization.get('matching_keywords', [])),
            'total_job_keywords': 20
        },
        'suggestions': optimization.get('suggestions', []),
        'top_keywords': [
            ('python', 15), ('javascript', 12), ('react', 10),
            ('aws', 8), ('docker', 7), ('kubernetes', 6)
        ],
        'technical_skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes']
    }
    
    return jsonify({
        'success': True,
        'optimization': {
            'id': optimization['id'],
            'resume_id': optimization['resume_id'],
            'job_description_id': optimization['job_description_id'],
            'quality_score': optimization['quality_score'],
            'match_score': optimization['match_score'],
            'optimization_type': optimization['optimization_type'],
            'model_used': optimization['model_used'],
            'api_provider': optimization['api_provider'],
            'created_at': optimization['created_at'],
            'has_optimized_resume': optimization['has_optimized_resume'],
            'suggestions_count': optimization['suggestions_count']
        },
        'analysis': analysis,
        'optimized_resume': optimization.get('optimized_resume', '')
    })

@app.route('/api/optimizations', methods=['GET'])
def get_optimizations():
    """Get all optimizations (dummy data)."""
    resume_id = request.args.get('resume_id', type=int)
    job_id = request.args.get('job_id', type=int)
    
    optimizations = DUMMY_OPTIMIZATIONS
    if resume_id:
        optimizations = [opt for opt in optimizations if opt['resume_id'] == resume_id]
    
    return jsonify({
        'success': True,
        'optimizations': [
            {
                'id': opt['id'],
                'resume_id': opt['resume_id'],
                'job_description_id': opt['job_description_id'],
                'quality_score': opt['quality_score'],
                'match_score': opt['match_score'],
                'optimization_type': opt['optimization_type'],
                'model_used': opt['model_used'],
                'api_provider': opt['api_provider'],
                'created_at': opt['created_at'],
                'has_optimized_resume': opt['has_optimized_resume'],
                'suggestions_count': opt['suggestions_count']
            }
            for opt in optimizations
        ]
    })

@app.route('/api/optimizations/<int:opt_id>', methods=['GET'])
def get_optimization(opt_id):
    """Get optimization by ID (dummy data)."""
    optimization = next((opt for opt in DUMMY_OPTIMIZATIONS if opt['id'] == opt_id), None)
    if not optimization:
        return jsonify({'success': False, 'error': 'Optimization not found'}), 404
    
    return jsonify({
        'success': True,
        'optimization': optimization
    })

@app.route('/api/optimizations/<int:opt_id>', methods=['DELETE'])
def delete_optimization(opt_id):
    """Delete optimization (demo - returns success but doesn't delete)."""
    return jsonify({
        'success': True,
        'message': 'Demo mode: Optimization would be deleted in real mode'
    })

# ==================== Analytics ====================

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data (dummy data)."""
    return jsonify({
        'success': True,
        'analytics': {
            'total_resumes': len(DUMMY_RESUMES),
            'total_jobs': len(DUMMY_JOBS),
            'total_optimizations': len(DUMMY_OPTIMIZATIONS),
            'avg_match_score': round(sum(opt['match_score'] for opt in DUMMY_OPTIMIZATIONS) / len(DUMMY_OPTIMIZATIONS), 2),
            'avg_quality_score': round(sum(opt['quality_score'] for opt in DUMMY_OPTIMIZATIONS) / len(DUMMY_OPTIMIZATIONS), 2)
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': 'demo_mode',
        'groq_configured': False,
        'app_ready': True,
        'mode': 'DEMO - Using dummy data, no database required!'
    })

if __name__ == '__main__':
    import socket
    import sys
    
    # Function to find available port
    def find_free_port(start_port=5000, max_attempts=10):
        """Find an available port starting from start_port."""
        for port in range(start_port, start_port + max_attempts):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        return None
    
    # Find available port
    port = find_free_port(5000)
    
    if port is None:
        print("❌ Could not find an available port!")
        print("   Please close other applications using ports 5000-5010")
        sys.exit(1)
    
    if port != 5000:
        print(f"⚠️  Port 5000 is in use, using port {port} instead")
        print(f"   (This is common on macOS due to AirPlay Receiver)")
    
    print("\n" + "="*70)
    print("🎨 Starting Resume Optimizer - DEMO MODE")
    print("="*70)
    print("💡 This is a demo with dummy data - no database needed!")
    print("\n" + "="*70)
    print("✅ SERVER STARTING...")
    print("="*70)
    print(f"\n🌐 OPEN THIS URL IN YOUR BROWSER:")
    print(f"   👉 http://localhost:{port} 👈")
    print(f"\n   Or try: http://127.0.0.1:{port}")
    print("\n" + "="*70)
    print("📝 IMPORTANT:")
    print("   - Keep this terminal window open while using the app")
    print("   - Press Ctrl+C to stop the server when done")
    print("="*70 + "\n")
    
    try:
        print("🚀 Server is running! Waiting for requests...\n")
        app.run(debug=True, host='0.0.0.0', port=port, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Port {port} might be in use - try closing other apps")
        print(f"   2. On macOS, disable AirPlay Receiver:")
        print(f"      System Preferences → General → AirDrop & Handoff")
        print(f"      Turn off 'AirPlay Receiver'")
        print(f"   3. Try a different port manually")
        sys.exit(1)

