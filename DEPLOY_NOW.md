# 🚀 Deploy Louis Slutton to Production (Railway + Vercel)

## Prerequisites
- ✅ GitHub repo: https://github.com/adamdasovich/slutton_v2
- ✅ Code pushed with deployment configs
- ✅ GoDaddy domain: louisslutton.com

---

## Part 1: Deploy Backend to Railway (20 minutes)

### Step 1: Create Railway Account & Project

1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway to access your GitHub account
4. Click "New Project"
5. Select "Deploy from GitHub repo"
6. Choose `adamdasovich/slutton_v2`
7. Railway will detect it's a monorepo

### Step 2: Configure Backend Service

1. **Set Root Directory**:
   - Click on the deployed service
   - Go to "Settings" tab
   - Find "Root Directory"
   - Set to: `backend`
   - Click "Save"

2. **Add PostgreSQL Database**:
   - In your project dashboard, click "+ New"
   - Select "Database"
   - Choose "PostgreSQL"
   - Wait 30 seconds for it to provision
   - Railway automatically creates `DATABASE_URL` variable

3. **Add Redis for WebSockets** (Optional but recommended):
   - Click "+ New"
   - Select "Database"
   - Choose "Redis"
   - Railway automatically creates `REDIS_URL` variable

### Step 3: Configure Environment Variables

Click on your backend service → "Variables" tab → Add these:

```bash
# Required
DJANGO_SETTINGS_MODULE=slutton_backend.settings_production
SECRET_KEY=<generate-new-secure-key>
ANTHROPIC_API_KEY=<your-claude-api-key>

# Optional (if using Stripe)
STRIPE_SECRET_KEY=<your-stripe-secret>
STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>
```

**Generate a secure SECRET_KEY:**
```python
# Run this in Python:
import secrets
print(secrets.token_urlsafe(50))
```

### Step 4: Deploy Backend

1. Railway will automatically deploy after detecting changes
2. Go to "Deployments" tab to watch progress
3. Wait for build to complete (3-5 minutes)
4. Check logs for any errors

### Step 5: Run Database Migrations

**Option A: Using Railway CLI** (Recommended):

Install Railway CLI:
```bash
# Windows (PowerShell as admin)
iwr https://railway.app/install.ps1 | iex

# Mac/Linux
curl -fsSL https://railway.app/install.sh | sh
```

Run migrations:
```bash
cd backend
railway login
railway link
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
```

**Option B: Using Railway Dashboard**:

1. Go to your backend service
2. Click "Settings" → "Service"
3. Add one-off commands:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

### Step 6: Import Your Data

From your local machine:

```bash
cd backend

# Set DATABASE_URL to Railway's PostgreSQL
# Get this from Railway Variables tab
set DATABASE_URL=postgresql://postgres:xxx@xxx.railway.app:5432/railway

# Import data
python import_data.py
```

### Step 7: Get Backend URL

1. Go to "Settings" → "Networking"
2. Click "Generate Domain"
3. You'll get a URL like: `slutton-backend-production.up.railway.app`
4. **Copy this URL** - you'll need it for Vercel

---

## Part 2: Deploy Frontend to Vercel (10 minutes)

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### Step 2: Import Project

1. Click "Add New..." → "Project"
2. Import `adamdasovich/slutton_v2`
3. Vercel detects it's a monorepo

### Step 3: Configure Project

**Framework Preset**: Next.js (auto-detected)

**Root Directory**:
- Click "Edit"
- Select `frontend`
- Click "Continue"

**Environment Variables**:

Add these variables:

```bash
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app/api
NEXT_PUBLIC_WS_URL=wss://your-railway-backend-url.up.railway.app/ws
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx (if using Stripe)
```

Replace `your-railway-backend-url.up.railway.app` with your actual Railway domain from Part 1, Step 7.

### Step 4: Deploy

1. Click "Deploy"
2. Wait 2-3 minutes for build
3. You'll get a URL like: `slutton-v2.vercel.app`
4. Test the deployment!

---

## Part 3: Connect Custom Domain louisslutton.com from GoDaddy (30 minutes)

### Overview

You'll configure your GoDaddy domain `louisslutton.com` to point to your deployed services:

- **louisslutton.com** → Vercel (Frontend)
- **www.louisslutton.com** → Vercel (Frontend)
- **api.louisslutton.com** → Railway (Backend)

### Step A: Access GoDaddy DNS Settings

1. **Log in to GoDaddy**:
   - Go to https://www.godaddy.com
   - Click "Sign In" (top right)
   - Enter your GoDaddy username and password

2. **Navigate to DNS Management**:
   - Click your profile icon (top right)
   - Select "My Products"
   - Find "louisslutton.com" in your domains list
   - Click the three dots (...) next to it
   - Select "Manage DNS" or "DNS"

