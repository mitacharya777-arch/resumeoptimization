# Git Setup Guide - Upload Your Code to GitHub

## Step 1: Create a .gitignore File ✅
A `.gitignore` file has been created to exclude sensitive files like:
- `.env` files (contains API keys!)
- `__pycache__/` (Python cache)
- Virtual environments
- Temporary files
- Logs

**⚠️ IMPORTANT: Never commit `.env` files with API keys!**

## Step 2: Initialize Git Repository (if not already done)

```bash
cd /Users/mitacharya/Desktop/resumeoptimization
git init
```

## Step 3: Add All Files

```bash
# Check what will be added (optional)
git status

# Add all files
git add .

# Verify what's staged
git status
```

## Step 4: Make Your First Commit

```bash
git commit -m "Initial commit: Resume optimization application with AI integration"
```

## Step 5: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `resume-optimizer` (or your preferred name)
4. Description: "AI-powered resume optimization tool with multi-provider support"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

## Step 6: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/resume-optimizer.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/resume-optimizer.git

# Verify remote was added
git remote -v
```

## Step 7: Push Your Code

```bash
# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

## Step 8: Verify Upload

1. Go to your GitHub repository page
2. You should see all your files there
3. **Double-check that `.env` file is NOT visible** (it should be ignored)

## Future Updates

After making changes:

```bash
# Check what changed
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Security Checklist Before Pushing

- ✅ `.env` file is in `.gitignore`
- ✅ No API keys in code files
- ✅ No passwords or secrets committed
- ✅ `__pycache__/` is ignored
- ✅ Virtual environment is ignored

## Common Commands

```bash
# Check status
git status

# See what files changed
git diff

# View commit history
git log

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull
```

## Troubleshooting

### If you accidentally committed .env file:
```bash
# Remove from git (but keep local file)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env file from repository"

# Push
git push
```

### If you need to update .gitignore:
```bash
# Remove cached files
git rm -r --cached .

# Re-add everything
git add .

# Commit
git commit -m "Update .gitignore"
```

## Next Steps

1. Create a README.md with project description
2. Add license file (if needed)
3. Set up GitHub Actions for CI/CD (optional)
4. Add collaborators (if working in a team)

