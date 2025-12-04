import sqlite3
from sqlite3 import Connection
import json

def init_db(db_path="bayanihub.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suc_id TEXT,
            timestamp TEXT,
            event_type TEXT,
            raw_masked TEXT,
            anomaly_score REAL,
            severity TEXT,
            summary TEXT
        );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        if conn:
            conn.close()

def insert_alert(db_path, record):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO alerts (suc_id, timestamp, event_type, raw_masked, anomaly_score, severity, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (record["suc_id"], record["timestamp"], record["event_type"], record["raw_masked"], 
              record["anomaly_score"], record.get("severity", "Medium"), record.get("summary", "")))
        conn.commit()
        alert_id = c.lastrowid
        return alert_id
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error inserting alert: {e}")
        raise
    finally:
        if conn:
            conn.close()

def update_alert_severity(db_path, alert_id, severity, summary):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            UPDATE alerts SET severity=?, summary=? WHERE id=?
        """, (severity, summary, alert_id))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error updating alert severity: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_alerts(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT id, suc_id, timestamp, event_type, raw_masked, anomaly_score, severity, summary FROM alerts ORDER BY id DESC")
        rows = c.fetchall()
        results = []
        for r in rows:
            # Validate row has expected number of columns
            if len(r) < 8:
                continue
                
            # Safely parse JSON
            raw_masked = {}
            if r[4]:
                try:
                    raw_masked = json.loads(r[4])
                except (json.JSONDecodeError, TypeError):
                    raw_masked = {}
            
            results.append({
                "id": r[0],
                "suc_id": r[1] or "unknown",
                "timestamp": r[2] or "",
                "event_type": r[3] or "unknown",
                "raw_masked": raw_masked,
                "anomaly_score": r[5] if r[5] is not None else None,
                "severity": r[6] or "Medium",
                "summary": r[7] or ""
            })
        return results
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return []
    finally:
        if conn:
            conn.close()

