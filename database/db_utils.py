"""
Database utility functions for CRUD operations.
"""

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .models import (
    get_session, Resume, JobDescription, Optimization, OptimizationHistory
)


class ResumeDB:
    """Database operations for resumes."""
    
    @staticmethod
    def create(name, filename, content, file_type=None, word_count=None):
        """Create a new resume record."""
        session = get_session()
        try:
            resume = Resume(
                name=name,
                filename=filename,
                content=content,
                file_type=file_type,
                word_count=word_count
            )
            session.add(resume)
            session.commit()
            session.refresh(resume)
            return resume
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_all():
        """Get all resumes."""
        session = get_session()
        try:
            return session.query(Resume).order_by(Resume.created_at.desc()).all()
        finally:
            session.close()
    
    @staticmethod
    def get_by_id(resume_id):
        """Get resume by ID."""
        session = get_session()
        try:
            return session.query(Resume).filter_by(id=resume_id).first()
        finally:
            session.close()
    
    @staticmethod
    def update(resume_id, **kwargs):
        """Update resume."""
        session = get_session()
        try:
            resume = session.query(Resume).filter_by(id=resume_id).first()
            if resume:
                for key, value in kwargs.items():
                    setattr(resume, key, value)
                resume.updated_at = datetime.utcnow()
                session.commit()
                return resume
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def delete(resume_id):
        """Delete resume."""
        session = get_session()
        try:
            resume = session.query(Resume).filter_by(id=resume_id).first()
            if resume:
                session.delete(resume)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()


class JobDescriptionDB:
    """Database operations for job descriptions."""
    
    @staticmethod
    def create(title, content, company=None, source_url=None):
        """Create a new job description record."""
        session = get_session()
        try:
            job = JobDescription(
                title=title,
                company=company,
                content=content,
                source_url=source_url
            )
            session.add(job)
            session.commit()
            session.refresh(job)
            return job
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_all():
        """Get all job descriptions."""
        session = get_session()
        try:
            return session.query(JobDescription).order_by(JobDescription.created_at.desc()).all()
        finally:
            session.close()
    
    @staticmethod
    def get_by_id(job_id):
        """Get job description by ID."""
        session = get_session()
        try:
            return session.query(JobDescription).filter_by(id=job_id).first()
        finally:
            session.close()
    
    @staticmethod
    def update(job_id, **kwargs):
        """Update job description."""
        session = get_session()
        try:
            job = session.query(JobDescription).filter_by(id=job_id).first()
            if job:
                for key, value in kwargs.items():
                    setattr(job, key, value)
                job.updated_at = datetime.utcnow()
                session.commit()
                return job
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def delete(job_id):
        """Delete job description."""
        session = get_session()
        try:
            job = session.query(JobDescription).filter_by(id=job_id).first()
            if job:
                session.delete(job)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()


class OptimizationDB:
    """Database operations for optimizations."""
    
    @staticmethod
    def create(
        resume_id,
        job_description_id,
        optimized_resume=None,
        original_resume=None,
        quality_score=None,
        match_score=None,
        analysis_data=None,
        suggestions=None,
        matching_keywords=None,
        missing_keywords=None,
        optimization_type='complete',
        model_used=None,
        api_provider='groq'
    ):
        """Create a new optimization record."""
        session = get_session()
        try:
            optimization = Optimization(
                resume_id=resume_id,
                job_description_id=job_description_id,
                optimized_resume=optimized_resume,
                original_resume=original_resume,
                quality_score=quality_score,
                match_score=match_score,
                analysis_data=analysis_data,
                suggestions=suggestions,
                matching_keywords=matching_keywords,
                missing_keywords=missing_keywords,
                optimization_type=optimization_type,
                model_used=model_used,
                api_provider=api_provider
            )
            session.add(optimization)
            session.commit()
            session.refresh(optimization)
            
            # Create history entry
            OptimizationDB.add_history(optimization.id, 'created')
            
            return optimization
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_all():
        """Get all optimizations."""
        session = get_session()
        try:
            return session.query(Optimization).order_by(Optimization.created_at.desc()).all()
        finally:
            session.close()
    
    @staticmethod
    def get_by_id(optimization_id):
        """Get optimization by ID."""
        session = get_session()
        try:
            return session.query(Optimization).filter_by(id=optimization_id).first()
        finally:
            session.close()
    
    @staticmethod
    def get_by_resume_and_job(resume_id, job_id):
        """Get optimization by resume and job."""
        session = get_session()
        try:
            return session.query(Optimization).filter_by(
                resume_id=resume_id,
                job_description_id=job_id
            ).order_by(Optimization.created_at.desc()).first()
        finally:
            session.close()
    
    @staticmethod
    def get_by_resume(resume_id):
        """Get all optimizations for a resume."""
        session = get_session()
        try:
            return session.query(Optimization).filter_by(
                resume_id=resume_id
            ).order_by(Optimization.created_at.desc()).all()
        finally:
            session.close()
    
    @staticmethod
    def update(optimization_id, **kwargs):
        """Update optimization."""
        session = get_session()
        try:
            optimization = session.query(Optimization).filter_by(id=optimization_id).first()
            if optimization:
                for key, value in kwargs.items():
                    setattr(optimization, key, value)
                session.commit()
                OptimizationDB.add_history(optimization_id, 'updated')
                return optimization
            return None
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def delete(optimization_id):
        """Delete optimization."""
        session = get_session()
        try:
            optimization = session.query(Optimization).filter_by(id=optimization_id).first()
            if optimization:
                session.delete(optimization)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add_history(optimization_id, action, notes=None):
        """Add history entry."""
        session = get_session()
        try:
            history = OptimizationHistory(
                optimization_id=optimization_id,
                action=action,
                notes=notes
            )
            session.add(history)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
        finally:
            session.close()

