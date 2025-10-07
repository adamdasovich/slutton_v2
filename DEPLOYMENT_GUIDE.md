# Louis Slutton - Production Deployment Guide

## 🎯 Recommended Architecture

### **Monorepo Approach (RECOMMENDED for your project)**
Keep your current structure with both `backend/` and `frontend/` in a single repository.

**Why Monorepo?**
- ✅ Easier version synchronization between frontend and backend
- ✅ Simpler CI/CD pipeline configuration
- ✅ Single source of truth for the entire application
- ✅ Better for small-to-medium teams/solo developers
- ✅ Your current GitHub repo already follows this pattern

---

## 🚀 Hosting Providers Recommendation

### **Option 1: Railway (RECOMMENDED) - All-in-One Solution**

**Cost:** $5-20/month
**Best for:** Quick deployment, minimal DevOps, PostgreSQL included

#### Why Railway?
- ✅ Deploys Django + Next.js + PostgreSQL from one monorepo
- ✅ Automatic HTTPS
- ✅ Built-in PostgreSQL database
- ✅ GitHub integration with auto-deploy
- ✅ Generous free tier ($5 credit/month)
- ✅ Simple environment variable management
- ✅ WebSocket support (for your Channels setup)

**Estimated Cost:**
- Backend (Django): $5/month (512MB RAM, 1 vCPU)
- Frontend (Next.js): $5/month (512MB RAM)
- PostgreSQL: $5/month (1GB storage)
- **Total: ~$15/month**

---

### **Option 2: Render (Alternative - Similar to Railway)**

**Cost:** $7-25/month
**Best for:** Reliability, better PostgreSQL options

#### Why Render?
- ✅ Similar to Railway but more mature
- ✅ PostgreSQL with automatic backups
- ✅ Excellent documentation
- ✅ Static site hosting for Next.js
- ✅ Background workers for Celery (if needed later)

**Estimated Cost:**
- Backend: $7/month (Web Service)
- Frontend: $0 (Static Site)
- PostgreSQL: $7/month (Starter plan)
- **Total: ~$14/month**

---

### **Option 3: Separate Providers (Most Scalable)**

**Cost:** $0-50/month
**Best for:** Maximum control, future scalability

#### Stack:
- **Backend:** Railway ($5-10/month) or Render ($7/month)
- **Frontend:** Vercel ($0 - free tier sufficient) or Netlify ($0)
- **Database:** Supabase ($0 free tier) or Railway/Render included

**Estimated Cost:** $5-15/month

---

## 📋 Step-by-Step Deployment Plan

### **Phase 1: Prepare Your Application**

#### 1.1 Create Production Django Settings

Create `backend/slutton_backend/settings_production.py`:

