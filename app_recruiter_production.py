"""
Internal Recruiter Tool - Production Version
Scalable system for 1000+ resumes/day with async processing, caching, and monitoring.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
import logging

# Import services
from services.cache_manager import optimization_cache
from services.monitoring import performance_monitor, setup_logging
from services.optimization_tasks import optimize_single_candidate_task, optimize_bulk_candidates_task
from config.celery_config import celery_app

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

# Dummy data (replace with database queries in production)
DUMMY_CANDIDATES = []  # Load from database
DUMMY_JOBS = []  # Load from database
OPTIMIZATION_RESULTS = {}  # Store in database in production


@app.route('/')
def index():
    """Main dashboard."""
    return render_template('recruiter.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check Redis
        cache_stats = optimization_cache.stats()
        redis_available = cache_stats.get('backend') == 'redis'
        
        # Check Celery
        celery_available = False
        try:
            celery_app.control.inspect().active()
            celery_available = True
        except:
            pass
        
        # Get performance stats
        perf_stats = performance_monitor.get_stats()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'redis': redis_available,
                'celery': celery_available,
                'cache': cache_stats
            },
            'performance': perf_stats
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'degraded',
            'error': str(e)
        }), 500


@app.route('/api/recruiter/candidates', methods=['GET'])
@limiter.limit("100 per minute")
def get_candidates():
    """Get candidates with filtering."""
    try:
        limit = int(request.args.get('limit', 50))
        skills_filter = request.args.getlist('skills')
        search = request.args.get('search', '').lower()
        
        # In production: query from database
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
        logger.error(f"Error getting candidates: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/jobs', methods=['GET'])
@limiter.limit("100 per minute")
def get_jobs():
    """Get job postings."""
    try:
        # In production: query from database
        return jsonify({
            'success': True,
            'jobs': DUMMY_JOBS
        })
    except Exception as e:
        logger.error(f"Error getting jobs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/optimize/bulk', methods=['POST'])
@limiter.limit("10 per minute")  # Lower limit for expensive operations
def bulk_optimize():
    """
    Bulk optimize candidates - async processing.
    Returns task ID immediately, use /api/recruiter/tasks/<task_id> to check status.
    """
    try:
        data = request.get_json()
        candidate_ids = data.get('candidate_ids', [])
        job_id = data.get('job_id')
        
        if not candidate_ids or not job_id:
            return jsonify({
                'success': False,
                'error': 'candidate_ids and job_id required'
            }), 400
        
        # Get job (from database in production)
        job = next((j for j in DUMMY_JOBS if j['id'] == job_id), None)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Get candidates (from database in production)
        candidates = [
            c for c in DUMMY_CANDIDATES
            if c['id'] in candidate_ids
        ]
        
        if not candidates:
            return jsonify({'success': False, 'error': 'No candidates found'}), 404
        
        # Queue async task
        task = optimize_bulk_candidates_task.delay(
            candidate_ids=candidate_ids,
            job_id=job_id,
            candidates_data=candidates,
            job_description=job
        )
        
        logger.info(f"Queued bulk optimization task {task.id} for {len(candidates)} candidates")
        
        return jsonify({
            'success': True,
            'task_id': task.id,
            'status': 'queued',
            'message': f'Processing {len(candidates)} candidates in background',
            'check_status_url': f'/api/recruiter/tasks/{task.id}'
        })
    
    except Exception as e:
        logger.error(f"Error queuing bulk optimization: {e}")
        performance_monitor.record_error('bulk_optimize', str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/optimize/single', methods=['POST'])
@limiter.limit("30 per minute")
def optimize_single():
    """
    Optimize single candidate - async processing.
    Returns task ID immediately.
    """
    try:
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        job_id = data.get('job_id')
        
        if not candidate_id or not job_id:
            return jsonify({
                'success': False,
                'error': 'candidate_id and job_id required'
            }), 400
        
        # Get candidate and job (from database in production)
        candidate = next((c for c in DUMMY_CANDIDATES if c['id'] == candidate_id), None)
        job = next((j for j in DUMMY_JOBS if j['id'] == job_id), None)
        
        if not candidate:
            return jsonify({'success': False, 'error': 'Candidate not found'}), 404
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Queue async task
        task = optimize_single_candidate_task.delay(
            candidate_id=candidate_id,
            job_id=job_id,
            candidate_data=candidate,
            job_description=job
        )
        
        logger.info(f"Queued optimization task {task.id} for candidate {candidate_id}")
        
        return jsonify({
            'success': True,
            'task_id': task.id,
            'status': 'queued',
            'check_status_url': f'/api/recruiter/tasks/{task.id}'
        })
    
    except Exception as e:
        logger.error(f"Error queuing optimization: {e}")
        performance_monitor.record_error('optimize_single', str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/tasks/<task_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_task_status(task_id):
    """Get status of async task."""
    try:
        task = celery_app.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Waiting to be processed...'
            }
        elif task.state == 'PROCESSING':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Processing...',
                'meta': task.info
            }
        elif task.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Completed',
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Failed',
                'error': str(task.info)
            }
        else:
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': task.info
            }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/stats', methods=['GET'])
@limiter.limit("60 per minute")
def get_stats():
    """Get system statistics and performance metrics."""
    try:
        stats = performance_monitor.get_stats()
        cache_stats = optimization_cache.stats()
        
        return jsonify({
            'success': True,
            'performance': stats,
            'cache': cache_stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recruiter/review/<int:job_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_review_queue(job_id):
    """Get candidates ready for review."""
    try:
        # In production: query from database
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
                    'candidate_name': candidate.get('name', ''),
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
        logger.error(f"Error getting review queue: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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
    print("🚀 Production Recruiter Tool - Starting...")
    print("="*60)
    print(f"📊 Monitoring: http://localhost:{port}/api/recruiter/stats")
    print(f"❤️  Health: http://localhost:{port}/api/health")
    print(f"📱 Dashboard: http://localhost:{port}/")
    print("="*60)
    print("\n⚠️  Make sure Redis and Celery workers are running!")
    print("   Start Redis: redis-server")
    print("   Start Celery: celery -A config.celery_config worker --loglevel=info")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

