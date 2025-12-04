#!/usr/bin/env python3
"""
Comprehensive QA Test Suite for BAYANIHUB POC
Tests all components end-to-end with edge cases
"""

import requests
import time
import json
import sys
import os
from datetime import datetime, timedelta

HUB_URL = "http://localhost:5000"
TEST_RESULTS = []

def log_test(test_name, passed, message=""):
    """Log test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    result = {
        "test": test_name,
        "passed": passed,
        "message": message
    }
    TEST_RESULTS.append(result)
    print(f"{status}: {test_name}")
    if message:
        print(f"  → {message}")

def test_hub_health():
    """Test 1: Hub health endpoint"""
    try:
        r = requests.get(f"{HUB_URL}/health", timeout=2)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "healthy":
                log_test("Hub Health Check", True)
                return True
            else:
                log_test("Hub Health Check", False, f"Unexpected status: {data.get('status')}")
                return False
        else:
            log_test("Hub Health Check", False, f"Status code: {r.status_code}")
            return False
    except Exception as e:
        log_test("Hub Health Check", False, f"Exception: {e}")
        return False

def test_post_valid_alert():
    """Test 2: Post valid alert"""
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
            data = r.json()
            if "id" in data and "severity" in data:
                log_test("Post Valid Alert", True, f"Alert ID: {data.get('id')}")
                return data.get("id")
            else:
                log_test("Post Valid Alert", False, "Missing fields in response")
                return None
        else:
            log_test("Post Valid Alert", False, f"Status code: {r.status_code}")
            return None
    except Exception as e:
        log_test("Post Valid Alert", False, f"Exception: {e}")
        return None

def test_post_invalid_alert():
    """Test 3: Post invalid alert (missing suc_id)"""
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "test_event"
    }
    
    try:
        r = requests.post(f"{HUB_URL}/alerts", json=payload, timeout=2)
        if r.status_code == 400:
            log_test("Post Invalid Alert (Validation)", True)
            return True
        else:
            log_test("Post Invalid Alert (Validation)", False, f"Expected 400, got {r.status_code}")
            return False
    except Exception as e:
        log_test("Post Invalid Alert (Validation)", False, f"Exception: {e}")
        return False

def test_post_alert_edge_cases():
    """Test 4: Post alerts with edge cases"""
    edge_cases = [
        {
            "name": "Null anomaly_score",
            "payload": {
                "suc_id": "TEST_SUC",
                "event_type": "test",
                "anomaly_score": None
            }
        },
        {
            "name": "Very high anomaly_score",
            "payload": {
                "suc_id": "TEST_SUC",
                "event_type": "test",
                "anomaly_score": 1.5  # Should be clamped
            }
        },
        {
            "name": "Negative anomaly_score",
            "payload": {
                "suc_id": "TEST_SUC",
                "event_type": "test",
                "anomaly_score": -0.5  # Should be clamped
            }
        },
        {
            "name": "Empty raw_details",
            "payload": {
                "suc_id": "TEST_SUC",
                "event_type": "test",
                "raw_details": {}
            }
        }
    ]
    
    passed = 0
    for case in edge_cases:
        try:
            r = requests.post(f"{HUB_URL}/alerts", json=case["payload"], timeout=2)
            if r.status_code == 200:
                passed += 1
            else:
                log_test(f"Edge Case: {case['name']}", False, f"Status: {r.status_code}")
        except Exception as e:
            log_test(f"Edge Case: {case['name']}", False, f"Exception: {e}")
    
    if passed == len(edge_cases):
        log_test("Post Alert Edge Cases", True, f"{passed}/{len(edge_cases)} passed")
        return True
    else:
        log_test("Post Alert Edge Cases", False, f"{passed}/{len(edge_cases)} passed")
        return False

def test_get_alerts():
    """Test 5: Get all alerts"""
    try:
        r = requests.get(f"{HUB_URL}/alerts", timeout=2)
        if r.status_code == 200:
            alerts = r.json()
            if isinstance(alerts, list):
                log_test("Get All Alerts", True, f"Retrieved {len(alerts)} alerts")
                return len(alerts) > 0
            else:
                log_test("Get All Alerts", False, "Response is not a list")
                return False
        else:
            log_test("Get All Alerts", False, f"Status code: {r.status_code}")
            return False
    except Exception as e:
        log_test("Get All Alerts", False, f"Exception: {e}")
        return False

def test_metrics_endpoint():
    """Test 6: Metrics endpoint"""
    try:
        r = requests.get(f"{HUB_URL}/metrics", timeout=2)
        if r.status_code == 200:
            metrics = r.json()
            required_fields = ["total_alerts", "by_severity", "by_suc", "by_event_type", "coordinated_attacks"]
            if all(field in metrics for field in required_fields):
                log_test("Metrics Endpoint", True, f"Total: {metrics.get('total_alerts')}")
                return True
            else:
                missing = [f for f in required_fields if f not in metrics]
                log_test("Metrics Endpoint", False, f"Missing fields: {missing}")
                return False
        else:
            log_test("Metrics Endpoint", False, f"Status code: {r.status_code}")
            return False
    except Exception as e:
        log_test("Metrics Endpoint", False, f"Exception: {e}")
        return False

def test_anonymization():
    """Test 7: Verify anonymization"""
    payload = {
        "suc_id": "TEST_SUC",
        "event_type": "test",
        "raw_details": {
            "src_ip": "192.168.1.100",
            "username": "sensitive_user"
        }
    }
    
    try:
        r = requests.post(f"{HUB_URL}/alerts", json=payload, timeout=2)
        if r.status_code == 200:
            # Get the alert back
            time.sleep(0.5)
            alerts_r = requests.get(f"{HUB_URL}/alerts", timeout=2)
            if alerts_r.status_code == 200:
                alerts = alerts_r.json()
                if alerts:
                    latest = alerts[0]
                    raw_masked = latest.get("raw_masked", {})
                    if "src_ip_masked" in raw_masked and "username_hash" in raw_masked:
                        if "192.168.1.100" not in str(raw_masked) and "sensitive_user" not in str(raw_masked):
                            log_test("Anonymization", True, "IP and username anonymized")
                            return True
                        else:
                            log_test("Anonymization", False, "Sensitive data not properly anonymized")
                            return False
                    else:
                        log_test("Anonymization", False, "Missing anonymized fields")
                        return False
        log_test("Anonymization", False, "Could not retrieve alert")
        return False
    except Exception as e:
        log_test("Anonymization", False, f"Exception: {e}")
        return False

def test_severity_assignment():
    """Test 8: Verify severity assignment"""
    test_cases = [
        {"score": 0.9, "expected": "High"},
        {"score": 0.6, "expected": "Medium"},
        {"score": 0.3, "expected": "Low"}
    ]
    
    passed = 0
    for case in test_cases:
        payload = {
            "suc_id": "TEST_SUC",
            "event_type": "test",
            "anomaly_score": case["score"]
        }
        try:
            r = requests.post(f"{HUB_URL}/alerts", json=payload, timeout=2)
            if r.status_code == 200:
                data = r.json()
                if data.get("severity") == case["expected"]:
                    passed += 1
                else:
                    log_test(f"Severity Assignment (score={case['score']})", False, 
                            f"Expected {case['expected']}, got {data.get('severity')}")
        except Exception as e:
            log_test(f"Severity Assignment (score={case['score']})", False, f"Exception: {e}")
    
    if passed == len(test_cases):
        log_test("Severity Assignment", True, f"{passed}/{len(test_cases)} passed")
        return True
    else:
        log_test("Severity Assignment", False, f"{passed}/{len(test_cases)} passed")
        return False

def test_coordinated_detection():
    """Test 9: Test coordinated attack detection"""
    # Send two alerts with same event_type from different SUCs within time window
    payload1 = {
        "suc_id": "SUC_A",
        "event_type": "coordinated_test",
        "anomaly_score": 0.5
    }
    
    payload2 = {
        "suc_id": "SUC_B",
        "event_type": "coordinated_test",
        "anomaly_score": 0.5
    }
    
    try:
        # Send first alert
        r1 = requests.post(f"{HUB_URL}/alerts", json=payload1, timeout=2)
        time.sleep(1)  # Wait 1 second
        # Send second alert
        r2 = requests.post(f"{HUB_URL}/alerts", json=payload2, timeout=2)
        
        if r1.status_code == 200 and r2.status_code == 200:
            time.sleep(0.5)
            # Check if coordinated
            alerts_r = requests.get(f"{HUB_URL}/alerts", timeout=2)
            if alerts_r.status_code == 200:
                alerts = alerts_r.json()
                coordinated = [a for a in alerts if "coordinated" in a.get("summary", "").lower()]
                if len(coordinated) > 0:
                    log_test("Coordinated Attack Detection", True, f"Detected {len(coordinated)} coordinated attack(s)")
                    return True
                else:
                    log_test("Coordinated Attack Detection", False, "Coordinated attack not detected")
                    return False
        log_test("Coordinated Attack Detection", False, "Could not send test alerts")
        return False
    except Exception as e:
        log_test("Coordinated Attack Detection", False, f"Exception: {e}")
        return False

def test_data_persistence():
    """Test 10: Verify data persistence"""
    # Send an alert, restart would be needed to fully test, but we can check it's stored
    payload = {
        "suc_id": "PERSISTENCE_TEST",
        "event_type": "persistence_test",
        "anomaly_score": 0.75
    }
    
    try:
        r = requests.post(f"{HUB_URL}/alerts", json=payload, timeout=2)
        if r.status_code == 200:
            alert_id = r.json().get("id")
            time.sleep(0.5)
            # Retrieve and verify
            alerts_r = requests.get(f"{HUB_URL}/alerts", timeout=2)
            if alerts_r.status_code == 200:
                alerts = alerts_r.json()
                found = [a for a in alerts if a.get("id") == alert_id]
                if found:
                    log_test("Data Persistence", True, f"Alert {alert_id} persisted")
                    return True
                else:
                    log_test("Data Persistence", False, "Alert not found after storage")
                    return False
        log_test("Data Persistence", False, "Could not create test alert")
        return False
    except Exception as e:
        log_test("Data Persistence", False, f"Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("BAYANIHUB POC - Comprehensive QA Test Suite")
    print("=" * 60)
    print()
    
    # Check if hub is running
    print("Checking hub connectivity...")
    try:
        requests.get(f"{HUB_URL}/health", timeout=1)
        print("✓ Hub is accessible\n")
    except:
        print("✗ Hub is not accessible. Please start the hub first:")
        print("  cd hub && python app.py\n")
        return 1
    
    # Run all tests
    print("Running test suite...\n")
    
    test_hub_health()
    test_post_valid_alert()
    test_post_invalid_alert()
    test_post_alert_edge_cases()
    test_get_alerts()
    test_metrics_endpoint()
    test_anonymization()
    test_severity_assignment()
    test_coordinated_detection()
    test_data_persistence()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in TEST_RESULTS if r["passed"])
    total = len(TEST_RESULTS)
    
    for result in TEST_RESULTS:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} {result['test']}")
        if result["message"] and not result["passed"]:
            print(f"    {result['message']}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ All tests passed! System is ready for evaluation.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    exit(main())

