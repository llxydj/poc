import requests
import time
import random
import uuid
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anomaly.detector import load_model, score_event

HUB_URL = os.environ.get("HUB_URL", "http://localhost:5000/alerts")
SUC_ID = "SUC_A"

def simulate_event():
    try:
        # Example: simulate login attempts: feature vector derived from attempts and time
        attempts = random.choice([1,1,1,2,3,4,5,6,8,10,12])  # sometimes large
        feature = [attempts, random.random()]
        model = load_model()
        anomaly_score = score_event(feature, model)
        
        # Ensure anomaly_score is valid
        if anomaly_score is None or not (0 <= anomaly_score <= 1):
            anomaly_score = 0.5
        
        payload = {
            "suc_id": SUC_ID,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "login_attempts",
            "raw_details": {
                "src_ip": f"10.0.0.{random.randint(2,254)}",
                "username": f"user{random.randint(1,200)}",
                "attempts": attempts
            },
            "anomaly_score": float(anomaly_score),
            "anomaly_label": "anomaly" if anomaly_score > 0.7 else "normal"
        }
        return payload
    except Exception as e:
        print(f"[{SUC_ID}] Error generating event: {e}")
        # Return a basic payload on error
        return {
            "suc_id": SUC_ID,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "login_attempts",
            "raw_details": {"src_ip": "10.0.0.1", "username": "user1", "attempts": 1},
            "anomaly_score": 0.5,
            "anomaly_label": "normal"
        }

def main_loop():
    print(f"[{SUC_ID}] Starting simulator, sending alerts to {HUB_URL}")
    print(f"[{SUC_ID}] Press Ctrl+C to stop")
    while True:
        payload = simulate_event()
        try:
            r = requests.post(HUB_URL, json=payload, timeout=3)
            status = "✓" if r.status_code == 200 else "✗"
            print(f"[{SUC_ID}] {status} Sent: {payload['event_type']} | score: {round(payload['anomaly_score'],2)} | attempts: {payload['raw_details']['attempts']} -> {r.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[{SUC_ID}] ✗ Connection error - is the hub running?")
        except Exception as e:
            print(f"[{SUC_ID}] ✗ Error sending: {e}")
        time.sleep(5 + random.random()*5)  # send every 5-10s

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f"\n[{SUC_ID}] Stopped")

