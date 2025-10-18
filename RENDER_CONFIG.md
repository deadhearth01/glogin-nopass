# 📝 Render Configuration Quick Reference

## When Creating Web Service on Render

Fill in these fields exactly:

### ✅ Basic Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `gitam-login-generator` | Or any name you prefer |
| **Region** | `Oregon (US West)` | Or closest to you |
| **Branch** | `main` | Default branch |
| **Root Directory** | Leave blank or `./` | Root of repository |
| **Runtime** | `Python 3` | Auto-detected |

### ✅ Build & Deploy Settings

| Field | Value | Notes |
|-------|-------|-------|
| **Build Command** | `pip install -r requirements.txt` | Installs dependencies |
| **Start Command** | `gunicorn app:app` | Starts production server |
| **Publish Directory** | **Leave blank** | Not needed for Flask backend |

> ⚠️ **Important:** "Publish Directory" is only for static sites (React, Vue, etc.). Flask is a backend application, so leave this field **blank** or it may cause deployment errors.

### ✅ Instance Type

Choose one:

- **Free** 
  - Good for: Testing, personal use
  - Limitations: Spins down after 15 min inactivity
  - Cost: $0/month

- **Starter** (Recommended for production)
  - Good for: Production use
  - Benefits: Always on, faster response
  - Cost: $7/month

### ✅ Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these 5 variables:

```
SUPABASE_URL=https://ntoewmrrwcinjvrwkgpu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50b2V3bXJyd2Npbmp2cndrZ3B1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNzM4MTgsImV4cCI6MjA3NDY0OTgxOH0.pY1280bWzvBqvwNaZV-jMP7n84Sr0qtCPQXMI-qbVB8
SECRET_KEY=4ca01deadfa576f8968e2fc41ff59018c5cf4173a7cdd453c8d1bc36139a19f1
ENCRYPTION_KEY=TU4ye6CPOtlCE1URkePijI0z0vkv69A8m9f-JrYhNgs=
FLASK_ENV=production
```

---

## 🎯 Common Mistakes to Avoid

❌ **Don't** set Publish Directory (leave it blank)  
❌ **Don't** use `python app.py` as start command (use `gunicorn app:app`)  
❌ **Don't** forget to add environment variables  
❌ **Don't** select "Static Site" (select "Web Service")  

✅ **Do** leave Publish Directory blank  
✅ **Do** use `gunicorn app:app` as start command  
✅ **Do** add all 5 environment variables  
✅ **Do** select "Web Service" when creating  

---

## 📸 Visual Guide

**Step-by-step screenshots:**

1. **New Web Service**
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Select: `deadhearth01/glogin-nopass`

3. **Basic Settings**
   ```
   Name: gitam-login-generator
   Region: Oregon (US West)
   Branch: main
   Root Directory: (blank)
   ```

4. **Build Settings**
   ```
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Publish Directory: (blank) ← IMPORTANT!
   ```

5. **Environment Variables**
   - Click "Advanced"
   - Add 5 variables (see above)

6. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes

---

## 🔍 What Each Setting Does

**Build Command:**
- Installs Python packages from `requirements.txt`
- Includes Flask, Gunicorn, Supabase, etc.

**Start Command:**
- `gunicorn app:app` starts the production WSGI server
- Format: `gunicorn <filename>:<flask_app_variable>`
- Our file is `app.py` with `app = Flask(__name__)`

**Publish Directory:**
- Used for static sites (HTML/CSS/JS only)
- Flask serves dynamic content, so **not needed**
- Leave blank to avoid deployment errors

**Environment Variables:**
- Secrets that shouldn't be in code
- Loaded by `python-dotenv` in production
- Same as `.env` file but secure

---

## ✅ After Deployment

Your app will be live at:
```
https://gitam-login-generator.onrender.com
```

Test it:
1. Visit the URL
2. Enter GITAM credentials
3. Get no-password login link
4. Check Supabase for saved data

---

## 📚 More Help

- Full guide: `DEPLOYMENT.md`
- Project docs: `README.md`
- Render docs: https://render.com/docs/web-services

---

**Quick Answer to Your Question:**

> **Publish Directory:** Leave blank (or don't fill it)

Flask is a backend application that serves dynamic content. The "Publish Directory" field is only for static sites (like React/Vue builds). For Flask, Render will use Gunicorn to serve your application directly, so no publish directory is needed.
