"""
Internal Recruiter Tool - Beautiful UI Version
Works without Redis/Celery - perfect for testing the new UI!
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
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

# Add more dummy candidates
for i in range(6, 50):
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
            {'title': f'Software Engineer {i}', 'company': f'Company {i}', 'years': random.randint(2, 8), 'description': f'Worked on various projects'}
        ],
        'skills': random.choice(skills_pool),
        'education': {'degree': 'BS Computer Science', 'university': 'University', 'year': 2015 + random.randint(0, 5)},
        'resume_text': f'Experienced professional with {random.randint(3, 10)} years of experience.'
    })

DUMMY_JOBS = [
    {
        'id': 1,
        'title': 'Senior Software Engineer',
        'company': 'Tech Corp',
        'description': 'We are looking for a Senior Software Engineer with experience in Python, JavaScript, and cloud technologies. You will work on building scalable web applications and APIs.',
        'requirements': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'required_years': 5,
        'created_at': (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'company': 'DataCorp',
        'description': 'Join our data science team to build ML models and perform advanced analytics. Experience with Python, TensorFlow, and SQL required.',
        'requirements': ['Python', 'TensorFlow', 'SQL', 'R'],
        'required_years': 3,
        'created_at': (datetime.now() - timedelta(days=3)).isoformat()
    },
    {
        'id': 3,
        'title': 'Full Stack Developer',
        'company': 'WebSolutions',
        'description': 'Full stack developer needed for modern web applications. Must have experience with React, Node.js, and databases.',
        'requirements': ['JavaScript', 'React', 'Node.js', 'MongoDB'],
        'required_years': 4,
        'created_at': (datetime.now() - timedelta(days=1)).isoformat()
    }
]

OPTIMIZATION_RESULTS = {}


def candidate_to_resume_text(candidate):
    """Convert candidate data to resume text."""
    lines = []
    lines.append(f"{candidate.get('name', '')}")
    lines.append(f"Email: {candidate.get('email', '')}")
    lines.append(f"Phone: {candidate.get('phone', '')}")
    lines.append("")
    
    lines.append("EXPERIENCE")
    for exp in candidate.get('experience', []):
        lines.append(f"{exp.get('title', '')} at {exp.get('company', '')} ({exp.get('years', 0)} years)")
        lines.append(exp.get('description', ''))
        lines.append("")
    
    lines.append("SKILLS")
    lines.append(", ".join(candidate.get('skills', [])))
    lines.append("")
    
    edu = candidate.get('education', {})
    if edu:
        lines.append("EDUCATION")
        lines.append(f"{edu.get('degree', '')} - {edu.get('university', '')} ({edu.get('year', '')})")
    
    return "\n".join(lines)


def simulate_optimization(resume_text, job_description):
    """Simulate optimization (in real version, this uses Groq API)."""
    optimized = resume_text
    # Add some simulated improvements
    optimized += "\n\n[OPTIMIZED] Added relevant keywords from job description"
    optimized += "\n[OPTIMIZED] Improved action verbs"
    optimized += "\n[OPTIMIZED] Enhanced technical skills section"
    return optimized


def calculate_match_score(candidate, job):
    """Calculate match score between candidate and job."""
    score = 0.0
    max_score = 100.0
    
    # Skills match (40 points)
    candidate_skills = set(s.lower() for s in candidate.get('skills', []))
    job_requirements = job.get('requirements', [])
    job_skills = set(s.lower() for s in job_requirements)
    
    if job_skills:
        matched_skills = candidate_skills.intersection(job_skills)
        skill_score = (len(matched_skills) / len(job_skills)) * 40
        score += min(skill_score, 40)
    
    # Experience match (30 points)
    required_years = job.get('required_years', 0)
    candidate_years = sum(exp.get('years', 0) for exp in candidate.get('experience', []))
    if required_years > 0:
        exp_score = min((candidate_years / required_years) * 30, 30)
        score += exp_score
    else:
        score += 15
    
    # Title match (30 points)
    job_title = job.get('title', '').lower()
    for exp in candidate.get('experience', []):
        exp_title = exp.get('title', '').lower()
        if job_title in exp_title or exp_title in job_title:
            score += 30
            break
    
    return round(min(score, max_score), 1)


@app.route('/')
def index():
    """Main dashboard."""
    return render_template('recruiter.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'redis': False,
            'celery': False,
            'cache': {'backend': 'in-memory'}
        },
        'performance': {
            'total_optimizations': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0
        }
    })


@app.route('/api/recruiter/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data."""
    return jsonify({
        'success': True,
        'analytics': {
            'total_candidates': len(DUMMY_CANDIDATES),
            'total_jobs': len(DUMMY_JOBS),
            'total_optimizations': sum(len(results) for results in OPTIMIZATION_RESULTS.values()),
            'pending_review': sum(
                len([r for r in results.values() if r.get('status') == 'pending'])
                for results in OPTIMIZATION_RESULTS.values()
            )
        }
    })


@app.route('/api/recruiter/candidates', methods=['GET'])
def get_candidates():
    """Get candidates with filtering."""
    try:
        limit = int(request.args.get('limit', 50))
        skills_filter = request.args.getlist('skills')
        search = request.args.get('search', '').lower()
        
        candidates = DUMMY_CANDIDATES.copy()
        
        # Filter by search
        if search:
            candidates = [
                c for c in candidates
                if search in c.get('name', '').lower() or search in c.get('email', '').lower()
            ]
        
        # Filter by skills
        if skills_filter:
            candidates = [
                c for c in candidates
                if any(skill in c.get('skills', []) for skill in skills_filter)
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
        
        # Simulate optimization
        results = []
        job_description = job['description']
        
        for candidate in candidates:
            # Convert candidate to resume text
            resume_text = candidate_to_resume_text(candidate)
            
            # Simulate optimization
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
                'cached': 0,
                'processed': len(candidates)
            }
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


@app.route('/api/recruiter/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    return jsonify({
        'success': True,
        'performance': {
            'total_optimizations': sum(len(results) for results in OPTIMIZATION_RESULTS.values()),
            'successful_optimizations': sum(
                len([r for r in results.values() if r.get('status') == 'success'])
                for results in OPTIMIZATION_RESULTS.values()
            ),
            'failed_optimizations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'success_rate': 100.0,
            'cache_hit_rate': 0.0,
            'average_processing_time': 0.0
        },
        'cache': {
            'total_entries': 0,
            'active_entries': 0,
            'backend': 'in-memory'
        },
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5000, max_port=5100):
        """Find a free port."""
        for port in range(start_port, max_port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No free port found")
    
    port = find_free_port()
    
    print("\n" + "="*60)
    print("✨ Beautiful UI Recruiter Tool - Starting...")
    print("="*60)
    print(f"📱 Dashboard: http://localhost:{port}/")
    print(f"❤️  Health: http://localhost:{port}/api/health")
    print(f"📊 Stats: http://localhost:{port}/api/recruiter/stats")
    print("="*60)
    print("\n🎨 Enjoy the beautiful new UI!")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=port, debug=True, threaded=True, use_reloader=False)

