"""
Internal Recruiter Tool - Demo Version with Dummy Data
For recruiters to bulk optimize candidates from database (simulated with dummy data).
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
from services.bulk_optimizer import BulkOptimizer
from services.cache_manager import optimization_cache
from services.optimization_queue import optimization_queue
import os

app = Flask(__name__)
CORS(app)

# Dummy candidate data - simulating your database
DUMMY_CANDIDATES = [
    {
        'id': 1,
        'name': 'John Smith',
        'email': 'john.smith@email.com',
        'phone': '(555) 123-4567',
        'experience': [
            {'title': 'Senior Software Engineer', 'company': 'Tech Corp', 'years': 5, 'description': 'Developed web applications using Python and React'},
            {'title': 'Software Engineer', 'company': 'Startup Inc', 'years': 3, 'description': 'Built RESTful APIs and worked with databases'}
        ],
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'education': {'degree': 'BS Computer Science', 'university': 'MIT', 'year': 2016},
        'resume_text': 'Experienced software engineer with 8 years in full-stack development.'
    },
    {
        'id': 2,
        'name': 'Sarah Johnson',
        'email': 'sarah.j@email.com',
        'phone': '(555) 234-5678',
        'experience': [
            {'title': 'Data Scientist', 'company': 'DataCorp', 'years': 4, 'description': 'Built ML models using Python and TensorFlow'},
            {'title': 'Data Analyst', 'company': 'Analytics Inc', 'years': 2, 'description': 'Created dashboards and performed statistical analysis'}
        ],
        'skills': ['Python', 'R', 'TensorFlow', 'SQL', 'Tableau'],
        'education': {'degree': 'MS Data Science', 'university': 'Stanford', 'year': 2018},
        'resume_text': 'Data scientist with expertise in machine learning and statistical analysis.'
    },
    {
        'id': 3,
        'name': 'Mike Chen',
        'email': 'mike.chen@email.com',
        'phone': '(555) 345-6789',
        'experience': [
            {'title': 'Full Stack Developer', 'company': 'WebSolutions', 'years': 6, 'description': 'Developed scalable web applications'},
            {'title': 'Frontend Developer', 'company': 'Design Studio', 'years': 2, 'description': 'Built responsive UIs with React'}
        ],
        'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'GraphQL'],
        'education': {'degree': 'BS Software Engineering', 'university': 'UC Berkeley', 'year': 2014},
        'resume_text': 'Full stack developer with strong frontend and backend skills.'
    },
    {
        'id': 4,
        'name': 'Emily Davis',
        'email': 'emily.davis@email.com',
        'phone': '(555) 456-7890',
        'experience': [
            {'title': 'DevOps Engineer', 'company': 'CloudTech', 'years': 5, 'description': 'Managed CI/CD pipelines and cloud infrastructure'},
            {'title': 'System Administrator', 'company': 'IT Services', 'years': 3, 'description': 'Maintained servers and networks'}
        ],
        'skills': ['Kubernetes', 'Docker', 'AWS', 'Jenkins', 'Linux'],
        'education': {'degree': 'BS Information Systems', 'university': 'UT Austin', 'year': 2015},
        'resume_text': 'DevOps engineer with extensive cloud and infrastructure experience.'
    },
    {
        'id': 5,
        'name': 'David Wilson',
        'email': 'david.wilson@email.com',
        'phone': '(555) 567-8901',
        'experience': [
            {'title': 'Machine Learning Engineer', 'company': 'AI Innovations', 'years': 4, 'description': 'Developed and deployed ML models'},
            {'title': 'Software Engineer', 'company': 'Tech Startup', 'years': 2, 'description': 'Built backend services and APIs'}
        ],
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'MLOps', 'AWS'],
        'education': {'degree': 'MS Computer Science', 'university': 'Carnegie Mellon', 'year': 2018},
        'resume_text': 'ML engineer with expertise in deep learning and model deployment.'
    }
]

# Add more dummy candidates to simulate 400+ candidates
for i in range(6, 50):  # Create 45 more candidates
    skills_pool = [
        ['Python', 'JavaScript', 'React', 'AWS'],
        ['Java', 'Spring', 'MySQL', 'Docker'],
        ['C++', 'Linux', 'Embedded Systems'],
        ['TypeScript', 'Angular', 'Node.js', 'MongoDB'],
        ['Go', 'Kubernetes', 'Microservices', 'gRPC']
    ]
    DUMMY_CANDIDATES.append({
        'id': i,
        'name': f'Candidate {i}',
        'email': f'candidate{i}@email.com',
        'phone': f'(555) {100+i}-{2000+i}',
        'experience': [
            {
                'title': random.choice(['Software Engineer', 'Developer', 'Senior Developer']),
                'company': f'Company {i}',
                'years': random.randint(2, 8),
                'description': f'Worked on various projects using modern technologies'
            }
        ],
        'skills': random.choice(skills_pool),
        'education': {
            'degree': random.choice(['BS Computer Science', 'MS Computer Science', 'BS Software Engineering']),
            'university': f'University {i}',
            'year': random.randint(2010, 2020)
        },
        'resume_text': f'Experienced professional with {random.randint(3, 10)} years in software development.'
    })

# Dummy job postings
DUMMY_JOBS = [
    {
        'id': 1,
        'title': 'Senior Software Engineer',
        'company': 'Tech Corp',
        'description': '''We are looking for a Senior Software Engineer to join our team.

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
        'requirements': 'Python, JavaScript, React, AWS, Docker, Kubernetes, SQL',
        'created_at': (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        'id': 2,
        'title': 'Full Stack Developer',
        'company': 'StartupXYZ',
        'description': '''Join our fast-growing startup as a Full Stack Developer!

Requirements:
- 3+ years of full-stack development experience
- Strong skills in Python, JavaScript, and React
- Experience with Django or Flask
- Knowledge of PostgreSQL
- Understanding of microservices architecture
- Agile/Scrum experience''',
        'requirements': 'Python, JavaScript, React, Django, PostgreSQL, Microservices',
        'created_at': (datetime.now() - timedelta(days=3)).isoformat()
    },
    {
        'id': 3,
        'title': 'Machine Learning Engineer',
        'company': 'AI Innovations',
        'description': '''Machine Learning Engineer position at cutting-edge AI company.

Requirements:
- Master's degree in Computer Science or related field
- Experience with TensorFlow or PyTorch
- Strong Python programming skills
- Knowledge of deep learning architectures
- Experience with cloud ML platforms
- Published research papers (preferred)''',
        'requirements': 'Python, TensorFlow, PyTorch, Deep Learning, AWS, MLOps',
        'created_at': (datetime.now() - timedelta(days=1)).isoformat()
    }
]

# Store optimization results (simulating database)
OPTIMIZATION_RESULTS = {}

@app.route('/')
def index():
    """Recruiter dashboard."""
    return render_template('recruiter_dashboard.html')

@app.route('/review/<int:job_id>')
def review_interface(job_id):
    """Review interface for before/after comparison."""
    return render_template('review_interface.html', job_id=job_id)

# ==================== API Endpoints ====================

@app.route('/api/recruiter/candidates', methods=['GET'])
def get_candidates():
    """Get candidates from database (dummy data)."""
    try:
        # Simulate filtering
        status = request.args.get('status')
        skills_filter = request.args.getlist('skills')
        limit = int(request.args.get('limit', 50))
        search = request.args.get('search', '').lower()
        
        candidates = DUMMY_CANDIDATES.copy()
        
        # Filter by search
        if search:
            candidates = [
                c for c in candidates
                if search in c['name'].lower() or search in c['email'].lower()
            ]
        
        # Filter by skills
        if skills_filter:
            candidates = [
                c for c in candidates
                if any(skill in c['skills'] for skill in skills_filter)
            ]
        
        # Limit results
        candidates = candidates[:limit]
        
        return jsonify({
            'success': True,
            'candidates': candidates,
            'count': len(candidates),
            'total_available': len(DUMMY_CANDIDATES)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get single candidate."""
    candidate = next((c for c in DUMMY_CANDIDATES if c['id'] == candidate_id), None)
    if not candidate:
        return jsonify({'success': False, 'error': 'Candidate not found'}), 404
    
    return jsonify({
        'success': True,
        'candidate': candidate
    })


