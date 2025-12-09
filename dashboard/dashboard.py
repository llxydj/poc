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

# Enhanced Professional CSS for Modern UI/UX
st.markdown("""
<style>
    /* Main Header - Professional Gradient */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1f77b4 0%, #2c5aa0 50%, #1a4d8c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* Sub Header */
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
        font-style: italic;
        text-align: center;
    }
    
    /* Metric Cards - Professional Design */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    /* Severity Badges - Enhanced */
    .severity-high {
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(220,53,69,0.3);
    }
    
    .severity-medium {
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(255,152,0,0.3);
    }
    
    .severity-low {
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(40,167,69,0.3);
    }
    
    /* Status Indicators - Professional */
    .status-online {
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        padding: 8px 16px;
        border-radius: 25px;
        display: inline-block;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(40,167,69,0.3);
        animation: pulse-green 2s infinite;
    }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 2px 6px rgba(40,167,69,0.3); }
        50% { box-shadow: 0 2px 12px rgba(40,167,69,0.6); }
    }
    
    .status-offline {
        color: #ffffff;
        font-weight: 700;
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        padding: 8px 16px;
        border-radius: 25px;
        display: inline-block;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(220,53,69,0.3);
    }
    
    /* Coordinated Alert - Enhanced Warning */
    .coordinated-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 6px solid #ff9800;
        padding: 1.2rem;
        margin: 1.5rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(255,152,0,0.25);
        animation: pulse-warning 3s infinite;
    }
    
    @keyframes pulse-warning {
        0%, 100% { border-left-width: 6px; }
        50% { border-left-width: 8px; }
    }
    
    /* Button Enhancements */
    .stButton>button {
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #1f77b4 0%, #2c5aa0 100%);
        color: white;
    }
    
    /* Table Enhancements */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Chart Container */
    .plotly {
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        background: white;
        padding: 10px;
    }
    
    /* Section Headers */
    h3 {
        color: #2c5aa0;
        font-weight: 700;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #e0e0e0;
        font-size: 1.5rem;
    }
    
    /* Info/Warning/Error Boxes */
    .stInfo {
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .stWarning {
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        box-shadow: 0 2px 6px rgba(255,152,0,0.2);
    }
    
    .stError {
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        box-shadow: 0 2px 6px rgba(220,53,69,0.2);
    }
    
    .stSuccess {
        border-radius: 10px;
        border-left: 5px solid #28a745;
        box-shadow: 0 2px 6px rgba(40,167,69,0.2);
    }
    
    /* Sidebar Enhancements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 3px rgba(31,119,180,0.1);
    }
    
    /* Select Boxes */
    .stSelectbox>div>div>select {
        border-radius: 8px;
    }
    
    /* Multiselect */
    .stMultiSelect>div>div {
        border-radius: 8px;
    }
    
    /* Footer */
    footer {
        visibility: hidden;
    }
    
    /* Hide Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1f77b4 0%, #2c5aa0 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2c5aa0 0%, #1a4d8c 100%);
    }
    
    /* Card-like containers */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Better spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0

# Enhanced Sidebar with Professional Design
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")
    
    # Connection status with enhanced display
    st.markdown("### 🔌 Connection Status")
    try:
        health_check = requests.get(f"{HUB_BASE}/health", timeout=1)
        if health_check.status_code == 200:
            st.markdown('<div style="text-align: center;"><p class="status-online">🟢 Hub: Online</p></div>', unsafe_allow_html=True)
            hub_status = "online"
        else:
            st.markdown('<div style="text-align: center;"><p class="status-offline">🔴 Hub: Offline</p></div>', unsafe_allow_html=True)
            hub_status = "offline"
    except:
        st.markdown('<div style="text-align: center;"><p class="status-offline">🔴 Hub: Offline</p></div>', unsafe_allow_html=True)
        hub_status = "offline"
    
    st.markdown("---")
    
    # Refresh controls
    st.markdown("### ⚙️ Settings")
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=False, help="⚠️ Auto-refresh causes page reload which may interrupt navigation. Use manual refresh button for better UX.")
    if auto_refresh:
        st.info("💡 Tip: Use the 'Refresh Data' button below for better navigation experience")
        refresh_interval = st.slider("Refresh interval (seconds)", 3, 30, 5, help="How often to refresh data (longer = less freezing)")
    else:
        refresh_interval = 5  # Default when auto-refresh is off
        st.success("✅ Manual refresh enabled - Use 'Refresh Data' button to update")
    
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
    
    # Enhanced Statistics Section
    st.markdown("### 📊 Quick Statistics")
    try:
        metrics = requests.get(f"{HUB_BASE}/metrics", timeout=2).json()
        total = metrics.get("total_alerts", 0)
        high = metrics.get("by_severity", {}).get("high", 0)
        
        st.metric("📊 Total Alerts", total, help="Total number of alerts received")
        st.metric("🔴 High Severity", high, help="Number of high-severity alerts")
        
        # Show coordinated attacks if any
        coordinated = metrics.get("coordinated_attacks", 0)
        if coordinated > 0:
            st.warning(f"⚠️ {coordinated} Coordinated Attack(s)")
    except:
        st.info("ℹ️ Connect to hub to see statistics")
    
    st.markdown("---")
    
    # Enhanced About Section
    st.markdown("### ℹ️ About")
    st.markdown("""
    **BAYANIHUB POC Dashboard**
    
    Real-time security alert monitoring and correlation system for State Universities and Colleges.
    
    **Features:**
    - Real-time alert visualization
    - ML-based anomaly detection
    - Coordinated attack detection
    - Privacy-preserving data sharing
    """)
    
    st.markdown("---")
    st.caption("🛡️ BAYANIHUB POC v1.0")

# Enhanced Main Header Section
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    st.markdown('<h1 class="main-header">🛡️ BAYANIHUB Security Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time security alert monitoring and correlation across State Universities and Colleges</p>', unsafe_allow_html=True)

# Enhanced Refresh Section with Status
refresh_section = st.container()
with refresh_section:
    refresh_col1, refresh_col2, refresh_col3, refresh_col4 = st.columns([1, 1.5, 1.5, 1])
    with refresh_col2:
        if st.button("🔄 Refresh Data Now", use_container_width=True, type="primary", key="top_refresh", help="Click to manually refresh all data from the hub"):
            st.rerun()
    with refresh_col3:
        if st.session_state.last_update:
            last_update_str = st.session_state.last_update.strftime('%H:%M:%S')
            st.caption(f"⏰ Last updated: {last_update_str}")
        else:
            st.caption("⏰ Waiting for data...")

st.markdown("---")

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

# Enhanced Metrics Section with Better Visual Design
st.markdown("### 📈 Overview Metrics")
st.markdown("---")

# Create metric cards with better visual hierarchy
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

# Enhanced Metric Cards with Professional Styling
with metric_col1:
    st.markdown('<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #1f77b4; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    st.metric("📊 Total Alerts", f"{total:,}", delta=None, help="Total number of alerts in the system")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col2:
    st.markdown('<div style="background: linear-gradient(135deg, #ffffff 0%, #ffe6e6 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #dc3545; box-shadow: 0 2px 8px rgba(220,53,69,0.15);">', unsafe_allow_html=True)
    delta_high = None
    st.metric("🔴 High Severity", f"{high:,}", delta=delta_high, delta_color="inverse", help="Number of high-severity alerts requiring immediate attention")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col3:
    st.markdown('<div style="background: linear-gradient(135deg, #ffffff 0%, #fff3e0 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #ff9800; box-shadow: 0 2px 8px rgba(255,152,0,0.15);">', unsafe_allow_html=True)
    st.metric("🟡 Medium Severity", f"{medium:,}", delta=None, help="Number of medium-severity alerts")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col4:
    st.markdown('<div style="background: linear-gradient(135deg, #ffffff 0%, #e8f5e9 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #28a745; box-shadow: 0 2px 8px rgba(40,167,69,0.15);">', unsafe_allow_html=True)
    st.metric("🟢 Low Severity", f"{low:,}", delta=None, help="Number of low-severity alerts")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col5:
    st.markdown('<div style="background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #2196f3; box-shadow: 0 2px 8px rgba(33,150,243,0.15);">', unsafe_allow_html=True)
    active_sucs = suc_a_count + suc_b_count
    st.metric("🏫 Active SUCs", active_sucs, delta=None, help="Number of State Universities and Colleges sending alerts")
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Visualizations Section
st.markdown("### 📊 Visualizations")
st.markdown("---")
viz_col1, viz_col2 = st.columns(2)

if alerts and len(alerts) > 0:
    try:
        df = pd.DataFrame(alerts)
        
        # Ensure required columns exist
        required_cols = ["severity", "suc_id", "event_type"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "unknown"
        
        # Apply filters
        if filter_severity and len(filter_severity) > 0:
            df = df[df["severity"].isin(filter_severity)]
        if filter_suc and len(filter_suc) > 0:
            df = df[df["suc_id"].isin(filter_suc)]
        if filter_event_type and len(filter_event_type) > 0:
            df = df[df["event_type"].isin(filter_event_type)]
    except Exception as e:
        st.error(f"Error processing alerts: {e}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

# Charts section (works with df regardless of how it was created)
# Severity distribution pie chart
with viz_col1:
    if not df.empty and "severity" in df.columns and len(df) > 0:
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
        fig_pie.update_layout(
            showlegend=True, 
            height=380,
            font=dict(size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("📊 No severity data available to display")

# SUC distribution bar chart
with viz_col2:
    if not df.empty and "suc_id" in df.columns and len(df) > 0:
        suc_counts = df["suc_id"].value_counts()
        fig_bar = px.bar(
            x=suc_counts.index,
            y=suc_counts.values,
            title="Alerts by SUC",
            labels={"x": "SUC", "y": "Count"},
            color=suc_counts.values,
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(
            showlegend=False, 
            height=380,
            font=dict(size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("📊 No SUC data available to display")
    
# Timeline chart
if not df.empty and "timestamp" in df.columns and len(df) > 0:
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
                height=350,
                hovermode='x unified',
                font=dict(size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.warning("No valid timestamps found for timeline chart")
    except Exception as e:
        st.warning(f"Could not generate timeline: {e}")

# Enhanced Alerts Section
st.markdown("### 🚨 Recent Alerts")
    st.markdown("---")
    
    # Enhanced Search Section with Professional Design
    st.markdown("#### 🔍 Search & Filter Alerts")
    search_col1, search_col2, search_col3 = st.columns([4, 1, 1])
    with search_col1:
        search_term = st.text_input(
            "🔍 Search alerts", 
            placeholder="Type to search by SUC, event type, or summary...",
            help="Enter keywords to filter alerts. Search is case-insensitive and searches across multiple fields.",
            label_visibility="collapsed"
        )
    with search_col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("🔍 Search", use_container_width=True, type="secondary"):
            st.rerun()
    with search_col3:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("🔄 Clear", use_container_width=True, help="Clear search and filters"):
            st.rerun()
    
    if not df.empty:
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
            except Exception as e:
                st.warning(f"Search error: {e}")
                df_filtered = df
        else:
            df_filtered = df
    else:
        df_filtered = pd.DataFrame()
    
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
        
        # Show coordinated alerts prominently with enhanced styling
        if "summary" in df_filtered.columns:
            try:
                coordinated_alerts = df_filtered[df_filtered["summary"].astype(str).str.contains("Coordinated", case=False, na=False)]
                if len(coordinated_alerts) > 0:
                    st.markdown(
                        f'<div class="coordinated-alert">'
                        f'<h4>⚠️ <strong>{len(coordinated_alerts)} Coordinated Attack(s) Detected!</strong></h4>'
                        f'<p>These alerts indicate coordinated attacks across multiple SUCs and require immediate attention.</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            except:
                pass
        
        # Enhanced table display with professional styling
        st.markdown("#### 📋 Alert Details Table")
        st.dataframe(
            df_display.head(100),
            use_container_width=True,
            hide_index=True,
            height=500,
            column_config={
                "ID": st.column_config.NumberColumn("ID", format="%d", help="Unique alert identifier"),
                "Time": st.column_config.TextColumn("Time", help="Alert timestamp"),
                "SUC": st.column_config.TextColumn("SUC", help="State University/College identifier"),
                "Event Type": st.column_config.TextColumn("Event Type", help="Type of security event"),
                "Severity": st.column_config.TextColumn("Severity", help="Alert severity level"),
                "Anomaly Score": st.column_config.TextColumn("Anomaly Score", help="ML anomaly detection score (0-1)"),
                "Summary": st.column_config.TextColumn("Summary", width="large", help="Alert summary and correlation details")
            }
        )
        
        # Enhanced footer with better info
        info_text = f"📊 Showing {len(df_display)} of {len(df_filtered)} alert(s)"
        if st.session_state.last_update:
            info_text += f" | Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}"
        st.info(info_text)
        
        # Enhanced Alert details expander with better layout
        if len(df_filtered) > 0:
            with st.expander("📋 View Detailed Alert Information", expanded=False):
                alert_ids = df_filtered["id"].tolist()
                if alert_ids:
                    selected_idx = st.selectbox(
                        "Select alert ID to view details", 
                        alert_ids, 
                        key="alert_selector",
                        help="Choose an alert ID to see full details"
                    )
                    if selected_idx:
                        selected_alert = df_filtered[df_filtered["id"] == selected_idx].iloc[0]
                        
                        # Enhanced detail display with cards
                        st.markdown("#### Alert Details")
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            st.markdown("**Basic Information**")
                            st.markdown(f"**Alert ID:** `{selected_alert.get('id')}`")
                            st.markdown(f"**SUC:** `{selected_alert.get('suc_id', 'N/A')}`")
                            st.markdown(f"**Event Type:** `{selected_alert.get('event_type', 'N/A')}`")
                            severity = selected_alert.get('severity', 'Unknown')
                            if severity == "High":
                                st.markdown(f'**Severity:** <span class="severity-high">🔴 {severity}</span>', unsafe_allow_html=True)
                            elif severity == "Medium":
                                st.markdown(f'**Severity:** <span class="severity-medium">🟡 {severity}</span>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'**Severity:** <span class="severity-low">🟢 {severity}</span>', unsafe_allow_html=True)
                        
                        with detail_col2:
                            st.markdown("**Timing & Scoring**")
                            st.markdown(f"**Timestamp:** `{selected_alert.get('timestamp', 'N/A')}`")
                            score = selected_alert.get('anomaly_score')
                            if score is not None and pd.notna(score):
                                try:
                                    score_val = float(score)
                                    score_color = "#dc3545" if score_val > 0.7 else "#ff9800" if score_val > 0.5 else "#28a745"
                                    st.markdown(f'**Anomaly Score:** <span style="color: {score_color}; font-weight: 700;">{score_val:.2f}</span>', unsafe_allow_html=True)
                                except:
                                    st.markdown("**Anomaly Score:** N/A")
                            else:
                                st.markdown("**Anomaly Score:** N/A")
                            st.markdown(f"**Summary:** {selected_alert.get('summary', 'N/A')}")
                        
                        # Anonymized details in expandable section
                        if selected_alert.get("raw_masked"):
                            st.markdown("---")
                            st.markdown("#### 🔒 Anonymized Event Details")
                            st.markdown("*Privacy-protected data (IPs and usernames anonymized)*")
                            st.json(selected_alert.get("raw_masked", {}))
    else:
        st.warning("⚠️ No alerts match the current filters. Try adjusting your filters or wait for new alerts.")
else:
    # Enhanced Empty State with Professional Design
    empty_col1, empty_col2, empty_col3 = st.columns([1, 2, 1])
    with empty_col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color: #2c5aa0; margin-bottom: 1rem;">📡 No Alerts Received Yet</h2>
            <p style="color: #555; font-size: 1.1rem; margin-bottom: 2rem;">The dashboard is ready and waiting for alerts from the hub.</p>
            <div style="text-align: left; background: white; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
                <h4 style="color: #2c5aa0; margin-bottom: 1rem;">🚀 Getting Started:</h4>
                <ol style="color: #555; line-height: 2;">
                    <li><strong>Start the Hub:</strong> <code>cd hub && python app.py</code></li>
                    <li><strong>Start SUC Simulators:</strong> <code>python suc_simulators/suc_a.py</code> and <code>python suc_simulators/suc_b.py</code></li>
                    <li><strong>Wait a few seconds</strong> for alerts to appear</li>
                </ol>
                <p style="color: #666; margin-top: 1rem; font-style: italic;">Check the connection status in the sidebar to verify hub connectivity.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Footer Section
st.markdown("---")
footer_container = st.container()
with footer_container:
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
    with footer_col1:
        st.markdown("**🛡️ BAYANIHUB POC**")
        st.caption("Security Alert System")
    with footer_col2:
        if st.session_state.last_update:
            st.markdown("**⏰ Last Update**")
            st.caption(st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            st.markdown("**⏰ Status**")
            st.caption("Waiting for data...")
    with footer_col3:
        st.markdown("**📊 Alert Count**")
        st.caption(f"{st.session_state.alert_count:,} alerts")
    with footer_col4:
        st.markdown("**🔌 Connection**")
        if hub_status == "online":
            st.caption("🟢 Online")
        else:
            st.caption("🔴 Offline")

# Bottom refresh section
st.markdown("---")
refresh_bottom_col1, refresh_bottom_col2, refresh_bottom_col3 = st.columns([2, 1, 2])
with refresh_bottom_col2:
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary", key="bottom_refresh", help="Refresh all data from the hub"):
        st.rerun()

# Auto-refresh logic - Only runs if enabled (may cause page reload)
if auto_refresh and hub_status == "online":
    # Note: This will cause page reload, which may interrupt navigation
    # Consider using manual refresh instead for better UX
    time.sleep(refresh_interval)
    st.rerun()
