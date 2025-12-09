import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go

HUB_URL = os.environ.get("HUB_URL", "http://localhost:5000/alerts")
HUB_BASE = HUB_URL.replace("/alerts", "")

# Page configuration
st.set_page_config(
    page_title="BAYANIHUB Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .severity-high {
        color: #dc3545;
        font-weight: 600;
    }
    .severity-medium {
        color: #ffc107;
        font-weight: 600;
    }
    .severity-low {
        color: #28a745;
        font-weight: 600;
    }
    .status-online {
        color: #28a745;
        font-weight: 600;
    }
    .status-offline {
        color: #dc3545;
        font-weight: 600;
    }
    .stAlert {
        padding: 1rem;
    }
    .coordinated-alert {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    
    # Connection status
    try:
        health_check = requests.get(f"{HUB_BASE}/health", timeout=1)
        if health_check.status_code == 200:
            st.markdown('<p class="status-online">🟢 Hub: Online</p>', unsafe_allow_html=True)
            hub_status = "online"
        else:
            st.markdown('<p class="status-offline">🔴 Hub: Offline</p>', unsafe_allow_html=True)
            hub_status = "offline"
    except:
        st.markdown('<p class="status-offline">🔴 Hub: Offline</p>', unsafe_allow_html=True)
        hub_status = "offline"
    
    st.markdown("---")
    
    # Refresh controls
    st.markdown("### ⚙️ Settings")
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=True, help="Automatically refresh dashboard")
    refresh_interval = st.slider("Refresh interval (seconds)", 1, 10, 3, help="How often to refresh data")
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🔍 Filters")
    filter_severity = st.multiselect(
        "Severity",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
        help="Filter alerts by severity level"
    )
    filter_suc = st.multiselect(
        "SUC",
        ["SUC_A", "SUC_B"],
        default=["SUC_A", "SUC_B"],
        help="Filter alerts by SUC"
    )
    filter_event_type = st.multiselect(
        "Event Type",
        ["login_attempts", "port_scan"],
        default=["login_attempts", "port_scan"],
        help="Filter alerts by event type"
    )
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Quick Stats")
    try:
        metrics = requests.get(f"{HUB_BASE}/metrics", timeout=2).json()
        st.metric("Total Alerts", metrics.get("total_alerts", 0))
        st.metric("High Severity", metrics.get("by_severity", {}).get("high", 0))
    except:
        st.info("Connect to hub to see stats")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("BAYANIHUB POC Dashboard")
    st.caption("Real-time security alert monitoring")

# Main content area
st.markdown('<h1 class="main-header">🛡️ BAYANIHUB Security Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time security alert monitoring and correlation across State Universities and Colleges</p>', unsafe_allow_html=True)

