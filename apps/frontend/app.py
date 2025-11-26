import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from typing import List, Dict, Optional

# -----------------------------------------------------------
# Configuration
# -----------------------------------------------------------
BACKEND_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{BACKEND_URL}/predict/start"
HEALTH_CHECK_ENDPOINT = f"{BACKEND_URL}/check"

# -----------------------------------------------------------
# Page Setup
# -----------------------------------------------------------
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------
# Session State Management
# -----------------------------------------------------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'work_orders' not in st.session_state:
    st.session_state.work_orders = []
if 'machine_stats' not in st.session_state:
    st.session_state.machine_stats = {
        "total_machines": 100,
        "healthy_machines": 100,
        "at_risk": 0,
        "critical": 0
    }
if 'failing_machines_queue' not in st.session_state:
    st.session_state.failing_machines_queue = []
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False

# -----------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------
def check_backend_health():
    """Check if backend is available"""
    try:
        response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=2)
        return response.status_code == 200
    except:
        return False

def render_custom_alert_card(message, timestamp, severity="critical"):
    """
    Renders a custom alert card with a colored left border.
    severity: "critical" (red), "warning" (yellow), "info" (blue)
    """
    # Define colors for the left border strip
    color_map = {
        "critical": "#D32F2F",  # Red
        "warning": "#FFA000",   # Amber
        "info": "#1976D2"       # Blue
    }
    border_color = color_map.get(severity, "#D32F2F")
    
    # Custom HTML/CSS for the card
    card_html = f"""
    <div style="
        background-color: white;
        border-left: 5px solid {border_color};
        padding: 2px;
        border-radius: 4px;
        margin-bottom: 3px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtle shadow */
    ">
        <div style="color: #333; font-weight: 500; font-size: 14px;">
            {message}
        </div>
        <div style="color: #888; font-size: 12px;">
            {timestamp}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def run_simulation():
    """Call backend simulation endpoint"""
    try:
        # The spinner is already shown in start_simulation, so we just make the request
        response = requests.post(PREDICT_ENDPOINT, timeout=300)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            st.error(f"Backend returned error: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        st.error("Simulation timed out. The process is taking longer than expected.")
        st.info("Try again or check if the backend is processing correctly.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {str(e)}")
        st.info("Make sure the backend server is running on http://localhost:8000")
        return []

def process_simulation_results(results: List[Dict]):
    """Process simulation results to extract alerts, work orders, stats, and queue"""
    # Use sets to track unique alerts and work orders by machine_id
    alerts_dict = {}  # machine_id -> alert info
    work_orders_dict = {}  # machine_id -> work order info
    failing_machines = []
    
    # Track all machines for statistics
    critical_count = 0
    at_risk_count = 0
    healthy_count = 0
    
    # Process each machine result
    for result in results:
        machine_id = result.get("machineID")
        prediction = result.get("prediciton", {})  # Note: backend has typo "prediciton"
        failure_prob = prediction.get("failure_prob", 0)
        failure_label = prediction.get("failure_label", 0)
        rul = prediction.get("rul")
        timestamp = result.get("timestamp")
        
        # Determine status based on RUL hours
        # Critical: RUL < 10 hours
        # At Risk: RUL between 10 to 24 hours (inclusive)
        # Healthy: No failure predicted (failure_label == 0) or RUL > 24 hours (predicted to fail but not immediate)
        
        if failure_label == 0:
            # Machine is not predicted to fail, so it's healthy
            status = "Healthy"
        elif failure_label == 1 and rul is not None:
            # Machine is predicted to fail, categorize by RUL
            if rul < 12:
                status = "Critical"
            elif 12 <= rul <= 24:
                status = "At Risk"
            else:
                # RUL > 24 hours - still predicted to fail but beyond immediate risk window
                # Count as "Healthy" in statistics since no immediate action needed
                status = "Healthy"
        else:
            # Edge case: failure_label == 1 but no RUL (shouldn't happen, but handle it)
            status = "At Risk"
        
        # Only add to failing machines queue if machine is actually failing
        if failure_label == 1:
            # For queue display: machines with RUL > 24 should show as "Warning" 
            # (they're still predicted to fail, just not immediate)
            queue_status = status
            if failure_label == 1 and rul is not None and rul > 24:
                queue_status = "Warning"
            
            failing_machines.append({
                "machineID": machine_id,
                "failure_probability": f"{failure_prob:.2%}",
                "rul_hours": f"{rul:.1f}" if rul else "N/A",
                "timestamp": str(timestamp) if timestamp else "N/A",
                "status": queue_status
            })
            
            # Only machines with failure_label == 1 have alerts and work orders
            # Create alert for this failing machine (deduplicated by machine_id)
            if machine_id not in alerts_dict:
                alerts_dict[machine_id] = {
                    "machine_id": machine_id,
                    "probability": failure_prob,
                    "timestamp": timestamp
                }
            
            # Create work order only if machine has RUL (which it should if failing)
            if rul is not None and machine_id not in work_orders_dict:
                work_orders_dict[machine_id] = {
                    "machine_id": machine_id,
                    "rul_hours": rul,
                    "timestamp": timestamp
                }
        
        # Calculate machine statistics for ALL machines (100 total) based on RUL
        if status == "Critical":
            critical_count += 1
        elif status == "At Risk":
            at_risk_count += 1
        else:  # Healthy
            healthy_count += 1
    
    # Convert dictionaries to lists
    alerts = list(alerts_dict.values())
    work_orders = list(work_orders_dict.values())
    
    # Sort alerts by probability (highest first)
    alerts.sort(key=lambda x: x.get("probability", 0), reverse=True)
    
    # Sort work orders by RUL (shortest first)
    work_orders.sort(key=lambda x: x.get("rul_hours", float('inf')) if isinstance(x.get("rul_hours"), (int, float)) else float('inf'))
    
    # Calculate aggregate stats (all 100 machines)
    stats = {
        "total_machines": 100,
        "healthy_machines": healthy_count,
        "at_risk": at_risk_count,
        "critical": critical_count
    }
    
    return alerts, work_orders, stats, failing_machines

def start_simulation():
    """Start the simulation and update all dashboard components"""
    st.session_state.simulation_running = True
    
    # Show loading screen
    with st.spinner("Running simulation... This may take a few moments."):
        results = run_simulation()
    
    if results:
        # Process results with loading indicator
        with st.spinner("Processing results and updating dashboard..."):
            alerts, work_orders, stats, queue = process_simulation_results(results)
            st.session_state.simulation_results = results
            st.session_state.alerts = alerts
            st.session_state.work_orders = work_orders
            st.session_state.machine_stats = stats
            st.session_state.failing_machines_queue = queue
        
        st.session_state.simulation_running = False
        return True
    else:
        st.session_state.simulation_running = False
        return False

def reload_rul():
    """Reload RUL predictions for machines in the failure queue"""
    # Re-run simulation to get updated RUL values
    results = run_simulation()
    
    if results:
        alerts, work_orders, stats, queue = process_simulation_results(results)
        # Update only the queue and related data
        st.session_state.failing_machines_queue = queue
        st.session_state.alerts = alerts
        st.session_state.work_orders = work_orders
        return True
    return False

# -----------------------------------------------------------
# Sidebar - Control Panel (Collapsible)
# -----------------------------------------------------------
with st.sidebar:
    st.header("Control Panel")
    
    # Navigation buttons
    if st.button("Dashboard", use_container_width=True, 
                 type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
        st.session_state.current_page = "Dashboard"
        st.rerun()
    
    if st.button("Failure Queue", use_container_width=True,
                 type="primary" if st.session_state.current_page == "Failure Queue" else "secondary"):
        st.session_state.current_page = "Failure Queue"
        st.rerun()
    
    st.markdown("---")
    
    # # Backend health check
    # backend_healthy = check_backend_health()
    # if backend_healthy:
    #     st.success("Backend Connected")
    # else:
    #     st.error("Backend Offline")
    #     st.info("Ensure backend is running on http://localhost:8000")

    # st.markdown("---")

    st.caption("When Start Simulation button is clicked, we get sensor readings and event data (error, failure, and maintenance) for the past hour on all 100 machines.")
    st.caption("We run a feature engineering pipeline on those data and pass them on for prediction. Our model classifies if the machine fails in the next 24 hours, and calculates RUL for the machines that are about to fail. ")
    st.caption("Failure queue lists the information on the machines that are about to fail with their RUL, timestamp, failure probability, and status.")

# -----------------------------------------------------------
# Dashboard Page
# -----------------------------------------------------------
if st.session_state.current_page == "Dashboard":
    # Header with Start Simulation button
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.title("Predictive Maintenance Dashboard")
    
    with header_col2:
        if st.button("Start Simulation", use_container_width=True, 
                     disabled=st.session_state.simulation_running,
                     type="primary"):
            if start_simulation():
                st.success("Simulation completed successfully!")
                st.rerun()
            else:
                st.error("Simulation failed. Check backend connection.")
    
    # Enhanced loading screen
    if st.session_state.simulation_running:
        # Show loading message with spinner
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            st.markdown("###Running Simulation")
            st.markdown("Please wait while we process all machines...")
            
            # Progress steps
            progress_col1, progress_col2, progress_col3 = st.columns(3)
            with progress_col1:
                st.markdown("**Loading Data**")
                st.progress(0.33)
            with progress_col2:
                st.markdown("**Running Predictions**")
                st.progress(0.66)
            with progress_col3:
                st.markdown("**Processing Results**")
                st.progress(1.0)
            
            st.info("This process may take 30-60 seconds. Please do not close this page.")
    
    st.markdown("---")
    
    # Machine Statistics Bar (Top Row - 4 tiles)
    st.subheader("Machine Statistics")
    
    # Add custom styling for statistic tiles
    st.markdown(
        """
        <style>
        .stat-tile {
            background-color: #FFFFFF;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    stats = st.session_state.machine_stats
    
    with stat_col1:
        st.metric(
            "Total Machines",
            stats.get("total_machines", 100),
            delta=None
        )
    
    with stat_col2:
        st.metric(
            "Healthy Machines",
            stats.get("healthy_machines", 100),
            delta=None,
            delta_color="normal"
        )
    
    with stat_col3:
        st.metric(
            "At Risk",
            stats.get("at_risk", 0),
            delta=None,
            delta_color="off"
        )
    
    with stat_col4:
        st.metric(
            "Critical",
            stats.get("critical", 0),
            delta=None,
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Main Content Area: Chart (Left) and Event Log (Right)
    content_col1, content_col2 = st.columns([0.68, 0.32])
    
    # Machine Health Distribution Chart (Left)
    with content_col1:
        st.subheader("Machine Health Distribution")
        
        health_data = pd.DataFrame({
            "Status": ["Healthy", "At Risk", "Critical"],
            "Count": [
                stats.get("healthy_machines", 100),
                stats.get("at_risk", 0),
                stats.get("critical", 0)
            ]
        })
        
        st.bar_chart(health_data.set_index("Status"), height=300)
    
    # Event Log (Right Side Panel)
    with content_col2:
        st.subheader("Event Log")
        
        # --- Alerts Section ---
        with st.container(border=True):
            st.markdown("#### Alerts")
            
            alerts = st.session_state.alerts
            # Inside your dashboard loop:
            if alerts:
                for alert in alerts[:10]:
                    machine_id = alert.get("machine_id", "Unknown")
                    prob = alert.get("probability", 0)
                    timestamp = alert.get("timestamp", "Just now")
                    
                    # Call the custom renderer
                    render_custom_alert_card(
                        message=f"Machine {machine_id} has a failure probability of {prob:.0%}",
                        timestamp=str(timestamp),
                        severity="critical"
                    )
            else:
                st.caption("No alerts at this time.")

        # Spacer
        st.write("")

        # --- Work Orders Section ---
        with st.container(border=True):
            st.markdown("#### Work Orders")
            
            work_orders = st.session_state.work_orders
            if work_orders:
                for work_order in work_orders[:10]:
                    machine_id = work_order.get("machine_id", "Unknown")
                    rul = work_order.get("rul_hours", "N/A")
                    timestamp = work_order.get("timestamp", "Just now")
                    
                    # Format RUL display
                    if isinstance(rul, (int, float)):
                        rul_display = f"{rul:.1f} hours"
                    else:
                        rul_display = str(rul)
                    
                    render_custom_alert_card(
                        message=f"Work order for machine {machine_id} was created, RUL = {rul_display}",
                        timestamp=str(timestamp),
                        severity="info"
                    )
            else:
                st.caption("No active work orders.")

# -----------------------------------------------------------
# Failure Queue Page
# -----------------------------------------------------------
elif st.session_state.current_page == "Failure Queue":
    # Header with Reload RUL button
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.title("Machines About to Fail")
    
    # with header_col2:
    #     if st.button("Reload RUL", use_container_width=True, type="primary"):
    #         if reload_rul():
    #             st.success("RUL predictions updated!")
    #             st.rerun()
    #         else:
    #             st.error("Failed to reload RUL. Check backend connection.")
    
    # st.markdown("---")
    with header_col2:
        if st.button("Start Simulation", use_container_width=True, 
                     disabled=st.session_state.simulation_running,
                     type="primary"):
            if start_simulation():
                st.success("Simulation completed successfully!")
                st.rerun()
            else:
                st.error("Simulation failed. Check backend connection.")
    
    # Enhanced loading screen
    if st.session_state.simulation_running:
        # Show loading message with spinner
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            st.markdown("### 🔄 Running Simulation")
            st.markdown("Please wait while we process all machines...")
            
            # Progress steps
            progress_col1, progress_col2, progress_col3 = st.columns(3)
            with progress_col1:
                st.markdown("**Loading Data**")
                st.progress(0.33)
            with progress_col2:
                st.markdown("**Running Predictions**")
                st.progress(0.66)
            with progress_col3:
                st.markdown("**Processing Results**")
                st.progress(1.0)
            
            st.info("This process may take 30-60 seconds. Please do not close this page.")
    
    
    # Machines About to Fail Table
    queue = st.session_state.failing_machines_queue
    
    if queue:
        # Sort by RUL (shortest first)
        queue_sorted = sorted(
            queue,
            key=lambda x: float(x["rul_hours"]) if x["rul_hours"] != "N/A" else float('inf')
        )
        
        queue_df = pd.DataFrame(queue_sorted)
        
        # Display table
        st.dataframe(
            queue_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "machineID": st.column_config.TextColumn(
                    "Machine ID",
                    help="Unique machine identifier"
                ),
                "failure_probability": st.column_config.TextColumn(
                    "Failure Probability",
                    help="Probability of failure (0-100%)"
                ),
                "rul_hours": st.column_config.TextColumn(
                    "RUL",
                    help="Remaining Useful Life in hours"
                ),
                "timestamp": st.column_config.TextColumn(
                    "Timestamp",
                    help="Prediction timestamp"
                ),
                "status": st.column_config.TextColumn(
                    "Status",
                    help="Machine status: Critical or Warning"
                )
            }
        )
        
        st.info(f"**Total Machines in Queue**: {len(queue)}")
    else:
        st.info("No machines currently predicted to fail. The system is healthy!")
        st.caption("Run a simulation from the Dashboard to populate the failure queue.")

# # -----------------------------------------------------------
# # Footer
# # -----------------------------------------------------------
# st.markdown("---")
# st.caption("Predictive Maintenance Dashboard | Backend: http://localhost:8000")
