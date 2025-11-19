"""
Recruiter API - Endpoints for internal recruiter tool
This is the CORRECT API for your use case.
"""

from flask import Blueprint, request, jsonify
from integration.database_connector import DatabaseConnector
from services.bulk_optimizer import BulkOptimizer
import os

recruiter_bp = Blueprint('recruiter', __name__)

# Initialize connectors
db_connector = DatabaseConnector()
bulk_optimizer = BulkOptimizer(groq_api_key=os.getenv('GROQ_API_KEY'))


@recruiter_bp.route('/api/recruiter/candidates', methods=['GET'])
def get_candidates():
    """
    Get candidates from YOUR database.
    No file upload - reads from your existing database.
    """
    try:
        # Get filters from query parameters
        filters = {
            'status': request.args.get('status'),
            'skills': request.args.getlist('skills'),
            'limit': int(request.args.get('limit', 400))
        }
        
        candidates = db_connector.get_candidates(filters=filters)
        
        return jsonify({
            'success': True,
            'candidates': candidates,
            'count': len(candidates)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recruiter_bp.route('/api/recruiter/optimize/bulk', methods=['POST'])
def bulk_optimize():
    """
    Bulk optimize candidates for a job.
    Processes 400+ candidates at once.
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
        
        # Get job posting
        job = db_connector.get_job_posting(job_id)
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job posting not found'
            }), 404
        
        # Get candidates
        candidates = []
        for candidate_id in candidate_ids:
            candidate = db_connector.get_candidate_by_id(candidate_id)
            if candidate:
                candidates.append(candidate)
        
        if not candidates:
            return jsonify({
                'success': False,
                'error': 'No candidates found'
            }), 404
        
        # Progress tracking
        progress_data = {
            'total': len(candidates),
            'completed': 0,
            'errors': 0,
            'status': 'processing'
        }
        
        # Optimize in bulk
        job_description = job.get('description', '') + ' ' + job.get('requirements', '')
        results = bulk_optimizer.optimize_candidates_bulk(
            candidates=candidates,
            job_description=job_description,
            progress_callback=lambda current, total, cid, status: update_progress(current, total, status)
        )
        
        def update_progress(current, total, status):
            progress_data['completed'] = current
            if status == 'error':
                progress_data['errors'] += 1
        
        # Store results (you'll need to implement this)
        # optimization_results_db.save_bulk(results, job_id)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'total_candidates': len(candidates),
            'results': results,
            'summary': {
                'successful': len([r for r in results if r['status'] == 'success']),
                'failed': len([r for r in results if r['status'] == 'error'])
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recruiter_bp.route('/api/recruiter/review/<int:job_id>', methods=['GET'])
def get_review_queue(job_id):
    """
    Get candidates ready for review (optimized but not approved).
    """
    try:
        # TODO: Get from optimization_results table
        # This should return candidates with their before/after data
        return jsonify({
            'success': True,
            'job_id': job_id,
            'candidates': []  # TODO: Implement
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recruiter_bp.route('/api/recruiter/review/compare/<int:candidate_id>', methods=['GET'])
def compare_candidate(candidate_id):
    """
    Get before/after comparison for a candidate.
    """
    try:
        job_id = request.args.get('job_id')
        
        # Get original candidate
        original = db_connector.get_candidate_by_id(candidate_id)
        
        # Get optimized version
        # TODO: Get from optimization_results table
        optimized = None
        
        return jsonify({
            'success': True,
            'candidate_id': candidate_id,
            'original': original,
            'optimized': optimized,
            'changes': []  # TODO: Calculate diff
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recruiter_bp.route('/api/recruiter/approve', methods=['POST'])
def approve_optimization():
    """
    Approve an optimization - saves back to your database.
    """
    try:
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        optimized_data = data.get('optimized_data')
        
        # Update candidate in your database
        db_connector.update_candidate_optimized_data(candidate_id, optimized_data)
        
        return jsonify({
            'success': True,
            'message': 'Optimization approved and saved'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recruiter_bp.route('/api/recruiter/approve/bulk', methods=['POST'])
def bulk_approve():
    """
    Bulk approve multiple optimizations.
    """
    try:
        data = request.get_json()
        candidate_ids = data.get('candidate_ids', [])
        optimized_data_map = data.get('optimized_data', {})
        
        approved = 0
        for candidate_id in candidate_ids:
            if candidate_id in optimized_data_map:
                db_connector.update_candidate_optimized_data(
                    candidate_id,
                    optimized_data_map[candidate_id]
                )
                approved += 1
        
        return jsonify({
            'success': True,
            'approved': approved,
            'total': len(candidate_ids)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

