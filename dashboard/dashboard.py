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

# Manual refresh button at top (better UX)
refresh_col1, refresh_col2, refresh_col3 = st.columns([2, 1, 2])
with refresh_col2:
    if st.button("🔄 Refresh Data Now", use_container_width=True, type="primary", key="top_refresh"):
        st.rerun()

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

with metric_col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📊 Total Alerts", total, delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    delta_high = None
    st.metric("🔴 High Severity", high, delta=delta_high, delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🟡 Medium Severity", medium, delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🟢 Low Severity", low, delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    active_sucs = suc_a_count + suc_b_count
    st.metric("🏫 Active SUCs", active_sucs, delta=None)
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
    
    # Enhanced Search box with better styling
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_term = st.text_input(
            "🔍 Search alerts", 
            placeholder="Search by SUC, event type, or summary...",
            help="Enter keywords to filter alerts. Search is case-insensitive."
        )
    with search_col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("🔍 Search", use_container_width=True):
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
        
        # Enhanced table display with better styling
        st.dataframe(
            df_display.head(100),
            use_container_width=True,
            hide_index=True,
            height=450,
            column_config={
                "ID": st.column_config.NumberColumn("ID", format="%d"),
                "Time": st.column_config.TextColumn("Time"),
                "SUC": st.column_config.TextColumn("SUC"),
                "Event Type": st.column_config.TextColumn("Event Type"),
                "Severity": st.column_config.TextColumn("Severity"),
                "Anomaly Score": st.column_config.TextColumn("Anomaly Score"),
                "Summary": st.column_config.TextColumn("Summary", width="large")
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
                            st.markdown("#### Anonymized Event Details")
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

# Bottom refresh button (duplicate for convenience)
st.markdown("---")
refresh_bottom_col1, refresh_bottom_col2, refresh_bottom_col3 = st.columns([2, 1, 2])
with refresh_bottom_col2:
    if st.button("🔄 Refresh Data", use_container_width=True, type="secondary", key="bottom_refresh"):
        st.rerun()

# Auto-refresh logic - Only runs if enabled (may cause page reload)
if auto_refresh and hub_status == "online":
    # Note: This will cause page reload, which may interrupt navigation
    # Consider using manual refresh instead for better UX
    time.sleep(refresh_interval)
    st.rerun()
