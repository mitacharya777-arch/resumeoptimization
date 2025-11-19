"""
Simple Resume Optimizer API
Just optimize resume for a job - that's it!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.groq_optimizer import GroqResumeOptimizer

app = Flask(__name__)
CORS(app)

# Initialize optimizer
groq_optimizer = GroqResumeOptimizer()


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """
    Optimize resume for a job posting.
    
    Expected JSON:
    {
        "resume_text": "resume content here...",
        "job_description": "job description here..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description are required'
            }), 400
        
        # Check if Groq is available
        if not groq_optimizer.is_available():
            return jsonify({
                'success': False,
                'error': 'Groq API not available. Set GROQ_API_KEY environment variable.'
            }), 500
        
        # Create optimized resume
        result = groq_optimizer.create_optimized_resume(
            resume_text=resume_text,
            job_description=job_description
        )
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        return jsonify({
            'success': True,
            'optimized_resume': result.get('optimized_resume', ''),
            'original_resume': result.get('original_resume', resume_text)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        'status': 'healthy',
        'service': 'Resume Optimizer API'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n🚀 Resume Optimizer API running on http://localhost:{port}")
    print(f"📝 POST /api/optimize - Optimize resume for a job\n")
    app.run(host='127.0.0.1', port=port, debug=True)

