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
| **Publish Directory** | `./` | Use `./` (current directory) - REQUIRED |

> ⚠️ **Important:** Even though Flask doesn't need a publish directory, Render requires this field. Use `./` (dot slash) to indicate the current directory.

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

Add these 5 variables (get values from your `.env` file):

| Variable | Where to Get Value |
|----------|-------------------|
| `SUPABASE_URL` | From Supabase dashboard → Project Settings → API |
| `SUPABASE_ANON_KEY` | From Supabase dashboard → Project Settings → API |
| `SECRET_KEY` | From your local `.env` file |
| `ENCRYPTION_KEY` | From your local `.env` file |
| `FLASK_ENV` | Set to `production` |

> 🔒 **Security:** Never commit these values to GitHub. Add them directly in Render dashboard.

---

## 🎯 Common Mistakes to Avoid

❌ **Don't** leave Publish Directory blank (Render requires it now)  
❌ **Don't** use `python app.py` as start command (use `gunicorn app:app`)  
❌ **Don't** forget to add environment variables  
❌ **Don't** select "Static Site" (select "Web Service")  
❌ **Don't** commit secret keys to GitHub

✅ **Do** set Publish Directory to `./`  
✅ **Do** use `gunicorn app:app` as start command  
✅ **Do** add all 5 environment variables in Render dashboard  
✅ **Do** select "Web Service" when creating  
✅ **Do** keep secrets in Render environment variables only  

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
   Publish Directory: ./ ← REQUIRED (use dot slash)
   ```

5. **Environment Variables**
   - Click "Advanced"
   - Add 5 variables from your `.env` file
   - Never commit these to GitHub!

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
- Render now requires this field (mandatory)
- For Flask apps, use `./` (current directory)
- This tells Render where your app files are located
- Even though Flask doesn't build static files, Render needs this setting

**Environment Variables:**
- Secrets that shouldn't be in code
- Loaded by `python-dotenv` in production
- Copy values from your local `.env` file
- Add them manually in Render dashboard (one by one)

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

> **Publish Directory:** Required by Render - use `./` (dot slash)

Render made this field mandatory. For Flask backend applications, use `./` to indicate the current directory where your app files are located. This is different from static sites which have build folders like `dist` or `build`.
