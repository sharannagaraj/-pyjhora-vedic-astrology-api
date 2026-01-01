# Deploy PyJHora API to Render (Free Tier)

## Prerequisites

1. **GitHub Account** - Create one at https://github.com if you don't have
2. **Render Account** - Sign up at https://render.com (use GitHub to sign in)
3. **Git Installed** - For pushing code to GitHub

---

## Step 1: Initialize Git Repository (if not done)

```bash
cd "H:\claude code\pyjhora-api"

# Initialize git
git init

# Create .gitignore
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo "*.egg-info/" >> .gitignore

# Add all files
git add .

# Commit
git commit -m "Initial commit - PyJHora Vedic Astrology API v1.2.0"
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```bash
# Install GitHub CLI if not installed
# Download from: https://cli.github.com/

# Login
gh auth login

# Create repository
gh repo create pyjhora-vedic-astrology-api --public --source=. --remote=origin --push
```

### Option B: Using GitHub Website

1. Go to https://github.com/new
2. Repository name: `pyjhora-vedic-astrology-api`
3. Description: "Vedic Astrology REST API using PyJHora library"
4. Make it **Public** (required for free tier)
5. **Don't** initialize with README (we already have code)
6. Click "Create repository"
7. Follow the instructions to push existing repository:

```bash
git remote add origin https://github.com/YOUR_USERNAME/pyjhora-vedic-astrology-api.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Render

### 3.1 Login to Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign in with GitHub (recommended)

### 3.2 Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if first time
   - Grant Render access to your repositories
   - Find and select `pyjhora-vedic-astrology-api`
4. Click "Connect"

### 3.3 Configure Service

Fill in the following details:

**Basic Settings:**
- **Name:** `pyjhora-api` (or your choice)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

**Plan:**
- Select **"Free"** plan
  - 512 MB RAM
  - Shared CPU
  - 750 hours/month free
  - Sleeps after 15 minutes of inactivity
  - Wakes on first request (~30 seconds)

**Environment Variables:**
Click "Add Environment Variable" and add:
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.0`

**Advanced:**
- **Health Check Path:** `/health`
- **Auto-Deploy:** Yes (recommended)

### 3.4 Deploy

1. Click "Create Web Service"
2. Wait for deployment (usually 5-10 minutes)
3. Watch the deployment logs

---

## Step 4: Verify Deployment

Once deployed, you'll get a URL like: `https://pyjhora-api.onrender.com`

### Test the API

```bash
# Test health endpoint
curl https://pyjhora-api.onrender.com/health

# Test root endpoint
curl https://pyjhora-api.onrender.com/

# Test comprehensive endpoint
curl -X POST https://pyjhora-api.onrender.com/api/v1/comprehensive/full-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1998-12-22",
      "time": "17:12:00",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "timezone_offset": 5.5,
      "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
  }'
```

### Access Documentation

- **Swagger UI:** https://pyjhora-api.onrender.com/docs
- **ReDoc:** https://pyjhora-api.onrender.com/redoc

---

## Important Notes about Free Tier

### ⚠️ Limitations

1. **Automatic Sleep:**
   - Service sleeps after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds to wake up
   - Subsequent requests are fast

2. **750 Hours/Month Limit:**
   - Service runs 24/7 = 720 hours/month
   - You're within the limit if running continuously
   - Multiple services share the 750 hours

3. **No Custom Domain (Free):**
   - Uses `*.onrender.com` subdomain
   - Custom domains available on paid plans

4. **Shared Resources:**
   - 512 MB RAM (sufficient for this API)
   - Shared CPU (adequate for light-moderate use)

5. **Public Repository Required:**
   - Free tier only works with public GitHub repos
   - Private repos require paid plan

### ✅ What Works Great on Free Tier

- ✅ All API endpoints functional
- ✅ Automatic HTTPS
- ✅ Automatic deployments from GitHub
- ✅ Health checks
- ✅ 99.9% uptime (when awake)
- ✅ Global CDN
- ✅ Environment variables
- ✅ Logs and metrics

---

## Troubleshooting

### Build Fails

**Error:** `Failed to install requirements`

**Solution:**
Check that `requirements.txt` is in root directory:
```bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### Service Won't Start

**Error:** `Service exited with code 1`

**Solution:**
Check logs in Render dashboard. Common issues:
- Port binding: Ensure using `$PORT` environment variable
- Missing dependencies: Check requirements.txt
- Import errors: Check all files are committed

### Slow First Request

**This is normal!** Free tier sleeps after 15 minutes. Solutions:

1. **Accept it:** First request ~30s, then fast
2. **Keep-alive ping:** Use external service like UptimeRobot (free) to ping every 5 minutes
3. **Upgrade to paid:** Starter plan ($7/mo) never sleeps

---

## Keeping Service Awake (Optional)

### Option 1: UptimeRobot (Free)

1. Sign up at https://uptimerobot.com
2. Add New Monitor:
   - Type: HTTP(s)
   - URL: `https://pyjhora-api.onrender.com/health`
   - Interval: 5 minutes
