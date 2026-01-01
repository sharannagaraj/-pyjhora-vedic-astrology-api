# 🚀 Quick Deploy to Render - 3 Steps

## Before You Start

✅ All code is committed to Git
✅ Ready to deploy to Render for FREE

---

## Step 1: Push to GitHub (2 minutes)

### If you don't have a GitHub repo yet:

1. **Go to GitHub:** https://github.com/new
2. **Create repository:**
   - Name: `pyjhora-vedic-astrology-api`
   - Make it **PUBLIC** (required for free tier)
   - **Don't** initialize with README
   - Click "Create repository"

3. **Push your code:**
```bash
cd "H:\claude code\pyjhora-api"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pyjhora-vedic-astrology-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render (5 minutes)

1. **Sign up:** https://render.com (use GitHub login)

2. **Create Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Click **"Connect account"** (if first time)
   - Find your repo: `pyjhora-vedic-astrology-api`
   - Click **"Connect"**

3. **Configure** (auto-filled from render.yaml):
   - Name: `pyjhora-api` (or choose yours)
   - Region: Choose closest (Oregon/Frankfurt/Singapore)
   - Plan: **FREE**
   - Click **"Create Web Service"**

4. **Wait for deployment** (5-10 minutes)
   - Watch the build logs
   - Wait for "Deploy succeeded" ✅

---

## Step 3: Test Your API (1 minute)

Your API is now live at: `https://pyjhora-api.onrender.com`

### Test it:

```bash
# Health check
curl https://pyjhora-api.onrender.com/health

# API info
curl https://pyjhora-api.onrender.com/

# Open docs in browser
# https://pyjhora-api.onrender.com/docs
```

### Test comprehensive endpoint:

```bash
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

---

## ✅ You're Done!

Your PyJHora API is now:
- ✅ **Live on the internet**
- ✅ **Free forever** (with limitations)
- ✅ **HTTPS secured**
- ✅ **Globally accessible**

**Share your API:**
- Base URL: `https://pyjhora-api.onrender.com`
- Docs: `https://pyjhora-api.onrender.com/docs`

---

## 📌 Important: Free Tier Behavior

### Service Sleeps After 15 Minutes
- **First request** after sleep: ~30 seconds (waking up)
- **Subsequent requests**: Fast (<1 second)

### Keep It Awake (Optional)
Use **UptimeRobot** (free):
1. Sign up: https://uptimerobot.com
2. Add monitor: `https://pyjhora-api.onrender.com/health`
3. Interval: 5 minutes
4. Done! Service stays awake

---

## 🔄 Auto-Deploy

Any time you push to GitHub, Render auto-deploys:

```bash
# Make changes
# Edit files...

# Commit and push
git add .
git commit -m "Update API"
git push

# Render deploys in 2-3 minutes automatically! ✅
```

---

## 📊 Monitor Your API

**Render Dashboard:** https://dashboard.render.com

View:
- Real-time logs
- Request metrics
- Memory usage
- Deployment history

---

## 💡 Pro Tips

1. **Bookmark your API docs:** `https://pyjhora-api.onrender.com/docs`
2. **Check logs regularly** in Render dashboard
3. **Use UptimeRobot** to keep service awake
4. **Test locally first** before pushing to GitHub

---

## 🐛 Troubleshooting

### Build Failed?
- Check logs in Render dashboard
- Verify `requirements.txt` is present
- Check Python version (3.11)

### Service Won't Start?
- Check start command uses `$PORT`
- Verify all files committed to Git
- Review logs for errors

### Slow First Request?
- Normal for free tier (service sleeps)
- Use UptimeRobot to keep awake
- Or upgrade to paid plan ($7/mo)

---

## 📞 Need Help?

**Detailed Guides:**
- [DEPLOY_TO_RENDER.md](DEPLOY_TO_RENDER.md) - Full deployment guide
- [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) - Complete documentation

**Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com

---

**Total Time:** 8-10 minutes
**Cost:** $0/month (free forever)
**Difficulty:** Easy

Good luck! 🎉
