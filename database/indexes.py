"""
Database Indexes - Performance Optimization
Creates indexes for fast queries at scale.
"""

from sqlalchemy import text, Index
from database.models import Base, Optimization, Resume, JobDescription
from database.models import create_engine_instance, get_session
import logging

logger = logging.getLogger(__name__)


def create_indexes():
    """Create database indexes for performance."""
    try:
        engine = create_engine_instance()
        
        with engine.connect() as conn:
            # Indexes for candidates/resumes
            logger.info("Creating indexes for resumes...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_resumes_created_at 
                ON resumes(created_at DESC);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_resumes_status 
                ON resumes(status);
            """))
            
            # Indexes for job descriptions
            logger.info("Creating indexes for job descriptions...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_jobs_created_at 
                ON job_descriptions(created_at DESC);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_jobs_title 
                ON job_descriptions(title);
            """))
            
            # Indexes for optimizations (most important for performance)
            logger.info("Creating indexes for optimizations...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_optimizations_job_id 
                ON optimizations(job_id);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_optimizations_resume_id 
                ON optimizations(resume_id);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_optimizations_status 
                ON optimizations(status);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_optimizations_created_at 
                ON optimizations(created_at DESC);
            """))
            
            # Composite indexes for common queries
            logger.info("Creating composite indexes...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_opt_job_status 
                ON optimizations(job_id, status);
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_opt_resume_job 
                ON optimizations(resume_id, job_id);
            """))
            
            # Index for match score (for sorting)
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_optimizations_match_score 
                ON optimizations(match_score DESC);
            """))
            
            conn.commit()
        
        logger.info("✅ All indexes created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        return False


def drop_indexes():
    """Drop all indexes (for testing/reset)."""
    try:
        engine = create_engine_instance()
        
        with engine.connect() as conn:
            indexes = [
                'idx_resumes_created_at',
                'idx_resumes_status',
                'idx_jobs_created_at',
                'idx_jobs_title',
                'idx_optimizations_job_id',
                'idx_optimizations_resume_id',
                'idx_optimizations_status',
                'idx_optimizations_created_at',
                'idx_opt_job_status',
                'idx_opt_resume_job',
                'idx_optimizations_match_score'
            ]
            
            for index_name in indexes:
                try:
                    conn.execute(text(f"DROP INDEX IF EXISTS {index_name};"))
                except Exception as e:
                    logger.warning(f"Could not drop index {index_name}: {e}")
            
            conn.commit()
        
        logger.info("✅ All indexes dropped")
        return True
        
    except Exception as e:
        logger.error(f"Error dropping indexes: {e}")
        return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        drop_indexes()
    else:
        create_indexes()

