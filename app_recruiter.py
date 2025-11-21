"""
CORRECT Application - Internal Recruiter Tool
This is what you actually need!
"""

from flask import Flask, render_template
from flask_cors import CORS
from api.recruiter_api import recruiter_bp
import os

app = Flask(__name__)
CORS(app)

# Register recruiter blueprint
app.register_blueprint(recruiter_bp)

@app.route('/')
def index():
    """Recruiter dashboard."""
    return render_template('recruiter_dashboard.html')

@app.route('/review/<int:job_id>')
def review_interface(job_id):
    """Review interface for before/after comparison."""
    return render_template('review_interface.html', job_id=job_id)

if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5001):
        for port in range(start_port, start_port + 10):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        return 5001
    
    port = find_free_port(5001)  # Start at 5001 to avoid AirPlay on macOS
    
    print("\n" + "="*70)
    print("🎯 INTERNAL RECRUITER TOOL - Resume Optimizer")
    print("="*70)
    print("\n✅ This is the CORRECT version:")
    print("   - Reads from YOUR database")
    print("   - Bulk processing (400+ candidates)")
    print("   - Review & approval workflow")
    print("   - NO file parsing needed!")
    print("\n" + "="*70)
    print(f"🌐 Open: http://localhost:{port}")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)

