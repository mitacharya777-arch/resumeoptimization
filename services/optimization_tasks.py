"""
Celery Tasks - Production Queue System
Defines async tasks for resume optimization.
"""

try:
    from config.celery_config import celery_app
    CELERY_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Celery not available: {e}")
    CELERY_AVAILABLE = False
    # Create dummy celery app for fallback
    class DummyCelery:
        def task(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    celery_app = DummyCelery()

from services.bulk_optimizer import BulkOptimizer
from services.cache_manager import optimization_cache
from typing import Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import Groq optimizer, but don't fail if not available
try:
    from utils.groq_optimizer import GroqResumeOptimizer
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    GroqResumeOptimizer = None


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def optimize_single_candidate_task(
    self,
    candidate_id: int,
    job_id: int,
    candidate_data: Dict,
    job_description: Dict
) -> Dict:
    """
    Optimize a single candidate's resume for a job.
    
    Args:
        candidate_id: Candidate ID
        job_id: Job ID
        candidate_data: Candidate data dictionary
        job_description: Job description dictionary
    
    Returns:
        Optimization result dictionary
    """
    try:
        # Check cache first
        cached_result = optimization_cache.get(candidate_id, job_id)
        if cached_result:
            logger.info(f"Cache hit for candidate {candidate_id}, job {job_id}")
            return {
                'candidate_id': candidate_id,
                'job_id': job_id,
                'status': 'success',
                'cached': True,
                **cached_result
            }
        
        # Update task state
        self.update_state(
            state='PROCESSING',
            meta={'progress': 10, 'message': 'Starting optimization...'}
        )
        
        # Initialize optimizer
        optimizer = BulkOptimizer()
        
        # Convert candidate to resume text
        resume_text = _candidate_to_resume_text(candidate_data)
        
        self.update_state(
            state='PROCESSING',
            meta={'progress': 30, 'message': 'Calling AI optimization API...'}
        )
        
        # Optimize using Groq (if available) or fallback
        if GROQ_AVAILABLE and GroqResumeOptimizer:
            groq_optimizer = GroqResumeOptimizer()
            optimized_result = groq_optimizer.optimize_resume(
                resume_text=resume_text,
                job_description=job_description.get('description', ''),
                job_title=job_description.get('title', ''),
                job_requirements=job_description.get('requirements', [])
            )
        else:
            # Fallback: use bulk optimizer
            optimized_result = optimizer.optimize_single_candidate(
                candidate_data,
                job_description
            )
        
        self.update_state(
            state='PROCESSING',
            meta={'progress': 70, 'message': 'Calculating match score...'}
        )
        
        # Calculate match score
        match_score = _calculate_match_score(candidate_data, job_description)
        
        # Prepare result
        result = {
            'candidate_id': candidate_id,
            'job_id': job_id,
            'status': 'success',
            'cached': False,
            'original_resume': resume_text,
            'optimized_resume': optimized_result.get('optimized_resume', resume_text),
            'match_score': match_score,
            'quality_score': optimized_result.get('quality_score', 0),
            'changes': optimized_result.get('suggestions', []),
            'created_at': datetime.now().isoformat()
        }
        
        # Cache the result
        optimization_cache.set(candidate_id, job_id, result)
        
        self.update_state(
            state='SUCCESS',
            meta={'progress': 100, 'message': 'Optimization complete'}
        )
        
        logger.info(f"Successfully optimized candidate {candidate_id} for job {job_id}")
        return result
        
    except Exception as exc:
        logger.error(f"Error optimizing candidate {candidate_id}: {str(exc)}", exc_info=True)
        
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery_app.task(bind=True)
def optimize_bulk_candidates_task(
    self,
    candidate_ids: List[int],
    job_id: int,
    candidates_data: List[Dict],
    job_description: Dict
) -> Dict:
    """
    Optimize multiple candidates in bulk.
    
    Args:
        candidate_ids: List of candidate IDs
        job_id: Job ID
        candidates_data: List of candidate data dictionaries
        job_description: Job description dictionary
    
    Returns:
        Bulk optimization results
    """
    try:
        total = len(candidate_ids)
        results = []
        cached_count = 0
        processed_count = 0
        failed_count = 0
        
        # Update progress
        self.update_state(
            state='PROCESSING',
            meta={
                'progress': 0,
                'total': total,
                'processed': 0,
                'cached': 0,
                'failed': 0,
                'message': f'Processing {total} candidates...'
            }
        )
        
        # Process each candidate
        for idx, (candidate_id, candidate_data) in enumerate(zip(candidate_ids, candidates_data)):
            try:
                # Check cache
                cached_result = optimization_cache.get(candidate_id, job_id)
                if cached_result:
                    cached_count += 1
                    results.append({
                        'candidate_id': candidate_id,
                        'status': 'success',
                        'cached': True,
                        **cached_result
                    })
                else:
                    # Process async
                    task = optimize_single_candidate_task.delay(
                        candidate_id,
                        job_id,
                        candidate_data,
                        job_description
                    )
                    # Wait for result (or use async callback in production)
                    result = task.get(timeout=300)
                    results.append(result)
                    processed_count += 1
                
                # Update progress
                progress = int((idx + 1) / total * 100)
                self.update_state(
                    state='PROCESSING',
                    meta={
                        'progress': progress,
                        'total': total,
                        'processed': processed_count,
                        'cached': cached_count,
                        'failed': failed_count,
                        'message': f'Processed {idx + 1}/{total} candidates'
                    }
                )
                
            except Exception as e:
                logger.error(f"Error processing candidate {candidate_id}: {str(e)}")
                failed_count += 1
                results.append({
                    'candidate_id': candidate_id,
                    'status': 'error',
                    'error': str(e)
                })
        
        return {
            'job_id': job_id,
            'total': total,
            'successful': len([r for r in results if r.get('status') == 'success']),
            'failed': failed_count,
            'cached': cached_count,
            'processed': processed_count,
            'results': results
        }
        
    except Exception as exc:
        logger.error(f"Error in bulk optimization: {str(exc)}", exc_info=True)
        raise


@celery_app.task
def cleanup_old_results():
    """Periodic task to cleanup old optimization results."""
    try:
        # This would clean up old results from database
        # Implementation depends on your database structure
        logger.info("Cleaning up old optimization results...")
        return {'status': 'success', 'message': 'Cleanup completed'}
    except Exception as e:
        logger.error(f"Error in cleanup: {str(e)}")
        return {'status': 'error', 'error': str(e)}


def _candidate_to_resume_text(candidate: Dict) -> str:
    """Convert candidate data to resume text format."""
    lines = []
    lines.append(f"{candidate.get('name', '')}")
    lines.append(f"Email: {candidate.get('email', '')}")
    lines.append(f"Phone: {candidate.get('phone', '')}")
    lines.append("")
    
    # Experience
    lines.append("EXPERIENCE")
    for exp in candidate.get('experience', []):
        lines.append(f"{exp.get('title', '')} at {exp.get('company', '')} ({exp.get('years', 0)} years)")
        lines.append(exp.get('description', ''))
        lines.append("")
    
    # Skills
    lines.append("SKILLS")
    lines.append(", ".join(candidate.get('skills', [])))
    lines.append("")
    
    # Education
    edu = candidate.get('education', {})
    if edu:
        lines.append("EDUCATION")
        lines.append(f"{edu.get('degree', '')} - {edu.get('university', '')} ({edu.get('year', '')})")
    
    return "\n".join(lines)


def _calculate_match_score(candidate: Dict, job: Dict) -> float:
    """Calculate match score between candidate and job."""
    # Simple scoring algorithm
    score = 0.0
    max_score = 100.0
    
    # Skills match (40 points)
    candidate_skills = set(s.lower() for s in candidate.get('skills', []))
    job_requirements = job.get('requirements', [])
    job_skills = set()
    
    for req in job_requirements:
        if isinstance(req, str):
            job_skills.add(req.lower())
        elif isinstance(req, dict):
            job_skills.add(req.get('skill', '').lower())
    
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
        score += 15  # Default if no requirement
    
    # Title match (30 points)
    job_title = job.get('title', '').lower()
    for exp in candidate.get('experience', []):
        exp_title = exp.get('title', '').lower()
        if job_title in exp_title or exp_title in job_title:
            score += 30
            break
    
    return round(min(score, max_score), 1)