```python
import os
from .settings import *
import dj_database_url

# SECURITY SETTINGS
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = [
    'louisslutton.com',
    'www.louisslutton.com',
    'api.louisslutton.com',
    '.railway.app',  # Railway subdomain
    '.onrender.com',  # Render subdomain
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://louisslutton.com',
    'https://www.louisslutton.com',
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (for user uploads)
if os.environ.get('USE_S3') == 'TRUE':
    # Use S3 for production
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Channels (WebSockets)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

#### 1.2 Update Requirements

Add to `backend/requirements.txt`:
```txt
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
python-decouple==3.8
```

#### 1.3 Create Procfile for Backend

Create `backend/Procfile`:
```
web: gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: daphne -b 0.0.0.0 -p $PORT slutton_backend.asgi:application
```

#### 1.4 Create railway.json (if using Railway)

Create `railway.json` in root:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 1.5 Update Frontend Environment Variables

Create `frontend/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://api.louisslutton.com
NEXT_PUBLIC_WS_URL=wss://api.louisslutton.com
```

---

### **Phase 2: Database Migration**

#### 2.1 Export Current SQLite Data

**IMPORTANT: Use the custom script on Windows to handle emojis properly**

```bash
# In backend directory
python export_data.py
```

This creates `datadump.json` with all your data (100 objects exported successfully).

**Why not use Django's dumpdata?** The standard Django command fails on Windows when there are emoji characters (🎮💋🎯) in your database. The custom script handles UTF-8 encoding properly.

#### 2.2 Create PostgreSQL Database

---

### **Option A: Railway (Recommended - Easiest)**

**Step 1: Sign Up & Create Project**

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub (this will also connect your repositories)
4. You'll receive $5 free credit monthly

**Step 2: Provision PostgreSQL Database**

1. From Railway Dashboard, click "+ New"
2. Select "Database"
3. Choose "Add PostgreSQL"
4. Railway instantly provisions a PostgreSQL database

**Step 3: Get Connection Details**

1. Click on the PostgreSQL service (purple icon)
2. Go to "Variables" tab
3. You'll see these automatically generated variables:
   ```
   PGHOST=your-region.railway.app
   PGPORT=5432
   PGDATABASE=railway
   PGUSER=postgres
   PGPASSWORD=<generated-password>
   DATABASE_URL=postgresql://postgres:<password>@host:5432/railway
   ```

4. **Copy the `DATABASE_URL`** - this is what you'll need
   - Format: `postgresql://postgres:password@host.railway.app:5432/railway`
   - Example: `postgresql://postgres:gH8kL2mN@containers-us-west-123.railway.app:5432/railway`

**Step 4: Save Credentials Securely**

Create a file `backend/.env.production` (don't commit this!):
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_HOST.railway.app:5432/railway
```

---

### **Option B: Render (Alternative - Good for Backups)**

**Step 1: Sign Up**

1. Go to https://render.com
2. Sign up with GitHub
3. Free tier includes 90 days of PostgreSQL

**Step 2: Create PostgreSQL Database**

1. From Dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in details:
   - **Name**: `slutton-db`
   - **Database**: `slutton_production` (or any name)
   - **User**: `slutton_user` (auto-generated)
   - **Region**: Choose closest to your users (e.g., Oregon USA)
   - **PostgreSQL Version**: 15 or latest
   - **Plan**: Starter ($7/month) - includes backups

4. Click "Create Database"

**Step 3: Get Connection Details**

After creation (takes 1-2 minutes), you'll see:

1. **Internal Database URL** (for apps on Render):
   ```
   postgres://user:pass@internal-host/dbname
   ```

2. **External Database URL** (for local testing):
   ```
   postgresql://user:pass@oregon-postgres.render.com/dbname
   ```

3. **Connection Details**:
   - **Hostname**: `oregon-postgres.render.com`
   - **Port**: `5432`
   - **Database**: `slutton_production`
   - **Username**: `slutton_user`
   - **Password**: `<auto-generated-secure-password>`

4. Copy the **External Database URL** for migration

---

### **Option C: Supabase (Free Forever - Good for Testing)**

**Step 1: Create Project**

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New Project"

**Step 2: Configure Project**

Fill in:
- **Name**: `louis-slutton`
- **Database Password**: Create a strong password (save it!)
- **Region**: Choose closest region
- **Pricing Plan**: Free (500MB database, 2GB bandwidth)

Click "Create new project" (takes ~2 minutes)

**Step 3: Get Connection String**

1. Go to Project Settings (gear icon)
2. Click "Database" in sidebar
3. Scroll to "Connection String"
4. Select "URI" tab
5. Copy the connection string:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.projectref.supabase.co:5432/postgres
   ```

6. Replace `[YOUR-PASSWORD]` with the password you created

**Important**: Use "Transaction" mode for Django:
```
postgresql://postgres:password@db.projectref.supabase.co:6543/postgres?pgbouncer=true
```

---

#### 2.3 Migrate to PostgreSQL

Now that you have a PostgreSQL database, let's migrate your data.

---

### **Step 1: Install PostgreSQL Adapter (if not already installed)**

```bash
cd backend

# Check if already installed
pip list | grep psycopg2

# If not installed, add it
pip install psycopg2-binary
```

---

### **Step 2: Configure Django to Use PostgreSQL**

**Option A: Environment Variable (Recommended)**

```bash
# Windows Command Prompt
set DATABASE_URL=postgresql://user:password@host:5432/dbname

# Windows PowerShell
$env:DATABASE_URL="postgresql://user:password@host:5432/dbname"

# Mac/Linux
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

**Replace with your actual connection string from Railway/Render/Supabase.**

Example:
```bash
export DATABASE_URL="postgresql://postgres:gH8kL2mN@containers-us-west-123.railway.app:5432/railway"
```

**Option B: Direct Settings Update (for testing only)**

Edit `backend/slutton_backend/settings.py` temporarily:

```python
import dj_database_url

# Comment out SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Add PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:pass@host:5432/dbname',
        conn_max_age=600,
    )
}
```

Install dj-database-url first:
```bash
pip install dj-database-url
```

---

### **Step 3: Test Database Connection**

```bash
cd backend
python manage.py dbshell
```

If successful, you'll see:
```
psql (15.x)
Type "help" for help.

