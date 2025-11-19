"""
Easy Setup Script for Beginners
Run this to set up everything automatically!
"""

import os
import sys
import subprocess

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {description}")
    print('='*60)

def check_python():
    """Check if Python is installed."""
    print_step(1, "Checking Python Installation")
    try:
        result = subprocess.run(['python3', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
            return 'python3'
    except:
        pass
    
    try:
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
            return 'python'
    except:
        pass
    
    print("❌ Python not found!")
    print("   Please install Python from https://www.python.org/")
    return None

def install_dependencies(python_cmd):
    """Install required packages."""
    print_step(2, "Installing Dependencies")
    print("This may take a minute...")
    
    try:
        subprocess.run([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may have failed to install.")
        print("   Try running manually: pip install -r requirements.txt")
        return False

def setup_sqlite():
    """Set up SQLite database."""
    print_step(3, "Setting Up SQLite Database")
    
    # Set environment variable for current session
    os.environ['DB_TYPE'] = 'sqlite'
    
    try:
        from database import create_tables
        create_tables()
        print("✅ SQLite database set up successfully!")
        print("   Database file: resume_optimizer.db")
        return True
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("   The app will still work, but you may need to set DB_TYPE=sqlite")
        return False

def create_env_file():
    """Create .env file with SQLite configuration."""
    print_step(4, "Creating Configuration File")
    
    env_content = """# Database Configuration
# Using SQLite for easy setup (no installation needed!)
DB_TYPE=sqlite

# Optional: Change database file location
# DB_PATH=resume_optimizer.db

# Optional: For Groq AI features
# GROQ_API_KEY=your_groq_api_key_here
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Configuration file (.env) created!")
        return True
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")
        return False

def print_next_steps():
    """Print instructions for next steps."""
    print_step(5, "Setup Complete!")
    print("\n🎉 Everything is set up! Here's what to do next:\n")
    print("1. Set the database type (if not using .env file):")
    print("   export DB_TYPE=sqlite")
    print("\n2. Run the application:")
    print("   python3 app_db.py")
    print("   (or: python app_db.py)")
    print("\n3. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n" + "="*60)
    print("💡 Tip: The database file 'resume_optimizer.db' will be")
    print("   created automatically when you run the app!")
    print("="*60 + "\n")

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("🚀 Resume Optimizer - Easy Setup for Beginners")
    print("="*60)
    print("\nThis script will help you set up everything automatically!")
    print("Just follow the steps below.\n")
    
    # Check Python
    python_cmd = check_python()
    if not python_cmd:
        sys.exit(1)
    
    # Install dependencies
    install_dependencies(python_cmd)
    
    # Create .env file
    create_env_file()
    
    # Setup SQLite
    setup_sqlite()
    
    # Print next steps
    print_next_steps()
    
    print("✅ Setup complete! You're ready to go! 🎉\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("\nDon't worry! You can still set up manually:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set DB_TYPE=sqlite")
        print("3. Run: python app_db.py")
        sys.exit(1)

