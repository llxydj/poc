#!/usr/bin/env python3
"""
Quick test script to verify BAYANIHUB POC is working correctly.
Run this after starting the hub to test the system.
"""

import requests
import time
import json
from datetime import datetime

HUB_URL = "http://localhost:5000"

def test_health():
    """Test hub health endpoint"""
    print("Testing hub health...")
    try:
        r = requests.get(f"{HUB_URL}/health", timeout=2)
        if r.status_code == 200:
            print("✓ Hub is healthy")
            return True
        else:
            print(f"✗ Hub returned status {r.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to hub: {e}")
        print("  Make sure the hub is running: cd hub && python app.py")
        return False

def test_post_alert():
    """Test posting an alert"""
    print("\nTesting alert submission...")
    payload = {
        "suc_id": "TEST_SUC",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "test_event",
        "raw_details": {
            "src_ip": "10.0.0.100",
            "username": "testuser",
            "attempts": 5
        },
        "anomaly_score": 0.85,
        "anomaly_label": "anomaly"
    }
    
    try:
        r = requests.post(f"{HUB_URL}/alerts", json=payload, timeout=2)
        if r.status_code == 200:
            response = r.json()
            print(f"✓ Alert submitted successfully (ID: {response.get('id')})")
            print(f"  Severity: {response.get('severity')}")
            print(f"  Summary: {response.get('summary')}")
            return True
        else:
            print(f"✗ Alert submission failed: {r.status_code}")
            print(f"  Response: {r.text}")
            return False
    except Exception as e:
        print(f"✗ Error submitting alert: {e}")
        return False

def test_get_alerts():
    """Test getting alerts"""
    print("\nTesting alert retrieval...")
    try:
        r = requests.get(f"{HUB_URL}/alerts", timeout=2)
        if r.status_code == 200:
            alerts = r.json()
            print(f"✓ Retrieved {len(alerts)} alert(s)")
            if alerts:
                print(f"  Latest alert: ID {alerts[0].get('id')}, {alerts[0].get('event_type')}")
            return True
        else:
            print(f"✗ Failed to retrieve alerts: {r.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error retrieving alerts: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\nTesting metrics endpoint...")
    try:
        r = requests.get(f"{HUB_URL}/metrics", timeout=2)
        if r.status_code == 200:
            metrics = r.json()
            print("✓ Metrics retrieved successfully")
            print(f"  Total alerts: {metrics.get('total_alerts', 0)}")
            print(f"  High severity: {metrics.get('by_severity', {}).get('high', 0)}")
            print(f"  Medium severity: {metrics.get('by_severity', {}).get('medium', 0)}")
            print(f"  Low severity: {metrics.get('by_severity', {}).get('low', 0)}")
            return True
        else:
            print(f"✗ Failed to retrieve metrics: {r.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error retrieving metrics: {e}")
        return False

def main():
    print("=" * 50)
    print("BAYANIHUB POC System Test")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    if results[-1][1]:  # Only continue if health check passes
        results.append(("Post Alert", test_post_alert()))
        results.append(("Get Alerts", test_get_alerts()))
        results.append(("Metrics", test_metrics()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! System is working correctly.")
    else:
        print("✗ Some tests failed. Check the errors above.")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())

