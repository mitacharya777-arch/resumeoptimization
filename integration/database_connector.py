"""
Database Connector - Connect to YOUR existing candidate database
This reads from your database, not creating a new one.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional
import os


class DatabaseConnector:
    """
    Connects to your existing database to read candidate data.
    No file parsing - uses structured data from your database.
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database connection.
        
        Args:
            connection_string: Database connection string
                Format: postgresql://user:password@host:port/database
                Or set via environment variables
        """
        if connection_string:
            self.connection_string = connection_string
        else:
            # Get from environment variables
            self.connection_string = self._get_connection_string()
        
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def _get_connection_string(self) -> str:
        """Get connection string from environment variables."""
        db_type = os.getenv('EXTERNAL_DB_TYPE', 'postgresql')
        db_user = os.getenv('EXTERNAL_DB_USER', '')
        db_password = os.getenv('EXTERNAL_DB_PASSWORD', '')
        db_host = os.getenv('EXTERNAL_DB_HOST', 'localhost')
        db_port = os.getenv('EXTERNAL_DB_PORT', '5432')
        db_name = os.getenv('EXTERNAL_DB_NAME', '')
        
        return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def get_candidates(self, filters: Optional[Dict] = None, limit: int = 400) -> List[Dict]:
        """
        Get candidates from your database.
        
        Args:
            filters: Optional filters (e.g., {'status': 'active', 'skills': ['Python']})
            limit: Maximum number of candidates to return
        
        Returns:
            List of candidate dictionaries
        """
        session = self.Session()
        try:
            # TODO: Replace with your actual table name and query
            # This is a template - needs your actual schema
            query = text("""
                SELECT 
                    id,
                    name,
                    email,
                    experience,
                    skills,
                    education,
                    resume_text
                FROM candidates
                WHERE 1=1
                LIMIT :limit
            """)
            
            result = session.execute(query, {'limit': limit})
            candidates = []
            
            for row in result:
                candidates.append({
                    'id': row.id,
                    'name': row.name,
                    'email': row.email,
                    'experience': row.experience,
                    'skills': row.skills,
                    'education': row.education,
                    'resume_text': row.resume_text
                })
            
            return candidates
        
        except Exception as e:
            print(f"Error fetching candidates: {e}")
            return []
        finally:
            session.close()
    
    def get_candidate_by_id(self, candidate_id: int) -> Optional[Dict]:
        """Get a single candidate by ID."""
        session = self.Session()
        try:
            query = text("""
                SELECT 
                    id, name, email, experience, skills, education, resume_text
                FROM candidates
                WHERE id = :candidate_id
            """)
            
            result = session.execute(query, {'candidate_id': candidate_id})
            row = result.fetchone()
            
            if row:
                return {
                    'id': row.id,
                    'name': row.name,
                    'email': row.email,
                    'experience': row.experience,
                    'skills': row.skills,
                    'education': row.education,
                    'resume_text': row.resume_text
                }
            return None
        
        except Exception as e:
            print(f"Error fetching candidate: {e}")
            return None
        finally:
            session.close()
    
    def get_job_posting(self, job_id: int) -> Optional[Dict]:
        """Get job posting from your database."""
        session = self.Session()
        try:
            # TODO: Replace with your actual job postings table
            query = text("""
                SELECT 
                    id, title, company, description, requirements
                FROM job_postings
                WHERE id = :job_id
            """)
            
            result = session.execute(query, {'job_id': job_id})
            row = result.fetchone()
            
            if row:
                return {
                    'id': row.id,
                    'title': row.title,
                    'company': row.company,
                    'description': row.description,
                    'requirements': row.requirements
                }
            return None
        
        except Exception as e:
            print(f"Error fetching job posting: {e}")
            return None
        finally:
            session.close()
    
    def update_candidate_optimized_data(self, candidate_id: int, optimized_data: Dict):
        """
        Update candidate with optimized resume data.
        Called after recruiter approves optimization.
        """
        session = self.Session()
        try:
            # TODO: Replace with your actual update query
            query = text("""
                UPDATE candidates
                SET optimized_resume = :optimized_data,
                    optimization_date = NOW()
                WHERE id = :candidate_id
            """)
            
            session.execute(query, {
                'candidate_id': candidate_id,
                'optimized_data': str(optimized_data)
            })
            session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Error updating candidate: {e}")
        finally:
            session.close()