3. Service will stay awake during monitoring

### Option 2: GitHub Actions (Free)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping API
        run: curl https://pyjhora-api.onrender.com/health
```

---

## Updating Your API

After making changes locally:

```bash
# Add changes
git add .

# Commit
git commit -m "Your change description"

# Push to GitHub
git push

# Render auto-deploys within 1-2 minutes
```

---

## Monitoring Your Service

### Render Dashboard

Access at: https://dashboard.render.com

**Available Metrics:**
- Request count
- Response times
- Error rates
- Memory usage
- CPU usage
- Deployment history
- Logs (last 7 days on free tier)

### View Logs

```bash
# Using Render CLI (optional)
npm install -g render-cli
render login
render logs pyjhora-api
```

---

## Custom Domain (Paid Feature)

If you want a custom domain (requires paid plan):

1. Upgrade to Starter plan ($7/mo)
2. Go to Settings > Custom Domains
3. Add your domain
4. Update DNS records as shown
5. SSL certificate auto-generated

---

## Example Client Usage

Once deployed, update your client code:

```python
import requests

# Update base URL to your Render URL
BASE_URL = "https://pyjhora-api.onrender.com"

payload = {
    "birth_data": {
        "date": "1998-12-22",
        "time": "17:12:00",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone_offset": 5.5,
        "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
}

# Get comprehensive analysis
response = requests.post(
    f"{BASE_URL}/api/v1/comprehensive/full-analysis",
    json=payload
)

data = response.json()
print(data)
```

---

## Cost Considerations

### Free Tier (Current)
- **Cost:** $0/month
- **Hours:** 750/month shared across services
- **RAM:** 512 MB
- **Storage:** 1 GB
- **Bandwidth:** 100 GB/month
- **Sleep:** After 15 min inactivity
- **Support:** Community

### Starter Tier ($7/month)
- **Cost:** $7/month per service
- **RAM:** 512 MB
- **Never sleeps:** Always on
- **Custom domains:** Included
- **Support:** Email

### Standard Tier ($25/month)
- **Cost:** $25/month per service
- **RAM:** 2 GB
- **Auto-scaling:** Available
- **Priority support:** Included

**Recommendation:** Start with Free, upgrade if needed

---

## Security Best Practices

### 1. Environment Variables

Never commit sensitive data. Use Render environment variables:

```bash
# In Render Dashboard > Environment
API_KEY=your_secret_key
DATABASE_URL=your_db_url
```

### 2. Rate Limiting (Add if needed)

Install:
```bash
pip install slowapi
```

Add to `app/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/comprehensive/full-analysis")
@limiter.limit("10/minute")
async def get_full_analysis(request: Request, ...):
    ...
```

### 3. CORS Configuration

Already configured in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, restrict origins:
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

---

## Backup & Recovery

### Automatic Backups

Render automatically:
- Backs up your service configuration
- Stores deployment history (30 days)
- Maintains logs (7 days on free)

### Manual Backup

Your code is safe in GitHub:
```bash
# Clone anywhere
git clone https://github.com/YOUR_USERNAME/pyjhora-vedic-astrology-api.git

# Deploy to another service
# (Vercel, Railway, Fly.io, etc.)
```

---

## Alternative Free Hosting Options

If Render doesn't work, try:

1. **Railway.app**
   - Similar to Render
   - 500 hours/month free
   - $5 credit/month

2. **Fly.io**
   - 3 VMs free
   - 3GB persistent storage
   - 160GB bandwidth/month

3. **Vercel** (serverless)
   - Good for lightweight APIs
   - Fast cold starts
   - 100GB bandwidth/month

4. **Heroku** (limited free)
   - Used to be best free tier
   - Now limited features

---

## Support & Resources

**Render Documentation:**
- https://render.com/docs
- https://render.com/docs/free

**Community:**
- Render Community: https://community.render.com
- Discord: https://discord.gg/render

**Status:**
- https://status.render.com

---

## Summary Checklist

- [ ] Git repository initialized
- [ ] Code committed to Git
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created on Render
- [ ] Build command configured
- [ ] Start command configured
- [ ] Environment variables added
- [ ] Health check path set
- [ ] Deployment successful
- [ ] API tested and working
- [ ] Documentation accessible
- [ ] (Optional) UptimeRobot configured

---

**Your API will be live at:** `https://your-service-name.onrender.com`

**Deployment time:** 5-10 minutes

**Status:** Free forever (with limitations)

---

Good luck with your deployment! 🚀
