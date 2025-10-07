# Database Migration Guide: SQLite → PostgreSQL

## ✅ Step 1: Export Data from SQLite (LOCAL)

**Status**: ✅ **COMPLETED** - 100 objects exported successfully

```bash
cd backend
python export_data.py
```

**Output**: `datadump.json` (52.43 KB)

---

## 📋 Step 2: Setup PostgreSQL (PRODUCTION)

### Option A: Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Add PostgreSQL database
4. Copy connection string from Variables tab:
   ```
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

### Option B: Supabase (Free)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Go to Project Settings → Database
4. Copy connection string (Transaction mode)

---

## 🔄 Step 3: Configure Production Settings

Create `backend/slutton_backend/settings_production.py`:

```python
from .settings import *
import dj_database_url
import os

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Use PostgreSQL from environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

# Add to requirements.txt
# dj-database-url==2.1.0
```

---

## 🚀 Step 4: Migrate to PostgreSQL (PRODUCTION)

**On your production server (Railway/Render):**

```bash
# 1. Set environment variable
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
export DJANGO_SETTINGS_MODULE="slutton_backend.settings_production"

# 2. Run migrations
python manage.py migrate

# 3. Upload datadump.json to server

# 4. Import data
python import_data.py

# 5. Create superuser (if needed)
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput
```

---

## 🧪 Step 5: Test the Migration (LOCAL)

**Want to test PostgreSQL locally before deploying?**

### Setup Local PostgreSQL:

1. **Install PostgreSQL**:
   - Windows: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql`

2. **Create Test Database**:
   ```bash
   # Start PostgreSQL service
   # Windows: Check Services app
   # Mac: brew services start postgresql
   # Linux: sudo service postgresql start

   # Create database
   psql -U postgres
   CREATE DATABASE slutton_test;
   \q
   ```

3. **Update settings temporarily**:
   ```python
   # In settings.py (just for testing)
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'slutton_test',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Test Migration**:
   ```bash
   python manage.py migrate
   python import_data.py
   python manage.py runserver
   ```

5. **If successful, revert to SQLite for local dev** or keep PostgreSQL for both.

---

## 📊 What Gets Migrated?

Your export includes **100 objects** across these models:

### User Data:
- ✅ Users (CustomUser)
- ✅ User sessions

### Products & Orders:
- ✅ Product categories
- ✅ Products (with images/videos)
- ✅ Product ratings & reviews
- ✅ Cart items
- ✅ Orders

### Games:
- ✅ Game categories
- ✅ Games (Memory Match, Spin the Bottle, Truth or Dare)
- ✅ Game progress
- ✅ Game ratings
- ✅ Daily Memory Images (with Claude-generated themes)

### Trivia:
- ✅ Daily Trivia (Midnight Mysteries)
- ✅ Trivia Questions (15 per day)
- ✅ User trivia stats
- ✅ Trivia game sessions

### Social:
- ✅ Product comments (with WebSocket support)

---

## ⚠️ Important Notes

### What's NOT Exported:
- ❌ Django ContentTypes (auto-recreated)
- ❌ Permissions (auto-recreated)
- ❌ Media files (images/videos) - Need separate migration

### Media Files Migration:

**Option A: Manual Upload**
```bash
# Copy media folder to server
scp -r backend/media/* user@server:/path/to/media/
```

**Option B: Use AWS S3 (Recommended for production)**
1. Create S3 bucket
2. Install: `pip install django-storages boto3`
3. Configure in settings_production.py:
   ```python
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = 'louisslutton-media'
   ```
4. Upload existing files: `python manage.py collectstatic`

---

## 🆘 Troubleshooting

### Error: "relation does not exist"
**Solution**: Run migrations first: `python manage.py migrate`

### Error: "duplicate key value violates unique constraint"
**Solution**: Database not empty. Clear it first:
```sql
-- PostgreSQL
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

### Error: "could not connect to server"
**Solution**: Check DATABASE_URL is correct and PostgreSQL is running

### Error: "authentication failed"
**Solution**: Verify username/password in DATABASE_URL

### Import hangs or is very slow
**Solution**: Large databases take time. Be patient or increase database resources.

---

## ✅ Verification Checklist

After migration, verify:

- [ ] Admin panel works (`/admin`)
- [ ] Can login with superuser
- [ ] Products display correctly
- [ ] Games load (Memory Match, Trivia)
- [ ] User registration works
- [ ] Images/videos display (or S3 configured)
- [ ] WebSocket connections work (comments)
- [ ] Stripe payments work (test mode)
- [ ] Claude AI integrations work (trivia, memory images)

---

## 🎯 Production Database Maintenance

### Backups (Railway/Render automatic):
- Daily automated backups
- Point-in-time recovery
- Download backups from dashboard

### Manual Backup:
```bash
# Export from production
python export_data.py

# Download locally
scp user@server:/path/to/datadump.json ./backup-$(date +%Y%m%d).json
```

### Database Performance:
- Add indexes for frequently queried fields
- Monitor query performance
- Use connection pooling (Railway/Render handle this)

---

## 📞 Need Help?

Your data is safely exported in `datadump.json`. You can always:
1. Re-import to local SQLite for testing
2. Import to PostgreSQL when ready
3. Keep backups before major changes

**Next Step**: Follow Phase 3 in DEPLOYMENT_GUIDE.md to deploy your backend to Railway/Render.