railway=#
```

Type `\q` to exit.

**If connection fails:**
- Check your DATABASE_URL is correct
- Verify PostgreSQL service is running on Railway/Render
- Check firewall/network settings
- Ensure password doesn't contain special characters that need URL encoding

---

### **Step 4: Create Database Schema**

Run migrations to create all tables:

```bash
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions,
  users, products, games, trivia, ratings, comments, cart, orders
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ... (many more)
  Applying trivia.0002_triviaquestion_options... OK
Total: 47 migrations applied
```

**Common Issues:**

- **"FATAL: password authentication failed"**: Wrong password in DATABASE_URL
- **"could not connect to server"**: Wrong host or port
- **"database does not exist"**: Check database name in URL

---

### **Step 5: Import Your Data**

Now load your 100 objects from the backup:

```bash
# Make sure datadump.json exists
ls datadump.json

# Import using our custom script
python import_data.py
```

**Expected Output:**
```
Importing data from datadump.json...
This may take a minute...
Installed 100 object(s) from 1 fixture(s)

Successfully imported all data!

Next steps:
1. Create a superuser: python manage.py createsuperuser
2. Test your application
```

**Alternative (if import_data.py doesn't work):**
```bash
python manage.py loaddata datadump.json
```

**If you get errors:**

**Error: "IntegrityError: duplicate key value"**
- Solution: Database not empty. Clear it first or use fresh database

**Error: "DoesNotExist: matching query does not exist"**
- Solution: Foreign key reference issue. Run migrations first: `python manage.py migrate`

**Error: "No module named 'trivia'"**
- Solution: Make sure all apps are installed in INSTALLED_APPS

---

### **Step 6: Verify Data Import**

Check that data was imported successfully:

```bash
# Enter Django shell
python manage.py shell
```

Run these commands:
```python
# Check users
from users.models import CustomUser
print(f"Users: {CustomUser.objects.count()}")

# Check products
from products.models import Product
print(f"Products: {Product.objects.count()}")

# Check games
from games.models import Game
print(f"Games: {Game.objects.count()}")

# Check trivia
from trivia.models import DailyTrivia
print(f"Trivia days: {DailyTrivia.objects.count()}")

# Exit shell
exit()
```

**Expected Output:**
```
Users: 1
Products: 1
Games: 3
Trivia days: 1
```

---

### **Step 7: Create Superuser (Production)**

Create a new admin account for production:

```bash
python manage.py createsuperuser
```

Fill in:
```
Username: admin
Email: your-email@example.com
Password: (create a strong password)
Password (again): (confirm)
Superuser created successfully.
```

**Important**:
- Use a different username than your local setup
- Use a very strong password for production
- Save these credentials in your password manager

---

### **Step 8: Collect Static Files**

Gather all static files for production:

```bash
python manage.py collectstatic --noinput
```

This copies all CSS, JS, and admin files to `staticfiles/` directory.

---

### **Step 9: Test Admin Panel**

Start the development server with PostgreSQL:

```bash
python manage.py runserver
```

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Verify you can see:
   - Users
   - Products
   - Games
   - Trivia
   - Orders
   - Comments

4. Check that data looks correct (images might be broken locally - that's OK, they'll work in production)

---

### **Step 10: Test API Endpoints**

Open browser or use curl:

```bash
# Test products API
curl http://localhost:8000/api/products/