# Fetch data
def fetch_alerts():
    try:
        r = requests.get(HUB_URL, timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        return []
    return []

def fetch_metrics():
    try:
        r = requests.get(f"{HUB_BASE}/metrics", timeout=2)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

alerts = fetch_alerts()
metrics = fetch_metrics()

# Update session state
if alerts:
    st.session_state.alert_count = len(alerts)
    st.session_state.last_update = datetime.now()

# Metrics row
st.markdown("### 📈 Overview Metrics")
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

if metrics:
    total = metrics.get("total_alerts", 0)
    high = metrics.get("by_severity", {}).get("high", 0)
    medium = metrics.get("by_severity", {}).get("medium", 0)
    low = metrics.get("by_severity", {}).get("low", 0)
    suc_counts = metrics.get("by_suc", {})
    suc_a_count = suc_counts.get("SUC_A", 0)
    suc_b_count = suc_counts.get("SUC_B", 0)
else:
    total = len(alerts)
    high = sum(1 for a in alerts if a.get("severity") == "High")
    medium = sum(1 for a in alerts if a.get("severity") == "Medium")
    low = sum(1 for a in alerts if a.get("severity") == "Low")
    suc_a_count = sum(1 for a in alerts if a.get("suc_id") == "SUC_A")
    suc_b_count = sum(1 for a in alerts if a.get("suc_id") == "SUC_B")

with metric_col1:
    st.metric("Total Alerts", total, delta=None)

with metric_col2:
    delta_high = None
    st.metric("🔴 High", high, delta=delta_high, delta_color="inverse")

with metric_col3:
    st.metric("🟡 Medium", medium, delta=None)

with metric_col4:
    st.metric("🟢 Low", low, delta=None)

with metric_col5:
    st.metric("Active SUCs", f"{suc_a_count + suc_b_count}", delta=None)

# Visualizations row
st.markdown("### 📊 Visualizations")
viz_col1, viz_col2 = st.columns(2)

if alerts:
    df = pd.DataFrame(alerts)
    
    # Apply filters
    if filter_severity:
        df = df[df["severity"].isin(filter_severity)]
    if filter_suc:
        df = df[df["suc_id"].isin(filter_suc)]
    if filter_event_type:
        df = df[df["event_type"].isin(filter_event_type)]
    
    # Severity distribution pie chart
    with viz_col1:
        if "severity" in df.columns and len(df) > 0:
            severity_counts = df["severity"].value_counts()
            fig_pie = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title="Alerts by Severity",
                color_discrete_map={
                    "High": "#dc3545",
                    "Medium": "#ffc107",
                    "Low": "#28a745"
                }
            )
            fig_pie.update_layout(showlegend=True, height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data to display")
    
    # SUC distribution bar chart
    with viz_col2:
        if "suc_id" in df.columns and len(df) > 0:
            suc_counts = df["suc_id"].value_counts()
            fig_bar = px.bar(
                x=suc_counts.index,
                y=suc_counts.values,
                title="Alerts by SUC",
                labels={"x": "SUC", "y": "Count"},
                color=suc_counts.values,
                color_continuous_scale="Blues"
            )
            fig_bar.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data to display")
    
    # Timeline chart
    if "timestamp" in df.columns and len(df) > 0:
        st.markdown("### ⏱️ Alert Timeline")
        try:
            df["timestamp_parsed"] = pd.to_datetime(df["timestamp"], errors='coerce')
            # Remove rows with invalid timestamps
            df_valid = df[df["timestamp_parsed"].notna()]
            
            if len(df_valid) > 0:
                df_timeline = df_valid.groupby([df_valid["timestamp_parsed"].dt.floor("1min"), "severity"]).size().reset_index(name="count")
                df_timeline = df_timeline.pivot(index="timestamp_parsed", columns="severity", values="count").fillna(0)
                
                fig_timeline = go.Figure()
                for severity in ["High", "Medium", "Low"]:
                    if severity in df_timeline.columns:
                        fig_timeline.add_trace(go.Scatter(
                            x=df_timeline.index,
                            y=df_timeline[severity],
                            mode='lines+markers',
                            name=severity,
                            line=dict(
                                width=2,
                                color="#dc3545" if severity == "High" else "#ffc107" if severity == "Medium" else "#28a745"
                            )
                        ))
                
                fig_timeline.update_layout(
                    title="Alerts Over Time",
                    xaxis_title="Time",
                    yaxis_title="Number of Alerts",
                    height=300,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.warning("No valid timestamps found for timeline chart")
        except Exception as e:
            st.warning(f"Could not generate timeline: {e}")
    
    # Alerts table
    st.markdown("### 🚨 Recent Alerts")
    
    # Search box
    search_term = st.text_input("🔍 Search alerts", placeholder="Search by SUC, event type, or summary...")
    
    if search_term:
        try:
            mask = pd.Series([False] * len(df))
            if "suc_id" in df.columns:
                mask = mask | df["suc_id"].astype(str).str.contains(search_term, case=False, na=False)
            if "event_type" in df.columns:
                mask = mask | df["event_type"].astype(str).str.contains(search_term, case=False, na=False)
            if "summary" in df.columns:
                mask = mask | df["summary"].astype(str).str.contains(search_term, case=False, na=False)
            df_filtered = df[mask]
        except:
            df_filtered = df
    else:
        df_filtered = df
    
    # Prepare display dataframe
    if len(df_filtered) > 0:
        df_display = df_filtered.copy()
        
        # Format timestamp
        if "timestamp" in df_display.columns:
            try:
                df_display["timestamp"] = pd.to_datetime(df_display["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
        
        # Format anomaly_score
        if "anomaly_score" in df_display.columns:
            df_display["anomaly_score"] = df_display["anomaly_score"].apply(
                lambda x: f"{x:.2f}" if pd.notna(x) and x is not None else "N/A"
            )
        
        # Add severity color coding
        def format_severity(severity):
            if severity == "High":
                return f'<span class="severity-high">🔴 {severity}</span>'
            elif severity == "Medium":
                return f'<span class="severity-medium">🟡 {severity}</span>'
            else:
                return f'<span class="severity-low">🟢 {severity}</span>'
        
        # Select and reorder columns
        display_cols = ["id", "timestamp", "suc_id", "event_type", "severity", "anomaly_score", "summary"]
        available_cols = [col for col in display_cols if col in df_display.columns]
        df_display = df_display[available_cols]
        
        # Rename columns for better display
        df_display = df_display.rename(columns={
            "id": "ID",
            "timestamp": "Time",
            "suc_id": "SUC",
            "event_type": "Event Type",
            "severity": "Severity",
            "anomaly_score": "Anomaly Score",
            "summary": "Summary"
        })
        
        # Show coordinated alerts prominently
        if "summary" in df_filtered.columns:
            try:
                coordinated_alerts = df_filtered[df_filtered["summary"].astype(str).str.contains("Coordinated", case=False, na=False)]
                if len(coordinated_alerts) > 0:
                    st.warning(f"⚠️ **{len(coordinated_alerts)} Coordinated Attack(s) Detected!** These require immediate attention.")
            except:
                pass
        
        # Display table with expandable rows
        st.dataframe(
            df_display.head(100),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.caption(f"Showing {len(df_display)} alert(s). Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.last_update else 'Never'}")
        
        # Alert details expander
        if len(df_filtered) > 0:
            with st.expander("📋 View Alert Details"):
                selected_idx = st.selectbox("Select alert ID", df_filtered["id"].tolist(), key="alert_selector")
                if selected_idx:
                    selected_alert = df_filtered[df_filtered["id"] == selected_idx].iloc[0]
                    
                    detail_col1, detail_col2 = st.columns(2)
                    with detail_col1:
                        st.write("**Alert ID:**", selected_alert.get("id"))
                        st.write("**SUC:**", selected_alert.get("suc_id"))
                        st.write("**Event Type:**", selected_alert.get("event_type"))
                        st.write("**Severity:**", selected_alert.get("severity"))
                    
                    with detail_col2:
                        st.write("**Timestamp:**", selected_alert.get("timestamp", "N/A"))
                        score = selected_alert.get('anomaly_score')
                        if score is not None and pd.notna(score):
                            try:
                                st.write("**Anomaly Score:**", f"{float(score):.2f}")
                            except:
                                st.write("**Anomaly Score:**", "N/A")
                        else:
                            st.write("**Anomaly Score:**", "N/A")
                        st.write("**Summary:**", selected_alert.get("summary", "N/A"))
                    
                    if selected_alert.get("raw_masked"):
                        st.write("**Anonymized Details:**")
                        st.json(selected_alert.get("raw_masked", {}))
    else:
        st.info("No alerts match the current filters. Adjust filters or wait for new alerts.")
else:
    # Empty state
    st.info("""
    ### 📡 No alerts received yet
    
    To start seeing alerts:
    1. Make sure the hub is running: `cd hub && python app.py`
    2. Start SUC simulators: `python suc_simulators/suc_a.py` and `python suc_simulators/suc_b.py`
    3. Wait a few seconds for alerts to appear
    
    Check the connection status in the sidebar.
    """)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("🛡️ BAYANIHUB POC")
with footer_col2:
    if st.session_state.last_update:
        st.caption(f"Last update: {st.session_state.last_update.strftime('%H:%M:%S')}")
    else:
        st.caption("Waiting for data...")
with footer_col3:
    st.caption(f"Total alerts: {st.session_state.alert_count}")

# Auto-refresh logic
if auto_refresh and hub_status == "online":
    time.sleep(refresh_interval)
    st.rerun()
