# BAYANIHUB POC - FREE Deployment Guide

## 🎯 Best FREE Option: **Render.com**

**Why Render is the best choice:**
- ✅ **100% FREE tier** (with limitations)
- ✅ Supports Flask (Hub API)
- ✅ Supports Streamlit (Dashboard)
- ✅ FREE PostgreSQL database
- ✅ Easy GitHub integration
- ✅ Auto-deploy on push
- ✅ No credit card required for free tier

**Free Tier Limits:**
- Services spin down after 15 minutes of inactivity (wake up on first request)
- 750 hours/month free (enough for 24/7 if you use it)
- 512MB RAM per service
- Free PostgreSQL database (90 days, then $7/month or you can use SQLite)

---

## 🚀 Deployment Steps

### Prerequisites

1. **GitHub Account** (free)
2. **Render Account** (free signup at render.com)
3. **Your code pushed to GitHub**

### Step 1: Prepare Your Code for Deployment

#### 1.1 Update Database to Support PostgreSQL (Optional but Recommended)

The code already supports SQLite, but for production, PostgreSQL is better. However, **you can keep SQLite for free tier** - Render supports it!

#### 1.2 Create Required Files

I'll create these files for you in the next steps.

---

### Step 2: Deploy Hub API

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name**: `bayanihub-hub`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd hub && python app.py`
   - **Root Directory**: Leave empty (or set to project root)

5. **Environment Variables:**
   ```
   BAYANI_DB=hub/bayanihub.db
   PORT=5000
   ```

6. **Click "Create Web Service"**

**Your Hub will be available at**: `https://bayanihub-hub.onrender.com`

---

### Step 3: Deploy Dashboard

1. **Go to Render Dashboard**
2. **Click "New +" → "Web Service"**
3. **Connect same GitHub repository**
4. **Configure:**
   - **Name**: `bayanihub-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run dashboard/dashboard.py --server.port $PORT --server.address 0.0.0.0`
   - **Root Directory**: Leave empty

5. **Environment Variables:**
   ```
   HUB_URL=https://bayanihub-hub.onrender.com/alerts
   PORT=8501
   ```

6. **Click "Create Web Service"**

**Your Dashboard will be available at**: `https://bayanihub-dashboard.onrender.com`

---

### Step 4: Deploy SUC Simulators (Optional - Can Run Locally)

For SUC simulators, you have two options:

#### Option A: Run Locally (Recommended for Free)
- Keep simulators running on your local machine
- Point them to your deployed hub URL

#### Option B: Deploy as Background Workers (Advanced)
- Create background worker services on Render
- More complex, may require paid tier

**For demo purposes, Option A is best!**

---

## 📝 Files Needed for Deployment

I'll create these files for you:

1. `render.yaml` - Render configuration (optional, makes deployment easier)
2. `.renderignore` - Files to ignore during deployment
3. `Procfile` - Process definitions (if needed)

---

## 🔧 Configuration Updates Needed

### Update Hub to Use Environment Port

Render provides a `PORT` environment variable. We need to update the hub to use it.

### Update Dashboard to Use Deployed Hub URL

Dashboard needs to know the deployed hub URL.

---

## 💰 Cost Breakdown

**FREE Option (Render Free Tier):**
- Hub API: FREE
- Dashboard: FREE
- Database: FREE (SQLite) or $7/month (PostgreSQL after 90 days)
- **Total: $0/month** (or $7/month if you want PostgreSQL)

**Limitations:**
- Services spin down after 15 min inactivity (wake on first request)
- 750 hours/month free (enough for 24/7)
- 512MB RAM per service

---

## 🎯 Alternative FREE Options

### Option 2: Railway (Limited Free Tier)
- ✅ $5 free credit/month
- ✅ Easy deployment
- ⚠️ Credit expires, then pay-as-you-go
- **Best for**: Short-term demos

### Option 3: Fly.io (Free Tier)
- ✅ Free tier available
- ✅ Good for Docker deployments
- ⚠️ More complex setup
- **Best for**: Docker-savvy users

### Option 4: PythonAnywhere (Free Tier)
- ✅ Free tier for Python apps
- ✅ Supports Flask and Streamlit
- ⚠️ Limited resources
- **Best for**: Simple demos

---

## ✅ Recommendation

**Use Render.com** - It's the best free option that:
- Supports all your components
- Has a generous free tier
- Easy to set up
- No credit card required
- Auto-deploys from GitHub

---

## 🚨 Important Notes

1. **Free tier services spin down** after 15 min inactivity
   - First request after spin-down takes ~30 seconds (cold start)
   - Subsequent requests are fast

2. **Database persistence**
   - SQLite files persist on Render
   - For production, consider PostgreSQL (free for 90 days)

3. **SUC Simulators**
   - Best to run locally pointing to deployed hub
   - Or use scheduled jobs (more complex)

4. **Environment Variables**
   - Update `HUB_URL` in dashboard to point to deployed hub
   - Update simulators to use deployed hub URL

---

## 📋 Quick Start Checklist

- [ ] Push code to GitHub
- [ ] Sign up for Render (free)
- [ ] Deploy Hub API
- [ ] Deploy Dashboard
- [ ] Update environment variables
- [ ] Test deployment
- [ ] Run SUC simulators locally (pointing to deployed hub)

---

**Ready to deploy? I'll create the necessary configuration files next!**

