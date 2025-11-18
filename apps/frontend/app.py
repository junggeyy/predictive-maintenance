import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# Page Setup
# -----------------------------------------------------------
st.set_page_config(
    page_title="Predictive Maintenance Simulation",
    layout="wide",
)

st.title("Predictive Maintenance Simulation Dashboard")

# -----------------------------------------------------------
# Dashboard Overview
# -----------------------------------------------------------
st.subheader("System Overview")

colA, colB, colC, colD = st.columns(4)

with colA:
    st.metric("Number of Machines", "100")

with colB:
    st.metric("Recent Failures", "12")  # placeholder

with colC:
    st.metric("Predicted Failures (Next 24h)", "4")  # placeholder

with colD:
    st.metric("Active Work Orders", "7")  # placeholder


st.markdown("---")


# -----------------------------------------------------------
# Simulation Trigger
# -----------------------------------------------------------
st.subheader("Simulation Control")

if st.button("🚀 Start Simulation"):
    st.success("Simulation running... (dummy placeholder)")
else:
    st.info("Click 'Start Simulation' to begin analyzing test dataset.")


st.markdown("---")

# -----------------------------------------------------------
# Main Layout: Left = MCP Logs, Right = Charts
# -----------------------------------------------------------
left_col, right_col = st.columns([0.32, 0.68])


# -----------------------------------------------------------
# LEFT PANEL — MCP Logs
# -----------------------------------------------------------
with left_col:
    st.subheader("MCP Event Log")

    st.markdown(
        """
        <style>
            .log-box {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
                padding: 12px;
                height: 450px;
                overflow-y: auto;
                border-radius: 6px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    logs = [
        "[00:00] Simulation initialized",
        "[00:05] Machine 23 flagged: high error rate",
        "[00:05] → MCP Alert Created",
        "[00:06] → Work Order #1032 generated",
        "[00:10] Machine 78 predicted to fail in 12h",
        "[00:10] → MCP Notification sent",
    ]

    st.markdown('<div class="log-box">', unsafe_allow_html=True)
    for log in logs:
        st.write(log)
    st.markdown('</div>', unsafe_allow_html=True)



# -----------------------------------------------------------
# RIGHT PANEL — Charts & Machine Status
# -----------------------------------------------------------
with right_col:

    st.subheader("Machine Health Summary")

    # Machines performing well vs failing (dummy pie chart)
    status_data = pd.DataFrame({
        "status": ["Healthy", "At Risk", "Likely Failure"],
        "count": [88, 8, 4]
    })

    st.bar_chart(status_data, x="status", y="count")

    st.subheader("Selected Sensor Trends (Placeholder)")

    sensor_df = pd.DataFrame({
        "timestamp": range(10),
        "volt": np.random.uniform(210, 230, 10),
        "vibration": np.random.uniform(0.2, 1.0, 10),
        "temp": np.random.uniform(50, 80, 10)
    }).set_index("timestamp")

    st.line_chart(sensor_df)


# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption("Simulation dashboard using test dataset. Backend integration coming soon.")
