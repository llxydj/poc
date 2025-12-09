import requests
import time
import random
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anomaly.detector import load_model, score_event

HUB_URL = os.environ.get("HUB_URL", "http://localhost:5000/alerts")
SUC_ID = "SUC_B"

def simulate_event():
    try:
        # Simulate port scan events: feature vector derived from ports scanned and time
        ports_scanned = random.choice([1,1,1,2,3,5,10,15,20,30,50])  # sometimes large
        feature = [ports_scanned, random.random()]
        model = load_model()
        anomaly_score = score_event(feature, model)
        
        # Ensure anomaly_score is valid
        if anomaly_score is None or not (0 <= anomaly_score <= 1):
            anomaly_score = 0.5
        
        # 30% chance to send login_attempts to trigger coordination with SUC_A
        # This helps demonstrate coordinated attack detection
        if random.random() < 0.3:
            event_type = "login_attempts"
            attempts = random.choice([5, 6, 7, 8, 10, 12])
            payload = {
                "suc_id": SUC_ID,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event_type": event_type,
                "raw_details": {
                    "src_ip": f"192.168.1.{random.randint(2,254)}",
                    "username": f"user{random.randint(1,200)}",
                    "attempts": attempts
                },
                "anomaly_score": float(anomaly_score),
                "anomaly_label": "anomaly" if anomaly_score > 0.7 else "normal"
            }
        else:
            event_type = "port_scan"
            payload = {
                "suc_id": SUC_ID,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event_type": event_type,
                "raw_details": {
                    "src_ip": f"192.168.1.{random.randint(2,254)}",
                    "dst_port": random.randint(20, 65535),
                    "ports_scanned": ports_scanned
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
            "event_type": "port_scan",
            "raw_details": {"src_ip": "192.168.1.1", "dst_port": 80, "ports_scanned": 1},
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
            print(f"[{SUC_ID}] {status} Sent: {payload['event_type']} | score: {round(payload['anomaly_score'],2)} | ports: {payload['raw_details'].get('ports_scanned', 'N/A')} -> {r.status_code}")
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

