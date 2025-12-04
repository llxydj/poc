# BAYANIHUB POC - Complete Implementation

A proof-of-concept implementation of BAYANIHUB: a centralized security alert coordination system for State Universities and Colleges (SUCs).

## 🎯 What This POC Demonstrates

- **Distributed Detection**: Two simulated SUCs detect anomalies locally using ML
- **Centralized Coordination**: A Flask hub receives, stores, and correlates alerts
- **Professional Dashboard**: Beautiful, intuitive Streamlit dashboard with real-time visualizations
- **Real-time Visualization**: Interactive charts, metrics, and alert tables
- **Anonymization**: Basic privacy protection through data masking
- **Correlation**: Detects coordinated attacks across multiple SUCs
- **Advanced UI/UX**: Color-coded severity, filters, search, and detailed views

## 📋 Prerequisites

- Python 3.8+ (3.10+ recommended)
- pip package manager
- 4 terminal windows (or use background processes)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Start the Hub (Terminal 1)

```bash
cd hub
python app.py
```

You should see:
```
[HUB] Starting BAYANIHUB Hub on http://0.0.0.0:5000
[HUB] Database: bayanihub.db
```

### 3. Start the Dashboard (Terminal 2)

```bash
cd dashboard
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### 4. Start SUC Simulator A (Terminal 3)

```bash
python suc_simulators/suc_a.py
```

### 5. Start SUC Simulator B (Terminal 4)

```bash
python suc_simulators/suc_b.py
```

## 📊 What You'll See

1. **Hub Terminal**: Shows incoming alerts with severity levels
2. **Dashboard**: Real-time visualization of alerts, metrics, and charts
3. **SUC Terminals**: Show alerts being sent to the hub

## 🔍 Testing Coordinated Attack Detection

To test the correlation engine:

1. Wait for both SUCs to send alerts
2. Watch for alerts with the same `event_type` from different SUCs within 2 minutes
3. The hub will mark these as "Coordinated" with High severity
4. The dashboard will show these in the alerts table

## 📁 Project Structure

```
bayanihub-poc/
├── hub/
│   ├── app.py              # Flask API server
│   ├── storage.py          # SQLite database operations
│   ├── correlation.py      # Alert correlation engine
│   ├── requirements.txt    # Hub dependencies
│   └── README.md
├── suc_simulators/
│   ├── suc_a.py           # SUC A simulator
│   └── suc_b.py           # SUC B simulator
├── anomaly/
│   └── detector.py        # ML anomaly detection
├── dashboard/
│   ├── dashboard.py       # Streamlit dashboard
│   └── requirements.txt   # Dashboard dependencies
├── requirements.txt       # All dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

- `HUB_URL`: Hub endpoint (default: `http://localhost:5000/alerts`)
- `BAYANI_DB`: Database path (default: `bayanihub.db`)
- `BAYANI_MODEL`: ML model file path (default: `if_model.joblib`)

Example:
```bash
# Windows
set HUB_URL=http://localhost:5000/alerts
python suc_simulators/suc_a.py

# Mac/Linux
export HUB_URL=http://localhost:5000/alerts
python suc_simulators/suc_a.py
```

## 📡 API Endpoints

### POST /alerts
Send an alert to the hub.

**Request:**
```json
{
  "suc_id": "SUC_A",
  "timestamp": "2025-12-04T09:35:21Z",
  "event_type": "login_attempts",
  "raw_details": {
    "src_ip": "10.0.0.5",
    "username": "student01",
    "attempts": 7
  },
  "anomaly_score": 0.87,
  "anomaly_label": "anomaly"
}
```

**Response:**
```json
{
  "status": "received",
  "id": 1,
  "severity": "High",
  "summary": "login_attempts detected by SUC_A"
}
```

### GET /alerts
Retrieve all alerts.

**Response:**
```json
[
  {
    "id": 1,
    "suc_id": "SUC_A",
    "timestamp": "2025-12-04T09:35:21Z",
    "event_type": "login_attempts",
    "severity": "High",
    "summary": "Coordinated login_attempts detected across schools",
    "anomaly_score": 0.87,
    "raw_masked": {
      "src_ip_masked": "10.0.0.xxx",
      "username_hash": "123456"
    }
  }
]
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "bayanihub-hub"
}
```

### GET /metrics
Get comprehensive summary statistics.

**Response:**
```json
{
  "total_alerts": 25,
  "by_severity": {
    "high": 5,
    "medium": 12,
    "low": 8
  },
  "by_suc": {
    "SUC_A": 15,
    "SUC_B": 10
  },
  "by_event_type": {
    "login_attempts": 18,
    "port_scan": 7
  },
  "coordinated_attacks": 2
}
```

## 🛑 Stopping the System

Press `Ctrl+C` in each terminal to stop:
1. Stop SUC simulators (Terminals 3 & 4)
2. Stop dashboard (Terminal 2) - press `Ctrl+C` in terminal
3. Stop hub (Terminal 1)

## 🔒 Privacy & Security Notes

**⚠️ IMPORTANT**: This is a POC for demonstration only.

- Uses synthetic/simulated data only
- Basic anonymization (not production-ready)
- No authentication or encryption
- Not suitable for production use

For production:
- Implement strong encryption (TLS/HTTPS)
- Add authentication and authorization
- Use secure hashing with salt
- Implement proper data governance
- Add audit logging

## 🧪 Testing the System

Run the test script to verify everything is working:

```bash
# Make sure hub is running first
python test_system.py
```

This will test:
- Hub health check
- Alert submission
- Alert retrieval
- Metrics endpoint

## 🐛 Troubleshooting

### Hub won't start
- Check if port 5000 is already in use
- Verify Flask is installed: `pip install Flask flask-cors`
- Check for database file permissions

### SUCs can't connect
- Ensure hub is running first
- Check `HUB_URL` environment variable
- Verify network connectivity
- Check hub terminal for error messages

### Dashboard shows no data
- Verify hub is running and receiving alerts
- Check browser console for errors
- Ensure SUC simulators are running
- Check connection status in sidebar (should show "🟢 Hub: Online")
- Try refreshing the page

### Import errors
- Make sure you're in the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path includes project root
- Ensure plotly is installed: `pip install plotly`

### Charts not displaying
- Verify plotly is installed: `pip install plotly==5.18.0`
- Check browser console for JavaScript errors
- Try clearing browser cache

## 📝 Demo Script

See `demo_script.md` for a step-by-step demonstration guide.

## 🎓 Mapping to Full BAYANIHUB Vision

This POC demonstrates:
- **Local Detection**: SUCs run anomaly detection locally
- **Anonymized Sharing**: Alerts are anonymized before transmission
- **Central Correlation**: Hub identifies coordinated threats
- **Visualization**: Dashboard provides situational awareness

Full system would add:
- Federated learning for model updates
- Secure communication channels (mTLS)
- Advanced correlation algorithms
- Incident response workflows
- Policy recommendation engine

## 📄 License

This is a proof-of-concept for educational/demonstration purposes.

## 🤝 Support

For issues or questions, refer to the documentation in each module's README.

