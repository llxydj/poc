# 🚀 Step-by-Step Deployment Guide - Render.com (FREE)

## ✅ Best FREE Option: Render.com

**Why Render:**
- ✅ 100% FREE tier (no credit card needed)
- ✅ Supports Flask and Streamlit
- ✅ Free PostgreSQL (optional)
- ✅ Easy GitHub integration
- ✅ Auto-deploy on push

---

## 📋 Prerequisites

1. ✅ GitHub account (free)
2. ✅ Code pushed to GitHub repository
3. ✅ Render account (sign up at render.com - free)

---

## 🎯 Deployment Steps

### Step 1: Push Code to GitHub

```bash
# If you haven't already
git init
git add .
git commit -m "Initial commit - BAYANIHUB POC"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

### Step 2: Deploy Hub API

1. **Go to**: https://dashboard.render.com
2. **Click**: "New +" → "Web Service"
3. **Connect GitHub**: Authorize Render to access your repository
4. **Select Repository**: Choose your BAYANIHUB repository
5. **Configure Service**:
   - **Name**: `bayanihub-hub`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd hub && python app.py`

6. **Add Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - Add:
     ```
     BAYANI_DB = hub/bayanihub.db
     PORT = 5000
     FLASK_DEBUG = False
     ```

7. **Click**: "Create Web Service"

8. **Wait for deployment** (2-5 minutes)

9. **Copy your Hub URL**: `https://bayanihub-hub.onrender.com`

---

### Step 3: Deploy Dashboard

1. **In Render Dashboard**: Click "New +" → "Web Service"
2. **Select same repository**
3. **Configure Service**:
   - **Name**: `bayanihub-dashboard`
   - **Region**: Same as hub
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run dashboard/dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

4. **Add Environment Variables**:
   ```
   HUB_URL = https://bayanihub-hub.onrender.com/alerts
   PORT = 8501
   ```

5. **Click**: "Create Web Service"

6. **Wait for deployment** (2-5 minutes)

7. **Your Dashboard URL**: `https://bayanihub-dashboard.onrender.com`

---

### Step 4: Update SUC Simulators (Run Locally)

Update your local simulators to point to deployed hub:

**Windows:**
```bash
set HUB_URL=https://bayanihub-hub.onrender.com/alerts
python suc_simulators/suc_a.py
```

**Mac/Linux:**
```bash
export HUB_URL=https://bayanihub-hub.onrender.com/alerts
python suc_simulators/suc_a.py
```

Or create a `.env` file or update the scripts.

---

## 🔧 Testing Your Deployment

### Test Hub API:
```bash
# Health check
curl https://bayanihub-hub.onrender.com/health

# Should return: {"status":"healthy","service":"bayanihub-hub"}
```

### Test Dashboard:
- Open: `https://bayanihub-dashboard.onrender.com`
- Should show dashboard interface
- Check connection status (should show hub is online)

### Test Full Flow:
1. Start SUC simulators locally (pointing to deployed hub)
2. Watch alerts appear in dashboard
3. Verify correlation works

---

## ⚠️ Important Notes

### Free Tier Limitations:

1. **Cold Starts**: 
   - Services spin down after 15 min inactivity
   - First request takes ~30 seconds (wake up)
   - Subsequent requests are fast

2. **Resource Limits**:
   - 512MB RAM per service
   - 750 hours/month free (enough for 24/7)

3. **Database**:
   - SQLite works on Render (file persists)
   - For production, consider PostgreSQL (free 90 days, then $7/month)

### Tips:

- **Keep services warm**: Set up a monitoring service to ping your URLs every 10 minutes
- **Use environment variables**: Never hardcode URLs
- **Monitor logs**: Check Render dashboard for errors
- **Test locally first**: Make sure everything works before deploying

---

## 🐛 Troubleshooting

### Service won't start:
- Check build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Check start command is correct

### Dashboard can't connect to hub:
- Verify `HUB_URL` environment variable is correct
- Check hub is deployed and running
- Test hub URL directly in browser

### Database errors:
- SQLite should work, but if issues occur, consider PostgreSQL
- Check file permissions
- Verify database path is correct

### Port errors:
- Render provides `PORT` environment variable
- Make sure your code uses `os.environ.get("PORT", 5000)`
- Hub code is already updated to support this

---

## 📊 Cost Summary

**FREE Tier:**
- Hub API: $0/month
- Dashboard: $0/month  
- Database (SQLite): $0/month
- **Total: $0/month** ✅

**If you need PostgreSQL:**
- First 90 days: FREE
- After 90 days: $7/month
- **Total: $7/month** (optional)

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Hub API deployed and accessible
- [ ] Dashboard deployed and accessible
- [ ] Environment variables set correctly
- [ ] Hub health check works
- [ ] Dashboard connects to hub
- [ ] SUC simulators updated to use deployed hub
- [ ] Full system tested end-to-end

---

## 🎉 You're Done!

Your BAYANIHUB POC is now live on the internet for FREE!

**Hub URL**: `https://bayanihub-hub.onrender.com`  
**Dashboard URL**: `https://bayanihub-dashboard.onrender.com`

Share these URLs to demo your project!

---

## 🔄 Updating Your Deployment

Whenever you push to GitHub:
1. Render automatically detects changes
2. Rebuilds and redeploys
3. Your changes go live in 2-5 minutes

No manual steps needed!

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Render Support: Available in dashboard
- Check deployment logs in Render dashboard

**Good luck with your deployment!** 🚀

