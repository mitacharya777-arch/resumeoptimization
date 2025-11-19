"""
Database Models for Resume Optimizer
PostgreSQL database schema for storing resumes, job descriptions, and optimizations.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()


class Resume(Base):
    """Resume model - stores original resumes."""
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    file_type = Column(String(10))  # pdf, docx, txt
    word_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    optimizations = relationship("Optimization", back_populates="resume", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Resume(id={self.id}, name='{self.name}')>"


class JobDescription(Base):
    """Job description model - stores job postings."""
    __tablename__ = 'job_descriptions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    content = Column(Text, nullable=False)
    source_url = Column(String(500))  # Optional: where the job was found
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    optimizations = relationship("Optimization", back_populates="job_description", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobDescription(id={self.id}, title='{self.title}', company='{self.company}')>"


class Optimization(Base):
    """Optimization model - stores optimization results."""
    __tablename__ = 'optimizations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    job_description_id = Column(Integer, ForeignKey('job_descriptions.id'), nullable=False)
    
    # Scores
    quality_score = Column(Float)
    match_score = Column(Float)
    
    # Content
    optimized_resume = Column(Text)  # The optimized resume content
    original_resume = Column(Text)  # Original resume content (for comparison)
    
    # Analysis data (stored as JSON)
    analysis_data = Column(JSON)  # Stores detailed analysis results
    suggestions = Column(JSON)  # Stores suggestions as list
    matching_keywords = Column(JSON)  # Stores matching keywords
    missing_keywords = Column(JSON)  # Stores missing keywords
    
    # Metadata
    optimization_type = Column(String(50))  # complete, keywords, overall, section
    model_used = Column(String(100))  # e.g., "llama-3.1-70b-versatile"
    api_provider = Column(String(50))  # groq, openai, basic
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="optimizations")
    job_description = relationship("JobDescription", back_populates="optimizations")
    
    def __repr__(self):
        return f"<Optimization(id={self.id}, resume_id={self.resume_id}, job_id={self.job_description_id}, match_score={self.match_score})>"


class OptimizationHistory(Base):
    """History of optimization attempts - for tracking and analytics."""
    __tablename__ = 'optimization_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    optimization_id = Column(Integer, ForeignKey('optimizations.id'))
    action = Column(String(50))  # created, updated, viewed, downloaded
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<OptimizationHistory(id={self.id}, action='{self.action}')>"


def get_database_url():
    """Get database URL from environment or use default.
    
    Supports both PostgreSQL and SQLite.
    Set DB_TYPE='sqlite' to use SQLite (easier for local development).
    """
    db_type = os.getenv('DB_TYPE', 'postgresql').lower()
    
    if db_type == 'sqlite':
        # SQLite - no setup required, perfect for local development
        db_path = os.getenv('DB_PATH', 'resume_optimizer.db')
        # Ensure directory exists
        db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else '.'
        os.makedirs(db_dir, exist_ok=True)
        return f"sqlite:///{db_path}"
    else:
        # PostgreSQL - for production
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'resume_optimizer')
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_engine_instance():
    """Create SQLAlchemy engine."""
    database_url = get_database_url()
    
    # SQLite-specific configuration
    if database_url.startswith('sqlite'):
        # Enable foreign keys for SQLite
        return create_engine(
            database_url, 
            echo=False,
            connect_args={'check_same_thread': False}  # Needed for SQLite with Flask
        )
    else:
        # PostgreSQL configuration
        return create_engine(database_url, echo=False)


def create_tables():
    """Create all database tables."""
    engine = create_engine_instance()
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")


def get_session():
    """Get database session."""
    engine = create_engine_instance()
    Session = sessionmaker(bind=engine)
    return Session()

