# BAYANIHUB Central Hub

The central coordination hub that receives, stores, and correlates alerts from SUCs.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The hub will start on `http://localhost:5000`

## API Endpoints

- `POST /alerts` - Receive alert from SUC
- `GET /alerts` - List all alerts
- `GET /health` - Health check
- `GET /metrics` - Summary statistics

## Configuration

Set environment variable `BAYANI_DB` to change database path (default: `bayanihub.db`)

