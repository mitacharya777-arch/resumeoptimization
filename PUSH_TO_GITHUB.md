# How to Push Your Code to GitHub

## ✅ Status
- ✅ Git repository initialized
- ✅ Remote configured: https://github.com/mitacharya777-arch/resumeoptimization.git
- ✅ All files committed (123 files)
- ✅ .env file is properly ignored (safe!)

## 🔐 Authentication Required

GitHub requires authentication to push code. Choose one method:

---

## Option 1: Personal Access Token (Easiest)

### Step 1: Create a Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Note:** Give it a name like "resume-optimizer"
4. **Expiration:** Choose your preference (90 days, 1 year, or no expiration)
5. **Select scopes:** Check **"repo"** (this gives full control of private repositories)
6. Click **"Generate token"** at the bottom
7. **⚠️ IMPORTANT:** Copy the token immediately (you won't see it again!)

### Step 2: Push Your Code
```bash
cd /Users/mitacharya/Desktop/resumeoptimization
git push -u origin main
```

When prompted:
- **Username:** `mitacharya777-arch`
- **Password:** Paste your personal access token (NOT your GitHub password)

---

## Option 2: SSH Key (More Secure for Future)

### Step 1: Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
- Press Enter to accept default file location
- Enter a passphrase (optional but recommended)

### Step 2: Add SSH Key to GitHub
1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to: https://github.com/settings/keys
3. Click **"New SSH key"**
4. **Title:** "My Laptop" (or any name)
5. **Key:** Paste the public key content
6. Click **"Add SSH key"**

### Step 3: Change Remote to SSH
```bash
cd /Users/mitacharya/Desktop/resumeoptimization
git remote set-url origin git@github.com:mitacharya777-arch/resumeoptimization.git
```

### Step 4: Push Your Code
```bash
git push -u origin main
```

---

## Option 3: GitHub CLI (Alternative)

If you have GitHub CLI installed:
```bash
gh auth login
git push -u origin main
```

---

## Verify Upload

After pushing, visit:
**https://github.com/mitacharya777-arch/resumeoptimization**

You should see all your files there!

---

## Future Updates

After making changes to your code:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Description of your changes"

# Push
git push
```

---

## Troubleshooting

### "Permission denied" error
- Make sure you're using the correct username
- For Personal Access Token: Use the token, not your password
- For SSH: Make sure your SSH key is added to GitHub

### "Repository not found" error
- Check the repository URL is correct
- Make sure you have access to the repository

### "Authentication failed" error
- Regenerate your Personal Access Token
- Or set up SSH keys

---

## Security Reminder

✅ **Good:** Your `.env` file is in `.gitignore` - it won't be uploaded
✅ **Good:** API keys are safe in local `.env` file
⚠️ **Never:** Commit `.env` files or hardcode API keys in your code

