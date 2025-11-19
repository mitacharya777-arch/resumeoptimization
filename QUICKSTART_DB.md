# Quick Start: Database Edition

Get your Resume Optimizer with PostgreSQL database running in 5 minutes!

## Step 1: Install PostgreSQL (2 minutes)

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

## Step 2: Create Database (1 minute)

```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE resume_optimizer;

# Exit
\q
```

## Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment (1 minute)

Create `.env` file or set environment variables:

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=resume_optimizer

# Optional: Groq API key
export GROQ_API_KEY=your_groq_api_key
```

## Step 5: Initialize Database

```bash
python setup_database.py
```

You should see:
```
✅ Database connection successful!
✅ Database setup complete!
```

## Step 6: Run Application

```bash
python app_db.py
```

Open http://localhost:5000 in your browser!

## Using the Application

### 1. Upload Resumes
- Go to "Resumes" tab
- Click "+ Upload Resume"
- Select your resume file (PDF, DOCX, or TXT)
- Give it a name and upload

### 2. Add Job Descriptions
- Go to "Job Descriptions" tab
- Click "+ Add Job Description"
- Fill in job title, company, and description
- Save

### 3. Optimize Resume
- Go to "Optimize" tab
- Select a resume from dropdown
- Select a job description
- Choose optimization type
- Click "Optimize"
- View results and download optimized resume

### 4. View History
- Go to "History" tab
- See all past optimizations
- Click "View" to see details

### 5. Dashboard
- View statistics and analytics
- See recent optimizations
- Monitor your progress

## Troubleshooting

**Database connection error?**
- Make sure PostgreSQL is running: `brew services list` or `sudo systemctl status postgresql`
- Check database exists: `psql -l | grep resume_optimizer`
- Verify credentials in environment variables

**Tables not created?**
- Run `python setup_database.py` again
- Check database user has CREATE TABLE permissions

**Port 5000 already in use?**
- Change port in `app_db.py`: `app.run(port=5001)`

## Next Steps

- Read `DATABASE_SETUP.md` for detailed setup
- Check `README.md` for full documentation
- Explore all features in the web interface

Happy optimizing! 🚀

