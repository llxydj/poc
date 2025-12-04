# BAYANIHUB POC - Demo Script

This script guides you through demonstrating the BAYANIHUB proof-of-concept to your professor.

## Pre-Demo Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] 4 terminal windows ready
- [ ] Browser ready for dashboard
- [ ] Project directory accessible

## Demo Steps

### Step 1: Start the Hub (Terminal 1)

```bash
cd hub
python app.py
```

**Say**: "This is the central BAYANIHUB coordination hub. It receives security alerts from multiple SUCs, stores them in a database, and performs correlation analysis to detect coordinated attacks."

**Show**: The terminal output showing the hub is running on port 5000.

### Step 2: Start the Dashboard (Terminal 2)

```bash
cd dashboard
streamlit run dashboard.py
```

**Say**: "Here is the real-time dashboard that visualizes incoming alerts. It shows metrics, alert tables, and charts that help security analysts understand the threat landscape."

**Show**: The dashboard opening in the browser. Point out the empty state (no alerts yet).

### Step 3: Start SUC Simulator A (Terminal 3)

```bash
python suc_simulators/suc_a.py
```

**Say**: "This is SUC A, one of our simulated State Universities. It's running a local anomaly detection model and sending anonymized security alerts to the hub."

**Show**: The terminal output showing alerts being sent.

### Step 4: Start SUC Simulator B (Terminal 4)

```bash
python suc_simulators/suc_b.py
```

**Say**: "This is SUC B, another simulated university. Both SUCs are now sending alerts independently, and the hub is correlating them."

**Show**: Both SUC terminals sending alerts.

### Step 5: Show Real-time Updates

**Say**: "Watch the dashboard update in real-time. You can see alerts appearing, metrics updating, and the system categorizing alerts by severity."

**Show**: 
- Dashboard refreshing with new alerts
- Metrics updating (Total Alerts, High/Medium/Low counts)
- Alert table populating
- Charts showing distribution

### Step 6: Demonstrate Coordinated Attack Detection

**Say**: "The correlation engine is watching for coordinated attacks. When two different SUCs report the same type of event within a 2-minute window, the system flags it as a coordinated attack and raises the severity to High."

**Show**: 
- Look for alerts with "Coordinated" in the summary
- Point out High severity alerts
- Show how the hub terminal logs these detections

**Wait**: Let the system run for 2-3 minutes to allow correlation to occur naturally, or explain that the simulators are designed to occasionally send matching event types.

### Step 7: Show Anonymization

**Say**: "Notice that sensitive information is anonymized. IP addresses are masked, and usernames are hashed. This protects privacy while still allowing threat intelligence sharing."

**Show**: 
- Click on an alert in the dashboard
- Point out the `raw_masked` field showing masked IPs and hashed usernames
- Explain that the original data never leaves the SUC

### Step 8: Explain the Architecture

**Say**: "This POC demonstrates the core concepts of BAYANIHUB:
1. **Distributed Detection**: Each SUC runs local ML models
2. **Anonymized Sharing**: Privacy-preserving alert transmission
3. **Central Correlation**: Identifying patterns across institutions
4. **Real-time Visualization**: Situational awareness for security teams"

### Step 9: Show API Endpoints (Optional)

**Say**: "The hub exposes a REST API for programmatic access."

**Show**: 
- Open browser to `http://localhost:5000/alerts` (GET request)
- Show the JSON response
- Explain the API can be used by other tools

### Step 10: Wrap Up

**Say**: "This proof-of-concept demonstrates that the BAYANIHUB concept is technically feasible. For a full DOST-level implementation, we would add:
- Federated learning for collaborative model improvement
- Secure communication channels with mTLS
- Advanced correlation algorithms
- Incident response workflows
- Policy recommendation engine
- Production-grade security and scalability"

## Key Talking Points

1. **Privacy First**: Data is anonymized before leaving each SUC
2. **Distributed Intelligence**: Each SUC maintains local detection capabilities
3. **Centralized Coordination**: Hub provides national-level threat visibility
4. **Real-time Response**: Dashboard enables rapid decision-making
5. **Scalable Architecture**: Can be extended to all SUCs nationwide

## Expected Demo Duration

- Setup: 2-3 minutes
- Demonstration: 5-7 minutes
- Q&A: 5-10 minutes
- **Total: 12-20 minutes**

## Troubleshooting During Demo

If something goes wrong:

1. **Hub not starting**: Check port 5000 is free, restart terminal
2. **Dashboard not updating**: Refresh browser, check hub is running
3. **No alerts appearing**: Verify SUC simulators are running, check hub logs
4. **Import errors**: Ensure you're in the correct directory, verify dependencies

## Post-Demo

- Stop all processes (Ctrl+C in each terminal)
- Offer to show the code structure
- Be ready to discuss:
  - Technical implementation details
  - Privacy and security considerations
  - Scalability challenges
  - Next steps for full implementation

