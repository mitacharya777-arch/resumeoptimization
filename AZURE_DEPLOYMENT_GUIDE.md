# Azure Deployment Guide - Resume Optimizer

**Complete Step-by-Step Guide for Deploying to Azure App Service**

---

## Prerequisites

✅ Azure account (you have this)
✅ GitHub repository with latest code (you have this)
✅ Groq API key (get from https://console.groq.com/)

---

## Part 1: Push Code to GitHub (DONE ✅)

Your code is ready with these Azure-specific files:
- `startup.sh` - Tells Azure how to start the app
- `runtime.txt` - Specifies Python 3.11
- `requirements.txt` - Includes gunicorn for production
- `app_web.py` - Updated to work with Azure ports

---

## Part 2: Create Azure App Service

### Step 1: Login to Azure Portal

1. Go to [https://portal.azure.com](https://portal.azure.com)
2. Sign in with your Azure account

### Step 2: Create a New Web App

1. Click **"+ Create a resource"** (top left)
2. Search for **"Web App"** and select it
3. Click **"Create"**

### Step 3: Configure Basic Settings

Fill in these details:

**Subscription:**
- Select your subscription

**Resource Group:**
- Click "Create new"
- Name it: `resume-optimizer-rg`
- Click OK

**Instance Details:**
- **Name**: `your-company-resume-optimizer` (must be unique across Azure)
  - This will be your URL: `https://your-company-resume-optimizer.azurewebsites.net`
  - Choose any name you like (lowercase, no spaces)
- **Publish**: Select `Code`
- **Runtime stack**: Select `Python 3.11`
- **Operating System**: Select `Linux`
- **Region**: Choose closest to you (e.g., `East US`, `West Europe`)

**Pricing Plans:**
- Click "Explore pricing plans"
- **For Testing**: Select `Free F1` (0 cost, good for 5-10 users)
- **For Production**: Select `Basic B1` ($13/month, better performance)
- Click "Select"

4. Click **"Next: Deployment >"** at the bottom

### Step 4: Configure GitHub Deployment

**GitHub Actions settings:**

1. **Enable GitHub Actions**: Toggle to `Enable`
2. **GitHub account**: Click "Authorize" and sign in to GitHub
3. **Organization**: Select your GitHub username
4. **Repository**: Select `resumeoptimization`
5. **Branch**: Select `main`

6. Click **"Next: Networking >"** (keep defaults)

7. Click **"Next: Monitoring >"** (keep defaults)

8. Click **"Review + create"**

### Step 5: Review and Create

1. Review all settings
2. Click **"Create"**
3. Wait 2-3 minutes for deployment ⏳

You'll see: "Your deployment is complete" ✅

4. Click **"Go to resource"**

---

## Part 3: Configure Environment Variables

### Step 1: Add Groq API Key

1. In your Azure Web App, find the left menu
2. Click on **"Environment variables"** (under Settings)
3. Click **"+ Add"** button

Add these environment variables:

**Variable 1:**
- **Name**: `GROQ_API_KEY`
- **Value**: `your-actual-groq-api-key-here`
- Click **"Apply"**

**Variable 2:**
- **Name**: `FLASK_ENV`
- **Value**: `production`
- Click **"Apply"**

4. Click **"Save"** at the top
5. Click **"Continue"** to confirm restart

---

## Part 4: Configure Startup Command

1. Still in "Environment variables" page
2. Scroll to **"Startup Command"** section
3. Enter this command:

```bash
bash startup.sh
```

4. Click **"Save"**
5. Click **"Continue"** to restart

---

## Part 5: Test Your Deployment

### Step 1: Get Your App URL

1. In the Azure portal, go to your Web App **"Overview"** page
2. Look for **"Default domain"**
3. Your URL will be: `https://your-app-name.azurewebsites.net`

### Step 2: Test the App

1. Click on the URL or paste it in your browser
2. You should see the Resume Optimizer interface! 🎉

If it doesn't load immediately:
- Wait 2-3 minutes (first load can be slow)
- Check "Log stream" in Azure portal (under Monitoring section)

### Step 3: Test Resume Optimization

1. Upload a test resume (PDF or DOCX)
2. Paste a job description
3. Click "Optimize Resume"
4. Verify it works!

---

## Part 6: Share with Your Team

Your employees can now access the app at:
```
https://your-app-name.azurewebsites.net
```

Just share this URL with your 5-10 employees!

---

## Monitoring & Logs

### View Logs

1. Go to your Web App in Azure Portal
2. Click **"Log stream"** (under Monitoring)
3. You'll see real-time logs

### View Metrics

1. Click **"Metrics"** (under Monitoring)
2. Add charts for:
   - CPU usage
   - Memory usage
   - HTTP requests

---

## Troubleshooting

### Problem: App not loading / 503 error

**Solution 1: Check logs**
1. Go to "Log stream" in Azure Portal
2. Look for errors

**Solution 2: Restart app**
1. Go to "Overview"
2. Click "Restart" at the top
3. Wait 2-3 minutes

### Problem: "Application Error"

**Solution: Check startup command**
1. Go to "Environment variables"
2. Verify Startup Command is: `bash startup.sh`
3. Save and restart

### Problem: Resume optimization not working

**Solution: Check GROQ_API_KEY**
1. Go to "Environment variables"
2. Verify `GROQ_API_KEY` is set correctly
3. Test the key at https://console.groq.com/
4. Update if needed and restart app

### Problem: Slow performance

**Solution: Upgrade to Basic tier**
1. Go to "Scale up (App Service plan)"
2. Select "Basic B1"
3. Click "Apply"

---

## Costs Breakdown

### Free Tier (F1)
- **Azure**: $0/month
- **Groq API**: ~$30/month (for 100-200 resumes/day)
- **Total**: ~$30/month

### Basic Tier (B1) - Recommended
- **Azure**: $13/month
- **Groq API**: ~$30/month
- **Total**: ~$43/month

---

## Updating Your App

Every time you push to GitHub:
1. Azure automatically detects the push
2. Rebuilds and redeploys your app
3. Takes ~2-3 minutes
4. Your app updates automatically! 🚀

To push updates:
```bash
git add .
git commit -m "Your update message"
git push
```

---

## Security Best Practices

✅ **Never commit your GROQ_API_KEY** to GitHub
✅ **Always use Environment Variables** in Azure
✅ **Keep your app updated** (Azure does this automatically)
✅ **Monitor usage** to avoid unexpected costs
✅ **Use HTTPS only** (Azure provides this by default)

---

## Next Steps

1. ✅ Deploy to Azure (follow this guide)
2. ✅ Test with your team (5-10 employees)
3. ✅ Monitor usage for 1 week
4. ✅ Collect feedback
5. ✅ Upgrade tier if needed

---

## Support

### Azure Support
- Azure Portal: https://portal.azure.com
- Documentation: https://docs.microsoft.com/azure/app-service/

### Groq Support
- Console: https://console.groq.com/
- Documentation: https://console.groq.com/docs

### Application Issues
- Check logs in Azure Portal "Log stream"
- Review GitHub repository: https://github.com/mitacharya777-arch/resumeoptimization

---

**Congratulations! You're ready to deploy! 🎉**

Total deployment time: ~15-20 minutes

Your employees will love it! 🚀