# Test games API
curl http://localhost:8000/api/games/games/

# Test trivia API
curl http://localhost:8000/api/trivia/today/
```

All should return JSON data.

---

### **Rollback to SQLite (If Needed)**

If something goes wrong and you want to go back to SQLite:

```bash
# Windows
set DATABASE_URL=

# Mac/Linux
unset DATABASE_URL

# Restart server
python manage.py runserver
```

Django will automatically use SQLite again.

---

### **✅ Migration Checklist**

- [ ] PostgreSQL database created on Railway/Render/Supabase
- [ ] DATABASE_URL configured and tested
- [ ] `python manage.py migrate` completed successfully
- [ ] Data imported with `python import_data.py` (100 objects)
- [ ] Superuser created for production
- [ ] Static files collected
- [ ] Admin panel accessible and data visible
- [ ] API endpoints returning correct data
- [ ] datadump.json backed up safely

---

**Next Step**: Move to Phase 3 - Deploy Backend to Railway/Render

---

### **Phase 3: Deploy Backend (Railway Example)**

#### 3.1 Connect GitHub

1. Go to railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `slutton_v2` repository
4. Railway detects your Python project

#### 3.2 Configure Backend Service

1. Click on the service → Settings
2. Set **Root Directory**: `backend`
3. Set **Start Command**: `gunicorn slutton_backend.wsgi:application --bind 0.0.0.0:$PORT`

#### 3.3 Add Environment Variables

In Railway dashboard → Variables:
```env
SECRET_KEY=your-super-secret-key-generate-new-one
DJANGO_SETTINGS_MODULE=slutton_backend.settings_production
DATABASE_URL=postgresql://... (auto-provided by Railway)
ANTHROPIC_API_KEY=your-claude-key
STRIPE_SECRET_KEY=your-stripe-key
ALLOWED_HOSTS=api.louisslutton.com,.railway.app
CORS_ALLOWED_ORIGINS=https://louisslutton.com,https://www.louisslutton.com
```

#### 3.4 Add PostgreSQL Service

1. In same Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway automatically links it to your backend

#### 3.5 Deploy

1. Railway auto-deploys on git push
2. Check logs for any errors
3. Run migrations: Railway → Service → Settings → Deploy → Run Command:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

---

### **Phase 4: Deploy Frontend**

#### Option A: Vercel (RECOMMENDED for Next.js)

1. Go to vercel.com
2. Click "Import Project"
3. Connect GitHub → Select `slutton_v2`
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Environment Variables:
   ```env
   NEXT_PUBLIC_API_URL=https://api.louisslutton.com
   NEXT_PUBLIC_WS_URL=wss://api.louisslutton.com
   ```

6. Deploy → Vercel provides temporary URL

#### Option B: Railway (Same provider as backend)

1. In same Railway project, click "+ New"
2. Select "GitHub Repo" → Select `slutton_v2`
3. Configure:
   - **Root Directory**: `frontend`
   - **Start Command**: `npm run start`
   - **Build Command**: `npm run build`

4. Add environment variables (same as above)

---

### **Phase 5: Domain Configuration**

#### 5.1 Backend Domain (api.louisslutton.com)

**Railway:**
1. Go to Backend Service → Settings → Domains
2. Click "Generate Domain" (gets `.railway.app` subdomain)
3. Click "Custom Domain" → Enter: `api.louisslutton.com`
4. Railway provides DNS records

**GoDaddy DNS Configuration:**
```
Type: CNAME
Name: api
Value: <your-railway-url>.railway.app
TTL: 600
```

#### 5.2 Frontend Domain (louisslutton.com)

**Vercel:**
1. Go to Project → Settings → Domains
2. Add Domain: `louisslutton.com`
3. Add Domain: `www.louisslutton.com`
4. Vercel provides DNS records

**GoDaddy DNS Configuration:**
```
# Root domain
Type: A
Name: @
Value: 76.76.21.21 (Vercel IP)

