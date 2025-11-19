"""
Web Interface with Groq Integration
Enhanced web app with Groq-powered resume optimization.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from resume_optimizer import ResumeOptimizer
from utils.file_parser import parse_resume
from utils.groq_optimizer import GroqResumeOptimizer

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main page."""
    return render_template('index_groq.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """API endpoint to analyze resume (basic analysis)."""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save and parse file
        filename = secure_filename(resume_file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        resume_file.save(filepath)
        
        resume_text = parse_resume(filepath)
        
        if not resume_text:
            return jsonify({'error': 'Could not parse resume file'}), 400
        
        # Basic analysis
        optimizer = ResumeOptimizer(resume_text, job_description)
        analysis = optimizer.get_comprehensive_analysis()
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """API endpoint to optimize resume using Groq."""
    try:
        # Check API key
        groq_api_key = request.form.get('api_key') or os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({'error': 'Groq API key required. Set GROQ_API_KEY or provide in request.'}), 400
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if not job_description:
            return jsonify({'error': 'Job description required for optimization'}), 400
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save and parse file
        filename = secure_filename(resume_file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        resume_file.save(filepath)
        
        resume_text = parse_resume(filepath)
        
        if not resume_text:
            return jsonify({'error': 'Could not parse resume file'}), 400
        
        # Initialize Groq optimizer
        groq_optimizer = GroqResumeOptimizer(groq_api_key)
        
        if not groq_optimizer.is_available():
            return jsonify({'error': 'Groq API not available'}), 500
        
        # Get optimization type
        optimization_type = request.form.get('optimization_type', 'complete')
        
        result = {}
        
        if optimization_type == 'complete':
            # Full resume optimization
            result = groq_optimizer.create_optimized_resume(
                resume_text, job_description
            )
        elif optimization_type == 'keywords':
            # Keyword suggestions only
            result = groq_optimizer.generate_keyword_suggestions(
                resume_text, job_description
            )
        elif optimization_type == 'overall':
            # Overall analysis
            result = groq_optimizer.optimize_resume_for_job(
                resume_text, job_description
            )
        else:
            return jsonify({'error': 'Invalid optimization type'}), 400
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize-section', methods=['POST'])
def optimize_section():
    """API endpoint to optimize a specific section."""
    try:
        groq_api_key = request.form.get('api_key') or os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({'error': 'Groq API key required'}), 400
        
        section_name = request.form.get('section_name')
        section_content = request.form.get('section_content')
        job_description = request.form.get('job_description')
        
        if not all([section_name, section_content, job_description]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        groq_optimizer = GroqResumeOptimizer(groq_api_key)
        
        if not groq_optimizer.is_available():
            return jsonify({'error': 'Groq API not available'}), 500
        
        result = groq_optimizer.optimize_section(
            section_name, section_content, job_description
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    has_groq_key = bool(os.getenv('GROQ_API_KEY'))
    return jsonify({
        'status': 'healthy',
        'groq_configured': has_groq_key
    })


if __name__ == '__main__':
    print("🚀 Starting Resume Optimizer Web Application (Groq-Enhanced)...")
    print("📱 Open http://localhost:5000 in your browser")
    if os.getenv('GROQ_API_KEY'):
        print("✅ Groq API key detected")
    else:
        print("⚠️  Groq API key not set. Set GROQ_API_KEY environment variable for AI features.")
    app.run(debug=True, host='0.0.0.0', port=5000)

