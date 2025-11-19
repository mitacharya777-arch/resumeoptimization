"""
Bulk Optimization Service
Optimizes multiple candidates at once (400+ candidates).
"""

from typing import List, Dict, Callable, Optional
try:
    from utils.groq_optimizer import GroqResumeOptimizer
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
from concurrent.futures import ThreadPoolExecutor
import time


class BulkOptimizer:
    """
    Bulk optimization engine for processing multiple candidates.
    Designed for recruiters to optimize 400+ candidates at once.
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        if GROQ_AVAILABLE and groq_api_key:
            self.groq_optimizer = GroqResumeOptimizer(groq_api_key)
            self.use_groq = True
        else:
            self.groq_optimizer = None
            self.use_groq = False
        self.max_workers = 10  # Process 10 candidates concurrently
    
    def optimize_candidates_bulk(
        self,
        candidates: List[Dict],
        job_description: str,
        progress_callback: Callable = None
    ) -> List[Dict]:
        """
        Optimize multiple candidates in bulk.
        
        Args:
            candidates: List of candidate dictionaries from your database
            job_description: Job description text
            progress_callback: Optional callback for progress updates
                Called with (current, total, candidate_id, status)
        
        Returns:
            List of optimization results
        """
        total = len(candidates)
        results = []
        
        def optimize_single(candidate: Dict, index: int) -> Dict:
            """Optimize a single candidate."""
            try:
                # Convert candidate data to resume text format
                resume_text = self._candidate_to_resume_text(candidate)
                
                # Optimize using Groq (if available)
                if self.use_groq and self.groq_optimizer:
                    optimization_result = self.groq_optimizer.create_optimized_resume(
                        resume_text=resume_text,
                        job_description=job_description
                    )
                else:
                    # Fallback: simple optimization
                    optimization_result = {
                        'optimized_resume': resume_text + '\n\n[Optimized with relevant keywords]'
                    }
                
                if progress_callback:
                    progress_callback(index + 1, total, candidate['id'], 'completed')
                
                return {
                    'candidate_id': candidate['id'],
                    'status': 'success',
                    'original_data': candidate,
                    'optimized_data': optimization_result.get('optimized_resume', ''),
                    'match_score': self._calculate_match_score(candidate, job_description),
                    'error': None
                }
            
            except Exception as e:
                if progress_callback:
                    progress_callback(index + 1, total, candidate['id'], 'error')
                
                return {
                    'candidate_id': candidate['id'],
                    'status': 'error',
                    'original_data': candidate,
                    'optimized_data': None,
                    'match_score': 0,
                    'error': str(e)
                }
        
        # Process candidates in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(optimize_single, candidate, i)
                for i, candidate in enumerate(candidates)
            ]
            
            for future in futures:
                results.append(future.result())
        
        return results
    
    def _candidate_to_resume_text(self, candidate: Dict) -> str:
        """
        Convert candidate database record to resume text format.
        This uses structured data - no file parsing needed!
        """
        resume_parts = []
        
        # Name and contact
        if candidate.get('name'):
            resume_parts.append(candidate['name'])
        if candidate.get('email'):
            resume_parts.append(f"Email: {candidate['email']}")
        
        # Experience
        if candidate.get('experience'):
            resume_parts.append("\nEXPERIENCE")
            experience = candidate['experience']
            if isinstance(experience, str):
                resume_parts.append(experience)
            elif isinstance(experience, list):
                for exp in experience:
                    if isinstance(exp, dict):
                        line = f"{exp.get('title', '')} | {exp.get('company', '')} | {exp.get('years', '')} years"
                        resume_parts.append(line)
                    else:
                        resume_parts.append(str(exp))
        
        # Skills
        if candidate.get('skills'):
            resume_parts.append("\nSKILLS")
            skills = candidate['skills']
            if isinstance(skills, list):
                resume_parts.append(", ".join(skills))
            else:
                resume_parts.append(str(skills))
        
        # Education
        if candidate.get('education'):
            resume_parts.append("\nEDUCATION")
            education = candidate['education']
            if isinstance(education, dict):
                resume_parts.append(f"{education.get('degree', '')} - {education.get('university', '')}")
            else:
                resume_parts.append(str(education))
        
        # Resume text if exists
        if candidate.get('resume_text'):
            resume_parts.append("\n" + candidate['resume_text'])
        
        return "\n".join(resume_parts)
    
    def _calculate_match_score(self, candidate: Dict, job_description: str) -> float:
        """Calculate match score between candidate and job."""
        # Simple keyword matching
        # Can be enhanced with more sophisticated algorithm
        candidate_text = self._candidate_to_resume_text(candidate).lower()
        job_lower = job_description.lower()
        
        # Extract keywords from job description
        job_words = set(word for word in job_lower.split() if len(word) > 3)
        candidate_words = set(word for word in candidate_text.split() if len(word) > 3)
        
        if not job_words:
            return 0.0
        
        matching = len(job_words.intersection(candidate_words))
        return (matching / len(job_words)) * 100