# www subdomain
Type: CNAME
Name: www
Value: cname.vercel-dns.com

# API subdomain (if backend on Railway)
Type: CNAME
Name: api
Value: <your-backend>.railway.app
```

#### 5.3 SSL Certificates

- **Railway**: Automatic SSL (Let's Encrypt)
- **Vercel**: Automatic SSL (Let's Encrypt)
- **Both are free and auto-renew**

---

## 🔒 Security Checklist

### Backend Security

- [ ] Generate new `SECRET_KEY` for production
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS redirects
- [ ] Set secure cookie flags
- [ ] Add CORS whitelist
- [ ] Use environment variables for all secrets
- [ ] Enable Django security middleware
- [ ] Configure CSP headers
- [ ] Limit API rate limiting (django-ratelimit)

### Frontend Security

- [ ] No API keys in frontend code
- [ ] Use HTTPS for all API calls
- [ ] Implement CSRF tokens
- [ ] Sanitize user inputs
- [ ] Use Content Security Policy

### Database Security

- [ ] Use strong passwords
- [ ] Enable SSL connections
- [ ] Regular backups (Railway/Render do this automatically)
- [ ] Limit database access to backend only

---

## 📊 Cost Comparison

| Provider Stack | Monthly Cost | Pros | Cons |
|----------------|--------------|------|------|
| **Railway (All-in-One)** | $15-20 | Easy setup, monorepo support | Slightly more expensive |
| **Render (All-in-One)** | $14-20 | Reliable, good docs | Limited free tier |
| **Railway + Vercel** | $5-10 | Best Next.js performance | Two providers to manage |
| **Render + Vercel** | $7-15 | Good balance | Two providers |
| **Railway + Vercel + Supabase** | $0-10 | Free PostgreSQL | Three providers |

---

## 🚦 Post-Deployment Steps

1. **Test Everything**
   - [ ] API endpoints working
   - [ ] WebSocket connections (comments)
   - [ ] Authentication (JWT)
   - [ ] File uploads
   - [ ] Stripe payments
   - [ ] Claude AI integrations

2. **Setup Monitoring**
   - [ ] Sentry for error tracking (free tier)
   - [ ] Uptime monitoring (UptimeRobot - free)
   - [ ] Database performance monitoring

3. **Setup Backups**
   - [ ] Database backups (daily)
   - [ ] Media files backup (S3)

4. **Setup CI/CD**
   - [ ] Auto-deploy on `main` branch push
   - [ ] Run tests before deployment
   - [ ] Database migrations on deploy

---

## 🎯 My Recommendation

**For Louis Slutton, I recommend:**

1. **Backend + Database**: Railway ($10-15/month)
   - Includes PostgreSQL
   - Easy Django deployment
   - WebSocket support included

2. **Frontend**: Vercel (Free)
   - Best Next.js performance
   - Global CDN
   - Automatic SSL

3. **Domain Setup**:
   - `louisslutton.com` → Vercel (Frontend)
   - `api.louisslutton.com` → Railway (Backend)

**Total Cost: $10-15/month**

**Why This Stack?**
- ✅ Railway handles Django + PostgreSQL + WebSockets perfectly
- ✅ Vercel is the best platform for Next.js (free tier is generous)
- ✅ Clear separation: Frontend for users, API for backend
- ✅ Easy to scale later
- ✅ Automatic deployments from GitHub
- ✅ Both providers have excellent free SSL

---

## 📞 Next Steps

1. Create accounts on Railway and Vercel
2. Follow Phase 1-5 in order
3. Test each phase before moving to next
4. Keep your GitHub repo as source of truth
5. Document any environment variables you add

Would you like me to help you with any specific phase of the deployment?
