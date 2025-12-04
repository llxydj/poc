from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import threading
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from correlation import correlate_and_tag
from storage import init_db, insert_alert, get_alerts

# Use absolute path for database to avoid issues
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("BAYANI_DB", os.path.join(DB_DIR, "bayanihub.db"))

app = Flask(__name__)
CORS(app)

# initialize DB
init_db(DB_PATH)

@app.route("/alerts", methods=["POST"])
def receive_alert():
    try:
        data = request.get_json()
        if not data or "suc_id" not in data:
            return jsonify({"error": "malformed payload: missing suc_id"}), 400

        # Basic anonymization
        raw = data.get("raw_details", {})
        if not isinstance(raw, dict):
            raw = {}
        
        masked = {}
        # Example anonymization: mask IPs and usernames
        if "src_ip" in raw:
            ip = raw["src_ip"]
            masked["src_ip_masked"] = mask_ip(ip)
        if "username" in raw:
            masked["username_hash"] = hash_username(raw["username"])
        if "attempts" in raw:
            masked["attempts"] = raw["attempts"]
        if "dst_port" in raw:
            masked["dst_port"] = raw["dst_port"]
        if "ports_scanned" in raw:
            masked["ports_scanned"] = raw["ports_scanned"]

        # Validate and sanitize inputs
        suc_id = str(data["suc_id"])[:50]  # Limit length
        event_type = str(data.get("event_type", ""))[:50]
        timestamp = data.get("timestamp")
        if not timestamp:
            timestamp = datetime.utcnow().isoformat() + "Z"
        
        anomaly_score = data.get("anomaly_score")
        if anomaly_score is not None:
            try:
                anomaly_score = float(anomaly_score)
                # Clamp to valid range
                anomaly_score = max(0.0, min(1.0, anomaly_score))
            except (ValueError, TypeError):
                anomaly_score = None

        record = {
            "suc_id": suc_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "raw_masked": json.dumps(masked),
            "anomaly_score": anomaly_score
        }

        alert_id = insert_alert(DB_PATH, record)

        # run correlation (can be async/threaded in POC)
        severity, summary = correlate_and_tag(DB_PATH, alert_id)

        print(f"[HUB] Received alert #{alert_id} from {suc_id}: {event_type} (severity: {severity})")
        
        return jsonify({"status": "received", "id": alert_id, "severity": severity, "summary": summary}), 200
    except Exception as e:
        print(f"[HUB] Error processing alert: {e}")
        return jsonify({"error": "internal server error", "message": str(e)}), 500

@app.route("/alerts", methods=["GET"])
def list_alerts():
    try:
        alerts = get_alerts(DB_PATH)
        return jsonify(alerts)
    except Exception as e:
        print(f"[HUB] Error retrieving alerts: {e}")
        return jsonify({"error": "internal server error"}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "bayanihub-hub"}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    try:
        alerts = get_alerts(DB_PATH)
        total = len(alerts)
        high_severity = sum(1 for a in alerts if a.get("severity") == "High")
        medium_severity = sum(1 for a in alerts if a.get("severity") == "Medium")
        low_severity = sum(1 for a in alerts if a.get("severity") == "Low")
        
        suc_counts = {}
        event_type_counts = {}
        coordinated_count = 0
        
        for a in alerts:
            suc_id = a.get("suc_id", "unknown")
            suc_counts[suc_id] = suc_counts.get(suc_id, 0) + 1
            
            event_type = a.get("event_type", "unknown")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            summary = a.get("summary", "")
            if summary and "coordinated" in str(summary).lower():
                coordinated_count += 1
        
        return jsonify({
            "total_alerts": total,
            "by_severity": {
                "high": high_severity,
                "medium": medium_severity,
                "low": low_severity
            },
            "by_suc": suc_counts,
            "by_event_type": event_type_counts,
            "coordinated_attacks": coordinated_count
        })
    except Exception as e:
        print(f"[HUB] Error calculating metrics: {e}")
        return jsonify({"error": "internal server error"}), 500

def mask_ip(ip):
    # naive mask: replace last octet
    try:
        if not ip or not isinstance(ip, str):
            return "masked"
        parts = ip.split(".")
        if len(parts) == 4:
            parts[-1] = "xxx"
            return ".".join(parts)
    except (AttributeError, ValueError):
        pass
    return "masked"

def hash_username(u):
    # simple deterministic hash for demo (not secure)
    return str(abs(hash(u)) % 1000000)

if __name__ == "__main__":
    print(f"[HUB] Starting BAYANIHUB Hub on http://0.0.0.0:5000")
    print(f"[HUB] Database: {DB_PATH}")
    app.run(host="0.0.0.0", port=5000, debug=True)

