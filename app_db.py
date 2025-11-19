"""
Enhanced Web Application with PostgreSQL Database Integration
Full-featured resume optimizer with database storage and management.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import json
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.file_parser import parse_resume
from resume_optimizer import ResumeOptimizer
from utils.groq_optimizer import GroqResumeOptimizer
from database import (
    create_tables, ResumeDB, JobDescriptionDB, OptimizationDB,
    Resume, JobDescription, Optimization
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for API calls)

# Fix for 403 errors - ensure proper routing
@app.before_request
def handle_preflight():
    """Handle CORS preflight requests."""
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        headers = list(response.headers)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database tables on startup (non-blocking)
def init_database():
    """Initialize database tables (non-blocking)."""
    try:
        create_tables()
        return True
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        print("   The app will start but database features may not work.")
        print("   Make sure PostgreSQL is running and database is created.")
        return False

# Try to initialize database, but don't block app startup
DB_AVAILABLE = init_database()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def serialize_resume(resume):
    """Serialize resume object to dict."""
    return {
        'id': resume.id,
        'name': resume.name,
        'filename': resume.filename,
        'file_type': resume.file_type,
        'word_count': resume.word_count,
        'created_at': resume.created_at.isoformat() if resume.created_at else None,
        'updated_at': resume.updated_at.isoformat() if resume.updated_at else None
    }


def serialize_job(job):
    """Serialize job description object to dict."""
    return {
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'content': job.content[:500] + '...' if len(job.content) > 500 else job.content,
        'source_url': job.source_url,
        'created_at': job.created_at.isoformat() if job.created_at else None
    }


def serialize_optimization(opt):
    """Serialize optimization object to dict."""
    return {
        'id': opt.id,
        'resume_id': opt.resume_id,
        'job_description_id': opt.job_description_id,
        'quality_score': opt.quality_score,
        'match_score': opt.match_score,
        'optimization_type': opt.optimization_type,
        'model_used': opt.model_used,
        'api_provider': opt.api_provider,
        'created_at': opt.created_at.isoformat() if opt.created_at else None,
        'has_optimized_resume': bool(opt.optimized_resume),
        'suggestions_count': len(opt.suggestions) if opt.suggestions else 0
    }


@app.route('/')
def index():
    """Render main page."""
    return render_template('app_db.html')


# ==================== Resume Management ====================

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """Get all resumes."""
    if not DB_AVAILABLE:
        return jsonify({'success': False, 'error': 'Database not available. Please check your database connection.'}), 503
    try:
        resumes = ResumeDB.get_all()
        return jsonify({
            'success': True,
            'resumes': [serialize_resume(r) for r in resumes]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/resumes', methods=['POST'])
def create_resume():
    """Create a new resume."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        name = request.form.get('name', file.filename)
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Parse resume
        content = parse_resume(filepath)
        if not content:
            os.remove(filepath)
            return jsonify({'success': False, 'error': 'Could not parse file'}), 400
        
        # Get file type
        file_type = filename.rsplit('.', 1)[1].lower()
        word_count = len(content.split())
        
        # Save to database
        resume = ResumeDB.create(
            name=name,
            filename=filename,
            content=content,
            file_type=file_type,
            word_count=word_count
        )
        
        # Clean up temp file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'resume': serialize_resume(resume)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume by ID."""
    try:
        resume = ResumeDB.get_by_id(resume_id)
        if not resume:
            return jsonify({'success': False, 'error': 'Resume not found'}), 404
        
        return jsonify({
            'success': True,
            'resume': {
                **serialize_resume(resume),
                'content': resume.content
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete resume."""
    try:
        success = ResumeDB.delete(resume_id)
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Resume not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Job Description Management ====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all job descriptions."""
    try:
        jobs = JobDescriptionDB.get_all()
        return jsonify({
            'success': True,
            'jobs': [serialize_job(j) for j in jobs]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job description."""
    try:
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({'success': False, 'error': 'Content required'}), 400
        
        job = JobDescriptionDB.create(
            title=data.get('title', 'Untitled Job'),
            company=data.get('company'),
            content=data['content'],
            source_url=data.get('source_url')
        )
        
        return jsonify({
            'success': True,
            'job': serialize_job(job)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job description by ID."""
    try:
        job = JobDescriptionDB.get_by_id(job_id)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        return jsonify({
            'success': True,
            'job': {
                **serialize_job(job),
                'content': job.content
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete job description."""
    try:
        success = JobDescriptionDB.delete(job_id)
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Optimization ====================

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Optimize resume for job description."""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        optimization_type = data.get('optimization_type', 'complete')
        use_groq = data.get('use_groq', True)
        groq_api_key = data.get('groq_api_key') or os.getenv('GROQ_API_KEY')
        
        if not resume_id or not job_id:
            return jsonify({'success': False, 'error': 'Resume ID and Job ID required'}), 400
        
        # Get resume and job
        resume = ResumeDB.get_by_id(resume_id)
        job = JobDescriptionDB.get_by_id(job_id)
        
        if not resume or not job:
            return jsonify({'success': False, 'error': 'Resume or Job not found'}), 404
        
        # Basic analysis first
        basic_optimizer = ResumeOptimizer(resume.content, job.content)
        basic_analysis = basic_optimizer.get_comprehensive_analysis()
        
        optimized_resume = None
        model_used = None
        api_provider = 'basic'
        
        # Groq optimization if requested
        if use_groq and groq_api_key:
            try:
                groq_optimizer = GroqResumeOptimizer(groq_api_key)
                if groq_optimizer.is_available():
                    if optimization_type == 'complete':
                        result = groq_optimizer.create_optimized_resume(
                            resume.content, job.content
                        )
                        if 'optimized_resume' in result:
                            optimized_resume = result['optimized_resume']
                            model_used = 'llama-3.1-70b-versatile'
                            api_provider = 'groq'
                    elif optimization_type == 'keywords':
                        result = groq_optimizer.generate_keyword_suggestions(
                            resume.content, job.content
                        )
                        if 'suggestions' in result:
                            basic_analysis['groq_keyword_suggestions'] = result['suggestions']
            except Exception as e:
                print(f"Groq optimization error: {e}")
        
        # Save optimization to database
        optimization = OptimizationDB.create(
            resume_id=resume_id,
            job_description_id=job_id,
            optimized_resume=optimized_resume,
            original_resume=resume.content,
            quality_score=basic_analysis.get('resume_quality', {}).get('quality_score'),
            match_score=basic_analysis.get('job_match', {}).get('score') if 'job_match' in basic_analysis else None,
            analysis_data=basic_analysis,
            suggestions=basic_analysis.get('suggestions', []),
            matching_keywords=basic_analysis.get('job_match', {}).get('matching_keywords') if 'job_match' in basic_analysis else None,
            missing_keywords=basic_analysis.get('job_match', {}).get('missing_keywords') if 'job_match' in basic_analysis else None,
            optimization_type=optimization_type,
            model_used=model_used,
            api_provider=api_provider
        )
        
        return jsonify({
            'success': True,
            'optimization': serialize_optimization(optimization),
            'analysis': basic_analysis,
            'optimized_resume': optimized_resume
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/optimizations', methods=['GET'])
def get_optimizations():
    """Get all optimizations."""
    try:
        resume_id = request.args.get('resume_id', type=int)
        job_id = request.args.get('job_id', type=int)
        
        if resume_id:
            optimizations = OptimizationDB.get_by_resume(resume_id)
        elif job_id:
            optimizations = OptimizationDB.get_all()  # Filter by job if needed
        else:
            optimizations = OptimizationDB.get_all()
        
        return jsonify({
            'success': True,
            'optimizations': [serialize_optimization(o) for o in optimizations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/optimizations/<int:opt_id>', methods=['GET'])
def get_optimization(opt_id):
    """Get optimization by ID."""
    try:
        optimization = OptimizationDB.get_by_id(opt_id)
        if not optimization:
            return jsonify({'success': False, 'error': 'Optimization not found'}), 404
        
        # Add history entry
        OptimizationDB.add_history(opt_id, 'viewed')
        
        return jsonify({
            'success': True,
            'optimization': {
                **serialize_optimization(optimization),
                'optimized_resume': optimization.optimized_resume,
                'original_resume': optimization.original_resume,
                'analysis_data': optimization.analysis_data,
                'suggestions': optimization.suggestions,
                'matching_keywords': optimization.matching_keywords,
                'missing_keywords': optimization.missing_keywords
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/optimizations/<int:opt_id>', methods=['DELETE'])
def delete_optimization(opt_id):
    """Delete optimization."""
    try:
        success = OptimizationDB.delete(opt_id)
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Optimization not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Analytics ====================

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data."""
    try:
        resumes = ResumeDB.get_all()
        jobs = JobDescriptionDB.get_all()
        optimizations = OptimizationDB.get_all()
        
        # Calculate statistics
        total_resumes = len(resumes)
        total_jobs = len(jobs)
        total_optimizations = len(optimizations)
        
        avg_match_score = 0
        avg_quality_score = 0
        if optimizations:
            match_scores = [o.match_score for o in optimizations if o.match_score]
            quality_scores = [o.quality_score for o in optimizations if o.quality_score]
            avg_match_score = sum(match_scores) / len(match_scores) if match_scores else 0
            avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_resumes': total_resumes,
                'total_jobs': total_jobs,
                'total_optimizations': total_optimizations,
                'avg_match_score': round(avg_match_score, 2),
                'avg_quality_score': round(avg_quality_score, 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    db_status = 'unknown'
    db_error = None
    
    if DB_AVAILABLE:
        try:
            # Test database connection
            resumes = ResumeDB.get_all()
            db_status = 'connected'
        except Exception as e:
            db_status = 'disconnected'
            db_error = str(e)
    else:
        db_status = 'not_initialized'
    
    return jsonify({
        'status': 'running',
        'database': db_status,
        'database_error': db_error,
        'groq_configured': bool(os.getenv('GROQ_API_KEY')),
        'app_ready': True
    })


if __name__ == '__main__':
    print("🚀 Starting Resume Optimizer with Database...")
    print("📱 Open http://localhost:5000 in your browser")
    
    if DB_AVAILABLE:
        print("✅ Database connection successful!")
    else:
        print("⚠️  Database not available - some features may not work")
        print("   To fix: Make sure PostgreSQL is running and database is created")
        print("   Or use SQLite: export DB_TYPE=sqlite")
        print("   Run: python setup_database.py")
    
    print("\n" + "="*60)
    print("🌐 Application URL: http://localhost:5000")
    print("   Alternative: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    # Check if port is available
    import socket
    port = 5000
    
    def is_port_available(port):
        """Check if a port is available."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return True
            except OSError:
                return False
    
    if not is_port_available(port):
        print(f"⚠️  Port {port} is already in use!")
        print(f"   Trying port {port + 1} instead...")
        port = port + 1
        print(f"   Use: http://localhost:{port}\n")
    
    try:
        # Use 0.0.0.0 to allow connections from localhost
        # This fixes the 403 error
        app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
    except PermissionError:
        print(f"❌ Permission denied on port {port}")
        print("   Try running with sudo or use a different port")
        print("   Or change port in the code to 5001 or 8080")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print(f"   Try: python app_db.py (it will auto-select another port)")
            print(f"   Or manually change port to 5001 in the code")
        else:
            print(f"❌ Error starting server: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Check if port is already in use: lsof -i :5000")
            print("   2. Try a different port")
            print("   3. Check firewall settings")
        raise
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if port 5000 is already in use")
        print("   2. Try a different port: app.run(port=5001)")
        print("   3. Check firewall settings")
        print("   4. Make sure Flask is installed: pip install flask")
        raise