3. **You should now see your DNS Records page** with existing records like:
   - Type: A, Name: @, Value: (parked page IP)
   - Type: CNAME, Name: www, Value: @
   - Type: NS, Name: @, Value: (nameservers)

**Important**: Keep this page open - you'll be editing these records.

---

### Step B: Configure Backend Domain (api.louisslutton.com → Railway)

#### B1. Get Railway Backend URL

1. Go to https://railway.app/dashboard
2. Click on your backend service
3. Go to "Settings" → "Networking"
4. Under "Domains", you should see your generated domain
   - Example: `slutton-backend-production.up.railway.app`
5. **Copy this full URL** (you'll need it for GoDaddy)

#### B2. Add Custom Domain in Railway

1. In the same "Networking" section, click "Custom Domain"
2. Click "+ Add Custom Domain"
3. Enter: `api.louisslutton.com`
4. Click "Add Domain"
5. Railway will show:
   ```
   Add a CNAME record:
   Name: api
   Value: slutton-backend-production.up.railway.app
   ```
6. **Keep this tab open** - you'll verify it later

#### B3. Add CNAME Record in GoDaddy for API Subdomain

1. **Go back to your GoDaddy DNS Management page**
2. Click "Add New Record" or "Add" button
3. Fill in the form:
   ```
   Type: CNAME
   Name: api
   Value: <your-railway-url>.up.railway.app
   TTL: 600 seconds (or Custom: 600)
   ```
   **Example**:
   ```
   Type: CNAME
   Name: api
   Value: slutton-backend-production.up.railway.app
   ```

   **Important Notes**:
   - For "Name", enter only `api` (NOT `api.louisslutton.com`)
   - For "Value", use your full Railway URL from Step B1
   - Do NOT include "https://" in the value
   - Do NOT add a period at the end

4. Click "Save" or "Add Record"

#### B4. Verify Railway Backend Domain

1. **Go back to Railway** → Networking section
2. Wait 1-2 minutes, then refresh the page
3. The status should change to "Active" or show a green checkmark
4. If it shows "Waiting for DNS", wait 5-10 more minutes

**Test It**:
- Open a new browser tab
- Visit: `https://api.louisslutton.com/admin`
- You should see your Django admin login page
- ✅ If it loads, backend domain is working!
- ❌ If you get an error, wait 10 more minutes (DNS propagation)

---

### Step C: Configure Frontend Domain (louisslutton.com → Vercel)

#### C1. Add Custom Domain in Vercel

1. Go to https://vercel.com/dashboard
2. Click on your frontend project (slutton-v2 or similar)
3. Click "Settings" (top navigation)
4. Click "Domains" (left sidebar)
5. You'll see your default Vercel domain (e.g., `slutton-v2.vercel.app`)

#### C2. Add Root Domain (louisslutton.com)

1. In the "Domains" section, find the input field that says "Enter domain name..."
2. Type: `louisslutton.com`
3. Click "Add"
4. Vercel will analyze your domain and show DNS configuration needed
5. You'll see a screen like:

   ```
   louisslutton.com

   Configure your DNS provider to point to Vercel:

   A Record
   Name: @
   Value: 76.76.21.21

   Status: Invalid Configuration
   ```

6. **Keep this tab open** - you'll verify it later

#### C3. Add WWW Subdomain (www.louisslutton.com)

1. In the same "Domains" section, click "Add" again
2. Type: `www.louisslutton.com`
3. Click "Add"
4. Vercel will show:

   ```
   www.louisslutton.com

   Configure your DNS provider to point to Vercel:

   CNAME Record
   Name: www
   Value: cname.vercel-dns.com

   Status: Invalid Configuration
   ```

7. **Keep this tab open**

#### C4. Update GoDaddy DNS Records for Root Domain

**Go back to GoDaddy DNS Management page**

**Step 1: Delete or Update Existing @ A Record**

1. Find the existing A record with Name: @ (usually points to a parked page)
2. Click the pencil/edit icon
3. **Option A - Edit**:
   - Change "Value" to: `76.76.21.21`
   - Set TTL to: 600 seconds
   - Click "Save"

   **Option B - Delete and Add New**:
   - Click the trash/delete icon to remove it
   - Click "Add New Record"
   - Fill in:
     ```
     Type: A
     Name: @
     Value: 76.76.21.21
     TTL: 600
     ```
   - Click "Save"

**Step 2: Delete or Update Existing www CNAME Record**

1. Find the existing CNAME record with Name: www
2. Click edit or delete
3. **Update it to**:
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 600
   ```
4. Click "Save"

**Important Notes**:
- For "Name: @" means the root domain (louisslutton.com)
- GoDaddy may show @ as "louisslutton.com" in the interface - that's fine
- Do NOT include "https://" in any Value field
- Do NOT add periods at the end of values

#### C5. Your GoDaddy DNS Should Now Look Like This

After completing all steps, your DNS records should include:

```
TYPE     NAME     VALUE                                    TTL
-----------------------------------------------------------
A        @        76.76.21.21                             600
CNAME    api      slutton-backend-production.up.railway.app   600
CNAME    www      cname.vercel-dns.com                    600
NS       @        ns**.domaincontrol.com                  1 Hour
NS       @        ns**.domaincontrol.com                  1 Hour
```

**Click "Save All Changes" if GoDaddy requires it**

---

### Step D: Verify Domain Configuration

#### D1. Wait for DNS Propagation (5-30 minutes)

DNS changes can take time. Typically:
- **Fastest**: 5-10 minutes
- **Average**: 15-20 minutes
- **Worst case**: Up to 48 hours (rare)

#### D2. Check DNS Propagation Status

Use this free tool to check if your DNS has propagated:

1. Go to https://dnschecker.org
2. Check each domain:
   - Enter `louisslutton.com` - should show `76.76.21.21`
   - Enter `www.louisslutton.com` - should show `cname.vercel-dns.com`
   - Enter `api.louisslutton.com` - should show your Railway URL

3. Look for green checkmarks around the world
4. If you see different IPs in different locations, DNS is still propagating

#### D3. Verify in Vercel

1. Go back to Vercel → Project → Settings → Domains
2. Refresh the page
3. Both domains should now show:
   ```
   ✅ louisslutton.com - Valid Configuration
   ✅ www.louisslutton.com - Valid Configuration
   ```

4. Vercel automatically issues SSL certificates (may take 5-10 minutes)

#### D4. Verify in Railway

1. Go to Railway → Backend Service → Settings → Networking
2. Your custom domain should show:
   ```
   ✅ api.louisslutton.com - Active
   ```

---

### Step E: Update Environment Variables with Custom Domains

Now that your domains are active, update your environment variables:

#### E1. Update Vercel Environment Variables

1. Go to Vercel → Project → Settings → Environment Variables
2. **Edit** these variables:
   ```
   NEXT_PUBLIC_API_URL=https://api.louisslutton.com/api
   NEXT_PUBLIC_WS_URL=wss://api.louisslutton.com/ws
   ```
3. Make sure they apply to "Production" environment
4. Click "Save"

#### E2. Redeploy Frontend

After updating variables:
1. Go to Vercel → Project → Deployments
2. Click on the latest deployment
3. Click "..." (three dots)
4. Click "Redeploy"
5. Wait 2-3 minutes for redeployment

#### E3. No Changes Needed on Railway

The `settings_production.py` already includes:
- `api.louisslutton.com` in ALLOWED_HOSTS
- Proper CORS settings for louisslutton.com

---

### Step F: Configure Domain Redirect (Optional but Recommended)

**Make www.louisslutton.com redirect to louisslutton.com**:

1. In Vercel → Settings → Domains
2. Find `www.louisslutton.com`
3. Click "Edit"
4. Select "Redirect to louisslutton.com"
5. Choose "Permanent (308)"
6. Click "Save"

This ensures users always see `louisslutton.com` in their browser.

---

### Step G: Test Everything

#### Test 1: Frontend Domain
- Visit: `https://louisslutton.com` ✅
- Visit: `https://www.louisslutton.com` (should redirect to above) ✅
- Check for SSL padlock in browser ✅

#### Test 2: Backend Domain
- Visit: `https://api.louisslutton.com/admin` ✅
- Should see Django admin login ✅
- Check for SSL padlock ✅

#### Test 3: API Connection
1. Go to `https://louisslutton.com`
2. Open browser console (F12)
3. Navigate to products or games
4. Check Network tab - API calls should go to `api.louisslutton.com` ✅
5. Should not see any CORS errors ✅

#### Test 4: WebSocket Connection
1. Go to `https://louisslutton.com/trivia`
2. Open browser console
3. Look for "WebSocket connected" message ✅
4. Check WebSocket URL uses `wss://api.louisslutton.com` ✅

---

### Troubleshooting GoDaddy DNS

#### Problem: "This site can't be reached"

**Solution**:
- DNS hasn't propagated yet - wait 15 more minutes
- Check dnschecker.org to see propagation status
- Clear your browser cache (Ctrl + Shift + Delete)
- Try in incognito/private browsing mode

#### Problem: Vercel shows "Invalid Configuration"

**Solution**:
- Make sure A record points to `76.76.21.21` exactly
- Make sure CNAME for www points to `cname.vercel-dns.com` exactly
- Wait 10-15 minutes after saving changes
- Check for typos in GoDaddy DNS records

#### Problem: Railway shows "Waiting for DNS"

**Solution**:
- Make sure CNAME for api points to your Railway URL exactly
- Don't include https:// in the CNAME value
- Don't add a trailing period
- Wait 10-15 minutes for DNS propagation

#### Problem: SSL Certificate Error

**Solution**:
- Railway and Vercel auto-generate SSL certificates
- This can take 10-20 minutes after DNS is configured
- If error persists after 30 minutes, check domain spelling

#### Problem: API calls fail with CORS error

**Solution**:
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Make sure you redeployed after changing environment variables
- Check Railway logs for CORS errors
- Verify `api.louisslutton.com` is in ALLOWED_HOSTS

---

### GoDaddy-Specific Tips

1. **DNS Changes Are Not Instant**: Even though GoDaddy says "saved", propagation takes time
2. **Use TTL 600**: This is 10 minutes - good balance between speed and caching
3. **Don't Delete NS Records**: Keep your nameserver (NS) records - these are critical
4. **GoDaddy Forwarding vs DNS**: Make sure you're in "DNS Management" not "Domain Forwarding"
5. **Clear GoDaddy Cache**: Sometimes GoDaddy caches old values - wait or use incognito mode

---

### After Successful Domain Connection

Once everything is working:

✅ Your site is live at `https://louisslutton.com`
✅ API accessible at `https://api.louisslutton.com`
✅ Both have valid SSL certificates
✅ Frontend connects to backend via custom domains
✅ WebSockets working over WSS

**Update your .env files locally**:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://api.louisslutton.com/api
NEXT_PUBLIC_WS_URL=wss://api.louisslutton.com/ws
```

This ensures local development uses production API for testing.

---

## Part 4: Testing & Verification

### Test Backend

1. Visit: `https://api.louisslutton.com/admin`
2. Log in with superuser credentials
3. Check that your data is visible

### Test Frontend

1. Visit: `https://louisslutton.com`
2. Test navigation
3. Test user registration/login
4. Test product pages
5. Test games (Trivia, Memory Match)
6. Test cart and checkout
7. Test comments and ratings

### Test WebSockets

1. Go to trivia or memory match game
2. Check browser console for WebSocket connection
3. Should see: "WebSocket connected"

---

## Part 5: Post-Deployment Tasks

### Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Added custom domains to ALLOWED_HOSTS
- [ ] SSL certificates active (auto by Railway/Vercel)
- [ ] Admin panel accessible only via HTTPS
- [ ] Environment variables secured

### Monitoring

**Railway:**
- Go to "Observability" to view logs
- Set up usage alerts

**Vercel:**
- Go to "Analytics" to view traffic
- Go to "Logs" to debug issues

### Backups

**Database Backup (run weekly):**

```bash
railway run pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql
```

---

## Troubleshooting

### Backend won't deploy
- Check logs in Railway dashboard
- Verify `DJANGO_SETTINGS_MODULE=slutton_backend.settings_production`
- Verify `DATABASE_URL` is set

### Frontend can't connect to backend
- Check CORS settings in settings_production.py
- Verify `NEXT_PUBLIC_API_URL` has `/api` at the end
- Check browser console for CORS errors

### Static files not loading
- Run: `railway run python manage.py collectstatic --noinput`
- Verify WhiteNoise is in MIDDLEWARE

### WebSockets not working
- Verify `REDIS_URL` is set on Railway
- Check that Channels is using Redis, not InMemoryChannelLayer
- Verify `NEXT_PUBLIC_WS_URL` uses `wss://` not `ws://`

### Database connection failed
- Check `DATABASE_URL` format
- Verify PostgreSQL service is running in Railway
- Test connection: `railway run python manage.py dbshell`

---

## Quick Reference

### Railway URLs
- Dashboard: https://railway.app/dashboard
- CLI Docs: https://docs.railway.app/develop/cli

### Vercel URLs
- Dashboard: https://vercel.com/dashboard
- Docs: https://vercel.com/docs

### Your URLs (after setup)
- Backend: https://api.louisslutton.com
- Admin: https://api.louisslutton.com/admin
- Frontend: https://louisslutton.com
- GitHub: https://github.com/adamdasovich/slutton_v2

---

## Estimated Costs

- **Railway**: $5-10/month (backend + PostgreSQL + Redis)
- **Vercel**: Free (Hobby plan sufficient for starting)
- **Total**: ~$5-10/month

---

## Support

If you encounter issues:

1. Check Railway logs: `railway logs`
2. Check Vercel logs: Project → "Logs"
3. Check DEPLOYMENT_GUIDE.md for detailed troubleshooting
4. Railway Discord: https://discord.gg/railway
5. Vercel Support: https://vercel.com/support
