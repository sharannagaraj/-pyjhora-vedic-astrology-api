# Deployment Guide - PyJHora API

Complete guide for deploying PyJHora API to Railway or Render free tier.

## Option 1: Deploy to Railway (Recommended)

### Why Railway?
- ✅ 500 hours/month free tier
- ✅ Auto-deploy from GitHub
- ✅ Easy environment setup
- ✅ Good performance

### Steps:

1. **Prepare Git Repository**
```bash
cd pyjhora-api
git init
git add .
git commit -m "Initial commit - PyJHora API"
```

2. **Push to GitHub**
```bash
# Create a new repository on GitHub
git remote add origin https://github.com/YOUR_USERNAME/pyjhora-api.git
git branch -M main
git push -u origin main
```

3. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Authorize GitHub and select `pyjhora-api` repository
   - Railway will auto-detect the `railway.json` configuration
   - Click "Deploy"

4. **Get Your URL**
   - After deployment, click "Settings" → "Domains"
   - Click "Generate Domain"
   - Your API will be live at: `https://your-app.up.railway.app`

### Environment Variables (Optional)
Railway will automatically set `PORT`. No other variables needed.

---

## Option 2: Deploy to Render

### Why Render?
- ✅ Truly free tier (no time limit)
- ✅ Auto-deploy from GitHub
- ✅ Automatic HTTPS

### Steps:

1. **Prepare Git Repository** (same as Railway step 1-2)

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `pyjhora-api` repository
   - Render will auto-detect `render.yaml`
   - Click "Create Web Service"

3. **Configure (Auto-detected from render.yaml)**
   - **Name**: pyjhora-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Plan**: Free

4. **Get Your URL**
   - Your API will be live at: `https://pyjhora-api.onrender.com`

### Note on Free Tier
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Subsequent requests are fast

---

## Option 3: Deploy with Docker (Any Platform)

### Using Docker Locally

```bash
# Build
docker build -t pyjhora-api .

# Run
docker run -p 8000:8000 pyjhora-api

# Test
curl http://localhost:8000/health
```

### Deploy to Docker Hub

```bash
# Login
docker login

# Tag
docker tag pyjhora-api YOUR_USERNAME/pyjhora-api:latest

# Push
docker push YOUR_USERNAME/pyjhora-api:latest
```

### Deploy to Cloud Run (Google Cloud)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Deploy
gcloud run deploy pyjhora-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --platform managed
```

---

## Testing Your Deployed API

### Test Health Endpoint

```bash
# Railway
curl https://your-app.up.railway.app/health

# Render
curl https://pyjhora-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "pyjhora-api"
}
```

### Test D1 Chart Endpoint

```bash
curl -X POST "https://your-app.up.railway.app/api/v1/charts/rasi" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1998-12-22",
      "time": "17:12:00",
      "timezone_offset": 5.5,
      "latitude": 12.9716,
      "longitude": 77.5946,
      "place_name": "Bangalore, India"
    },
    "ayanamsa": "LAHIRI"
  }'
```

### Access API Documentation

Visit: `https://your-app.up.railway.app/docs`

You'll see interactive Swagger UI documentation where you can:
- See all endpoints
- Test API calls directly
- See request/response schemas

---

## Performance Optimization

### Railway (Paid Plan)
If you need better performance:
- Upgrade to Hobby plan ($5/month)
- Increase to 2-4 workers

### Render (Paid Plan)
- Upgrade to Starter plan ($7/month)
- Guaranteed uptime, no spin-down

### Caching (Future Enhancement)
Add Redis caching for frequently requested charts:

```python
# In requirements.txt
redis==5.0.1

# Add caching middleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

---

## Monitoring & Logs

### Railway
- Click your project → "Observability"
- View logs, metrics, and deployments
- Set up alerts

### Render
- Go to your service → "Logs"
- View real-time logs
- Monitor resource usage

---

## Custom Domain (Optional)

### Railway
1. Go to Settings → Domains
2. Click "Custom Domain"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS with provided CNAME

### Render
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS with provided values

---

## Security Considerations

### API Rate Limiting
Add rate limiting to prevent abuse:

```python
# requirements.txt
slowapi==0.1.9

# In app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
@limiter.limit("100/hour")
async def root(request: Request):
    ...
```

### API Authentication (Optional)
For production, consider adding API key authentication:

```python
from fastapi.security.api_key import APIKeyHeader

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
```

---

## Cost Estimates

### Free Tier Limits

| Platform | Free Tier | Limitations |
|----------|-----------|-------------|
| **Railway** | 500 hours/month | ~$5 credit/month, sleeps after 1hr inactivity |
| **Render** | Unlimited | Spins down after 15min, slower cold start |
| **Google Cloud Run** | 2M requests/month | Pay per request after free tier |

### When to Upgrade

- **< 1000 requests/day**: Free tier is fine
- **1000-10,000 requests/day**: Consider Railway Hobby ($5/mo)
- **10,000+ requests/day**: Consider Render Starter ($7/mo) or Cloud Run

---

## Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError: No module named 'jhora'`

**Solution**: Ensure `requirements.txt` includes `PyJHora==4.5.5`

---

**Error**: `gcc not found` during pyswisseph installation

**Solution**: Already handled in Dockerfile with `apt-get install gcc g++`

---

### API Returns 500 Error

**Error**: Ephemeris files not found

**Solution**: PyJHora includes ephemeris data by default. Check logs for specific error.

---

### Slow Response Times

**Solution**:
- Increase worker count in start command
- Add caching for repeated calculations
- Upgrade to paid tier for better resources

---

## Next Steps

After deployment:
1. ✅ Test all endpoints via `/docs`
2. ✅ Monitor logs for errors
3. ✅ Set up custom domain (optional)
4. ✅ Add rate limiting for production
5. ✅ Implement caching for performance

---

## Support

- API Docs: `https://your-api-url.com/docs`
- Railway Support: [railway.app/help](https://railway.app/help)
- Render Support: [render.com/docs](https://render.com/docs)

---

**Your PyJHora API is now ready for production!** 🚀
