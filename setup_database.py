"""
Database Setup Script
Run this to initialize the database and create tables.
"""

import os
import sys
from database import create_tables, get_session

def setup_database():
    """Initialize database tables."""
    print("🔧 Setting up database...")
    
    # Check environment variables
    db_user = os.getenv('DB_USER', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'resume_optimizer')
    
    print(f"   Database: {db_name}")
    print(f"   Host: {db_host}")
    print(f"   User: {db_user}")
    
    try:
        # Test connection
        session = get_session()
        session.close()
        print("✅ Database connection successful!")
        
        # Create tables
        print("📊 Creating tables...")
        create_tables()
        print("✅ Database setup complete!")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. PostgreSQL is running")
        print("   2. Database exists (CREATE DATABASE resume_optimizer;)")
        print("   3. Environment variables are set correctly")
        print("   4. User has proper permissions")
        return False


if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)

