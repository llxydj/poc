# BAYANIHUB POC - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies (One Time)

```bash
pip install -r requirements.txt
```

### 2. Start All Components

Open **4 separate terminals** and run:

**Terminal 1 - Hub:**
```bash
cd hub
python app.py
```

**Terminal 2 - Dashboard:**
```bash
cd dashboard
streamlit run dashboard.py
```

**Terminal 3 - SUC A:**
```bash
python suc_simulators/suc_a.py
```

**Terminal 4 - SUC B:**
```bash
python suc_simulators/suc_b.py
```

### 3. View the Dashboard

Open your browser to: `http://localhost:8501`

You should see:
- Real-time alerts appearing
- Metrics updating
- Charts showing alert distribution

## ✅ What to Expect

1. **Hub Terminal**: Shows incoming alerts with severity levels
2. **Dashboard**: Updates every 3 seconds with new alerts
3. **SUC Terminals**: Show alerts being sent every 5-10 seconds

## 🎯 Testing Coordinated Attacks

Wait 2-3 minutes and watch for:
- Alerts marked as "Coordinated" in the summary
- High severity alerts
- Same event_type from different SUCs within 2 minutes

## 🛑 Stopping

Press `Ctrl+C` in each terminal to stop all components.

## 📝 Notes

- **No API keys needed** - everything runs locally
- **No configuration required** - uses sensible defaults
- **Database created automatically** - `hub/bayanihub.db`
- **ML model created automatically** - `if_model.joblib`

## 🐛 Troubleshooting

**Hub won't start?**
- Check port 5000 is free
- Verify Flask is installed: `pip install Flask flask-cors`

**Dashboard shows no data?**
- Make sure hub is running first
- Check browser console for errors

**SUCs can't connect?**
- Verify hub is running
- Check `HUB_URL` environment variable (default: `http://localhost:5000/alerts`)

## 📚 More Information

- See `README.md` for detailed documentation
- See `SETUP.md` for configuration options
- See `demo_script.md` for presentation guide

