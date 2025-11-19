# Quick Start with SQLite (Easiest Option!)

SQLite is perfect for local development - **no database server setup required!**

## Why SQLite?

✅ **Zero configuration** - No PostgreSQL installation needed  
✅ **No server** - Just a file on your computer  
✅ **Perfect for local use** - Ideal for development and testing  
✅ **Easy backup** - Just copy the .db file  
✅ **Fast setup** - Get started in seconds  

## Setup (Super Easy!)

### Step 1: Set Environment Variable

```bash
export DB_TYPE=sqlite
```

Or create a `.env` file:
```
DB_TYPE=sqlite
```

### Step 2: Run the App!

```bash
python3 app_db.py
```

That's it! The database file (`resume_optimizer.db`) will be created automatically.

## What Happens?

- A file called `resume_optimizer.db` will be created in your project directory
- All your data is stored in this single file
- No PostgreSQL needed!
- Everything else works exactly the same

## Custom Database Location

If you want to store the database file somewhere else:

```bash
export DB_TYPE=sqlite
export DB_PATH=/path/to/your/database.db
```

## Switching Between SQLite and PostgreSQL

**Use SQLite (local development):**
```bash
export DB_TYPE=sqlite
python3 app_db.py
```

**Use PostgreSQL (production):**
```bash
export DB_TYPE=postgresql
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_NAME=resume_optimizer
python3 app_db.py
```

## Advantages of SQLite for This Project

1. **No Installation** - Works out of the box
2. **Perfect for Single User** - Ideal for personal use
3. **Easy Testing** - Quick to reset (just delete the .db file)
4. **Portable** - Copy the .db file to backup or move
5. **Fast** - Excellent performance for local use

## When to Use PostgreSQL Instead?

- Multiple users accessing simultaneously
- Production deployment
- Need advanced features (full-text search, etc.)
- Very large datasets (millions of records)

## Migration

You can easily migrate from SQLite to PostgreSQL later:
1. Export data from SQLite
2. Import into PostgreSQL
3. Change DB_TYPE environment variable

## Troubleshooting

**Database file not created?**
- Check file permissions in the directory
- Make sure you have write access

**Want to reset?**
- Just delete `resume_optimizer.db` file
- Run the app again - it will create a fresh database

**Need to backup?**
- Just copy the `resume_optimizer.db` file!

---

**TL;DR:** Set `DB_TYPE=sqlite` and run the app. That's it! 🚀