@app.route('/api/recruiter/jobs', methods=['GET'])
def get_jobs():
    """Get job postings."""
    return jsonify({
        'success': True,
        'jobs': DUMMY_JOBS
    })


@app.route('/api/recruiter/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get single job posting."""
    job = next((j for j in DUMMY_JOBS if j['id'] == job_id), None)
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job': job
    })


@app.route('/api/recruiter/optimize/bulk', methods=['POST'])
def bulk_optimize():
    """Bulk optimize candidates for a job."""
    try:
        data = request.get_json()
        candidate_ids = data.get('candidate_ids', [])
        job_id = data.get('job_id')
        
        if not candidate_ids or not job_id:
            return jsonify({
                'success': False,
                'error': 'candidate_ids and job_id required'
            }), 400
        
        # Get job
        job = next((j for j in DUMMY_JOBS if j['id'] == job_id), None)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Get candidates
        candidates = [
            c for c in DUMMY_CANDIDATES
            if c['id'] in candidate_ids
        ]
        
        if not candidates:
            return jsonify({'success': False, 'error': 'No candidates found'}), 404
        
        # Check cache first (for scalability)
        results = []
        job_description = job['description']
        cached_count = 0
        
        for candidate in candidates:
            # Check cache
            cached_result = optimization_cache.get(candidate['id'], job_id)
            if cached_result:
                cached_count += 1
                results.append(cached_result)
                continue
            
            # Convert candidate to resume text
            resume_text = candidate_to_resume_text(candidate)
            
            # Simulate optimization (in real version, call Groq API)
            optimized_text = simulate_optimization(resume_text, job_description)
            match_score = calculate_match_score(candidate, job)
            
            result = {
                'candidate_id': candidate['id'],
                'status': 'success',
                'original_data': candidate,
                'original_resume': resume_text,
                'optimized_resume': optimized_text,
                'match_score': match_score,
                'quality_score': round(random.uniform(75, 95), 1),
                'changes': [
                    'Added relevant keywords from job description',
                    'Improved action verbs',
                    'Enhanced technical skills section',
                    'Reordered content for better ATS compatibility'
                ],
                'created_at': datetime.now().isoformat()
            }
            results.append(result)
            
            # Cache the result (for scalability)
            optimization_cache.set(candidate['id'], job_id, result)
        
        # Store results
        if job_id not in OPTIMIZATION_RESULTS:
            OPTIMIZATION_RESULTS[job_id] = {}
        
        for result in results:
            OPTIMIZATION_RESULTS[job_id][result['candidate_id']] = result
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'total_candidates': len(candidates),
            'results': results,
            'summary': {
                'successful': len([r for r in results if r['status'] == 'success']),
                'failed': len([r for r in results if r['status'] == 'error']),
                'cached': cached_count,
                'processed': len(candidates) - cached_count
            },
            'cache_stats': optimization_cache.stats()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/review/<int:job_id>', methods=['GET'])
