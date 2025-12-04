from datetime import datetime, timedelta
import sqlite3
import json

# Simple POC correlation:
# If another alert of same event_type from different SUC occurred within 2 minutes, mark as coordinated.

TIME_WINDOW_SECONDS = 120

def correlate_and_tag(db_path, alert_id):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT id, suc_id, timestamp, event_type, raw_masked, anomaly_score FROM alerts WHERE id=?", (alert_id,))
        row = c.fetchone()
        if not row:
            return "Unknown", "No record found"

        id_, suc_id, timestamp, event_type, raw_masked, anomaly_score = row
        
        # Validate required fields
        if not suc_id or not event_type:
            return "Medium", f"{event_type or 'Unknown event'} detected by {suc_id or 'unknown SUC'}"
        
        # parse timestamp (assuming ISO)
        try:
            ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            try:
                ts = datetime.fromisoformat(timestamp)
            except (ValueError, AttributeError):
                ts = datetime.utcnow()

        # find other recent alerts with same event_type
        c.execute("""
            SELECT id, suc_id, timestamp FROM alerts WHERE event_type=? AND id<>? ORDER BY id DESC
        """, (event_type, alert_id))
        others = c.fetchall()
        coordinated = False
        for o in others:
            if len(o) < 3:
                continue
            try:
                ots = datetime.fromisoformat(o[2].replace("Z", "+00:00"))
                if abs((ts - ots).total_seconds()) <= TIME_WINDOW_SECONDS and o[1] != suc_id:
                    coordinated = True
                    break
            except (ValueError, AttributeError):
                try:
                    ots = datetime.fromisoformat(o[2])
                    if abs((ts - ots).total_seconds()) <= TIME_WINDOW_SECONDS and o[1] != suc_id:
                        coordinated = True
                        break
                except (ValueError, AttributeError):
                    continue

        # severity logic (very simple)
        severity = "Medium"
        try:
            if anomaly_score is not None:
                score = float(anomaly_score)
                if score > 0.7:
                    severity = "High"
                elif score > 0.5:
                    severity = "Medium"
                else:
                    severity = "Low"
        except (ValueError, TypeError):
            severity = "Medium"

        if coordinated:
            severity = "High"
            summary = f"Coordinated {event_type} detected across schools"
        else:
            summary = f"{event_type} detected by {suc_id}"

        # Update the alert with severity and summary
        from storage import update_alert_severity
        update_alert_severity(db_path, alert_id, severity, summary)

        return severity, summary
    except Exception as e:
        print(f"Error in correlation: {e}")
        return "Medium", "Error processing alert"
    finally:
        if conn:
            conn.close()

