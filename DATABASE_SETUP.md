# Database Setup Guide

## PostgreSQL Setup

### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

### 2. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE resume_optimizer;

# Create user (optional)
CREATE USER resume_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_optimizer TO resume_user;

# Exit
\q
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=resume_optimizer

# Groq API (optional)
GROQ_API_KEY=your_groq_api_key
```

Or set environment variables:

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=resume_optimizer
```

### 4. Initialize Database Tables

The tables will be created automatically when you run the app, or you can create them manually:

```python
from database import create_tables
create_tables()
```

Or run:
```bash
python -c "from database import create_tables; create_tables()"
```

### 5. Verify Setup

Test the connection:

```python
from database import get_session, ResumeDB

# Test connection
try:
    resumes = ResumeDB.get_all()
    print("✅ Database connection successful!")
    print(f"Found {len(resumes)} resumes")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

## Database Schema

### Tables

1. **resumes** - Stores uploaded resumes
   - id, name, filename, content, file_type, word_count, created_at, updated_at

2. **job_descriptions** - Stores job postings
   - id, title, company, content, source_url, created_at, updated_at

3. **optimizations** - Stores optimization results
   - id, resume_id, job_description_id, quality_score, match_score
   - optimized_resume, original_resume, analysis_data, suggestions
   - matching_keywords, missing_keywords, optimization_type
   - model_used, api_provider, created_at

4. **optimization_history** - Tracks optimization actions
   - id, optimization_id, action, notes, created_at

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_NAME=resume_optimizer

# Run the app
python app_db.py
```

Then open http://localhost:5000

## Troubleshooting

### Connection Refused
- Make sure PostgreSQL is running: `brew services list` or `sudo systemctl status postgresql`
- Check if port 5432 is accessible
- Verify database credentials

### Authentication Failed
- Check username and password in environment variables
- Verify user has permissions on the database

### Table Creation Failed
- Ensure database exists
- Check user has CREATE TABLE permissions
- Review error messages for specific issues

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python path includes the project directory

## Backup and Restore

### Backup
```bash
pg_dump -U postgres resume_optimizer > backup.sql
```

### Restore
```bash
psql -U postgres resume_optimizer < backup.sql
```

## Production Considerations

1. **Use connection pooling** for better performance
2. **Set up regular backups**
3. **Use environment variables** for credentials (never hardcode)
4. **Enable SSL** for database connections in production
5. **Monitor database performance**
6. **Set up proper indexes** on frequently queried columns

