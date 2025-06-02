import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from calendar import monthrange

# === Load data ===
pass_df = pd.read_csv("pass_data.csv")
total_df = pd.read_csv("total_passes.csv")

# Get latest entries
latest_passes = pass_df.iloc[-1]
latest_totals = total_df.iloc[-1]

# Extract values
bliss_till_date = latest_passes["Bliss Passes"]
davy_till_date = latest_passes["Davy Passes"]
bliss_total_req = latest_totals["bliss_total_pass"]
davy_total_req = latest_totals["davy_total_pass"]

# === Date calculations ===
today = datetime.now()
days_till_now = today.day-1
_, total_days_in_month = monthrange(today.year, today.month)
balance_days = total_days_in_month - days_till_now

# === Calculated Metrics ===
bliss_avg = bliss_till_date / days_till_now if days_till_now > 0 else 0
davy_avg = davy_till_date / days_till_now if days_till_now > 0 else 0

bliss_balance_passes = bliss_total_req - bliss_till_date
davy_balance_passes = davy_total_req - davy_till_date

bliss_req_per_day = bliss_balance_passes / balance_days if balance_days > 0 else 0
davy_req_per_day = davy_balance_passes / balance_days if balance_days > 0 else 0

# === Layout ===
# Add footer in the sidebar

st.set_page_config(page_title="Passes Dashboard", layout="wide")

st.sidebar.markdown("🖥️ **Developed by Anant Mandal**")
st.markdown("<h1 style='text-align:center;'>🏎️🏁 Cold Mill Performance Dashboard 🏎️🏁</h1>", unsafe_allow_html=True)

# === Row 1: Gauges & Asking Rate ===
col1, col2 = st.columns(2)

with col1:
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(bliss_avg, 0),
        number={'valueformat': '.0f'},
        title={'text': "Avg. Passes/Day – Bliss"},
        gauge={
            'axis': {'range': [0, max(bliss_avg * 2, 50)]},
            'bar': {'color': "blue"}
        }
    ))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        f"""
        <div style='background-color:#001f3f; padding:10px; border-radius:10px; text-align:center; margin-top:10px;'>
            <h4 style='color:white; margin:0;'>🏁 Asking Rate – Bliss</h4>
            <p style='font-size:36px; color:#00d4ff; margin:0; font-weight:bold;'>{bliss_req_per_day:.0f} passes/day</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(davy_avg, 0),
        number={'valueformat': '.0f'},
        title={'text': "Avg. Passes/Day – Davy"},
        gauge={
            'axis': {'range': [0, max(davy_avg * 2, 50)]},
            'bar': {'color': "green"}
        }
    ))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        f"""
        <div style='background-color:#003300; padding:10px; border-radius:10px; text-align:center; margin-top:10px;'>
            <h4 style='color:white; margin:0;'>🏁 Asking Rate – Davy</h4>
            <p style='font-size:36px; color:#00ff88; margin:0; font-weight:bold;'>{davy_req_per_day:.0f} passes/day</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# === Row 2: Summary Tables (clean and compact) ===
col3, col4 = st.columns(2)

with col3:
    st.markdown("<h5 style='color:blue; margin-top:10px;'>📋 Bliss Summary</h5>", unsafe_allow_html=True)
    bliss_table = pd.DataFrame({
        "Metric": [
            "Total passes till date",
            "Current avg. passes/day",
            "Passes required for balance days",
            "Required passes/day"
        ],
        "Value": [
            int(bliss_till_date),
            f"{bliss_avg:.0f}",
            int(bliss_balance_passes),
            f"{bliss_req_per_day:.0f}"
        ]
    })
    st.table(bliss_table)

with col4:
    st.markdown("<h5 style='color:green; margin-top:10px;'>📋 Davy Summary</h5>", unsafe_allow_html=True)
    davy_table = pd.DataFrame({
        "Metric": [
            "Total passes till date",
            "Current avg. passes/day",
            "Passes required for balance days",
            "Required passes/day"
        ],
        "Value": [
            int(davy_till_date),
            f"{davy_avg:.0f}",
            int(davy_balance_passes),
            f"{davy_req_per_day:.0f}"
        ]
    })
    st.table(davy_table)