def get_review_queue(job_id):
    """Get candidates ready for review."""
    try:
        if job_id not in OPTIMIZATION_RESULTS:
            return jsonify({
                'success': True,
                'job_id': job_id,
                'candidates': []
            })
        
        results = OPTIMIZATION_RESULTS[job_id]
        candidates = []
        
        for candidate_id, result in results.items():
            candidate = next((c for c in DUMMY_CANDIDATES if c['id'] == candidate_id), None)
            if candidate:
                candidates.append({
                    'candidate_id': candidate_id,
                    'candidate_name': candidate['name'],
                    'match_score': result.get('match_score', 0),
                    'quality_score': result.get('quality_score', 0),
                    'status': result.get('status', 'pending'),
                    'created_at': result.get('created_at')
                })
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'candidates': candidates
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/review/compare/<int:candidate_id>', methods=['GET'])
def compare_candidate(candidate_id):
    """Get before/after comparison for a candidate."""
    try:
        job_id = int(request.args.get('job_id'))
        
        if job_id not in OPTIMIZATION_RESULTS:
            return jsonify({'success': False, 'error': 'No optimization found'}), 404
        
        if candidate_id not in OPTIMIZATION_RESULTS[job_id]:
            return jsonify({'success': False, 'error': 'Candidate optimization not found'}), 404
        
        result = OPTIMIZATION_RESULTS[job_id][candidate_id]
        candidate = next((c for c in DUMMY_CANDIDATES if c['id'] == candidate_id), None)
        
        return jsonify({
            'success': True,
            'candidate_id': candidate_id,
            'candidate': candidate,
            'original': result['original_resume'],
            'optimized': result['optimized_resume'],
            'match_score': result['match_score'],
            'quality_score': result['quality_score'],
            'changes': result.get('changes', [])
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/approve', methods=['POST'])
def approve_optimization():
    """Approve an optimization."""
    try:
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        job_id = data.get('job_id')
        
        if job_id not in OPTIMIZATION_RESULTS:
            return jsonify({'success': False, 'error': 'Optimization not found'}), 404
        
        if candidate_id not in OPTIMIZATION_RESULTS[job_id]:
            return jsonify({'success': False, 'error': 'Candidate optimization not found'}), 404
        
        # Mark as approved
        OPTIMIZATION_RESULTS[job_id][candidate_id]['status'] = 'approved'
        OPTIMIZATION_RESULTS[job_id][candidate_id]['approved_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Optimization approved'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/approve/bulk', methods=['POST'])
def bulk_approve():
    """Bulk approve optimizations."""
    try:
        data = request.get_json()
        candidate_ids = data.get('candidate_ids', [])
        job_id = data.get('job_id')
        
        if job_id not in OPTIMIZATION_RESULTS:
            return jsonify({'success': False, 'error': 'Optimization not found'}), 404
        
        approved = 0
        for candidate_id in candidate_ids:
            if candidate_id in OPTIMIZATION_RESULTS[job_id]:
                OPTIMIZATION_RESULTS[job_id][candidate_id]['status'] = 'approved'
                OPTIMIZATION_RESULTS[job_id][candidate_id]['approved_at'] = datetime.now().isoformat()
                approved += 1
        
        return jsonify({
            'success': True,
            'approved': approved,
            'total': len(candidate_ids)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data."""
    total_optimizations = sum(len(results) for results in OPTIMIZATION_RESULTS.values())
    approved = sum(
        1 for results in OPTIMIZATION_RESULTS.values()
        for r in results.values()
        if r.get('status') == 'approved'
    )
    
    return jsonify({
        'success': True,
        'analytics': {
            'total_candidates': len(DUMMY_CANDIDATES),
            'total_jobs': len(DUMMY_JOBS),
            'total_optimizations': total_optimizations,
            'approved_optimizations': approved,
            'pending_review': total_optimizations - approved
        }
    })


# Helper functions
def candidate_to_resume_text(candidate):
    """Convert candidate data to resume text format."""
    parts = []
    parts.append(candidate['name'])
    if candidate.get('email'):
        parts.append(f"Email: {candidate['email']}")
    if candidate.get('phone'):
        parts.append(f"Phone: {candidate['phone']}")
    
    parts.append("\nEXPERIENCE")
    for exp in candidate.get('experience', []):
        parts.append(f"{exp['title']} | {exp['company']} | {exp['years']} years")
        if exp.get('description'):
            parts.append(f"- {exp['description']}")
    
    parts.append("\nSKILLS")
    parts.append(", ".join(candidate.get('skills', [])))
    
    parts.append("\nEDUCATION")
    edu = candidate.get('education', {})
    parts.append(f"{edu.get('degree', '')} - {edu.get('university', '')} ({edu.get('year', '')})")
    
    if candidate.get('resume_text'):
        parts.append(f"\n{candidate['resume_text']}")
    
    return "\n".join(parts)


def simulate_optimization(resume_text, job_description):
    """Simulate optimization (in real version, uses Groq API)."""
    # This is a simplified simulation
    # In production, this would call Groq API
    optimized = resume_text + "\n\n[OPTIMIZED VERSION]\n"
    optimized += "Enhanced with relevant keywords from job description.\n"
    optimized += "Improved action verbs and quantifiable achievements.\n"
    optimized += "Reordered content to highlight most relevant experience.\n"
    optimized += "Optimized for ATS compatibility."
    return optimized


def calculate_match_score(candidate, job):
    """Calculate match score."""
    candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
    job_text = (job['description'] + ' ' + job.get('requirements', '')).lower()
    
    # Extract keywords from job
    job_words = set(word for word in job_text.split() if len(word) > 3)
    
    matching = len(job_words.intersection(candidate_skills))
    total_keywords = len(job_words)
    
    if total_keywords == 0:
        return 0.0
    
    return round((matching / total_keywords) * 100, 1)


if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5000):
        for port in range(start_port, start_port + 10):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        return 5000
    
    port = find_free_port(5000)
    
    print("\n" + "="*70)
    print("🎯 INTERNAL RECRUITER TOOL - Resume Optimizer")
    print("="*70)
    print("\n✅ This is the CORRECT version:")
    print("   - For INTERNAL RECRUITERS (not job seekers)")
    print("   - Bulk processing (50+ candidates available)")
    print("   - Review & approval workflow")
    print("   - NO file parsing - uses structured data")
    print("   - Dummy data included (no database needed)")
    print("\n" + "="*70)
    print(f"🌐 Open: http://localhost:{port}")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)

