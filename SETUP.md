# BAYANIHUB POC - Setup Guide

## Quick Setup (5 minutes)

### Step 1: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Required packages:**
- Flask 2.3.2
- flask-cors 3.0.10
- requests 2.31.0
- scikit-learn 1.3.2
- pandas 2.2.2
- streamlit 1.30.0
- joblib 1.3.2
- numpy 1.24.3

### Step 2: Verify Installation

```bash
python -c "import flask, streamlit, sklearn, pandas, requests; print('All packages installed successfully!')"
```

### Step 3: Run the System

See `README.md` for detailed run instructions.

## Configuration

### No API Keys Required

This POC does **NOT** require any API keys or external services. Everything runs locally.

### Environment Variables (Optional)

You can customize the following:

```bash
# Windows
set HUB_URL=http://localhost:5000/alerts
set BAYANI_DB=bayanihub.db
set BAYANI_MODEL=if_model.joblib

# Mac/Linux
export HUB_URL=http://localhost:5000/alerts
export BAYANI_DB=bayanihub.db
export BAYANI_MODEL=if_model.joblib
```

**Defaults:**
- `HUB_URL`: `http://localhost:5000/alerts`
- `BAYANI_DB`: `bayanihub.db` (created in hub/ directory)
- `BAYANI_MODEL`: `if_model.joblib` (created automatically on first run)

## Port Requirements

Make sure these ports are available:
- **5000**: Hub API server
- **8501**: Streamlit dashboard (default)

If ports are in use:
- Change hub port: Edit `hub/app.py`, change `port=5000` to another port
- Change dashboard port: `streamlit run dashboard.py --server.port 8502`

## Database

The SQLite database (`bayanihub.db`) is created automatically in the `hub/` directory on first run.

To reset the database:
1. Stop the hub
2. Delete `hub/bayanihub.db`
3. Restart the hub

## ML Model

The IsolationForest model (`if_model.joblib`) is created automatically on first run in the project root directory.

To retrain the model:
1. Delete `if_model.joblib`
2. Restart any SUC simulator (it will retrain automatically)

## Troubleshooting

### Import Errors

If you see import errors:
```bash
# Make sure you're in the project root
cd /path/to/bayanihub-poc

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Windows: Find process using port 5000
netstat -ano | findstr :5000

# Mac/Linux: Find process using port 5000
lsof -i :5000

# Kill the process or use a different port
```

### Database Locked

If you see "database is locked" errors:
- Make sure only one hub instance is running
- Close any database viewers
- Restart the hub

## System Requirements

- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 512MB minimum
- **Disk**: 100MB free space
- **OS**: Windows, Mac, or Linux

## Next Steps

After setup:
1. Read `README.md` for usage instructions
2. Review `demo_script.md` for demonstration guide
3. Start the system following the Quick Start guide

## Support

If you encounter issues:
1. Check all dependencies are installed
2. Verify Python version: `python --version`
3. Check port availability
4. Review error messages in terminal output

