import streamlit as st
import pandas as pd
from report_utils import (
    load_data_storage,
    load_master_data,
    get_last_pass_data,
    save_total_passes
)

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.sidebar.markdown("🖥️ **Developed by Anant Mandal**")

st.title("📊 Analytics Dashboard – Cold Mill Pass Prediction")

# --- Load Data ---
try:
    uploaded_data = load_data_storage()
    master_data = load_master_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# --- Preview Data ---
with st.expander("📄 Uploaded Data Preview"):
    st.dataframe(uploaded_data)

with st.expander("📄 Master Data Preview"):
    st.dataframe(master_data)

# --- Get Till-Date Passes ---
bliss_passes, davy_passes = get_last_pass_data()
st.info(f"✅ Till-date Passes → Bliss: {bliss_passes}, Davy: {davy_passes}")

# --- Merge Data ---
merged_df = pd.merge(uploaded_data, master_data, on="ID", how="left", suffixes=('', '_master'))

# Convert necessary columns to numeric
merged_df["Bliss Distribution"] = pd.to_numeric(merged_df["Bliss Distribution"], errors="coerce")
merged_df["Davy Distribution"] = pd.to_numeric(merged_df["Davy Distribution"], errors="coerce")
merged_df["Total volume"] = pd.to_numeric(merged_df["Total volume"], errors="coerce")
merged_df["Recovery"] = pd.to_numeric(merged_df["Recovery"], errors="coerce")
merged_df["Bliss Wt"] = pd.to_numeric(merged_df["Bliss Wt"], errors="coerce")
merged_df["Davy Wt"] = pd.to_numeric(merged_df["Davy Wt"], errors="coerce")
merged_df["Bliss Coil Passes"] = pd.to_numeric(merged_df["Bliss Coil Passes"], errors="coerce")
merged_df["Davy Coil Passes"] = pd.to_numeric(merged_df["Davy Coil Passes"], errors="coerce")



# Step 1: Bliss Vol and Davy Vol
merged_df["Bliss Vol"] = ((merged_df["Bliss Distribution"].fillna(0) * merged_df["Total volume"]) / 100).round(2)
merged_df["Davy Vol"] = ((merged_df["Davy Distribution"].fillna(0) * merged_df["Total volume"]) / 100).round(2)

# Step 2: Bliss_Coil_Wt and Davy_Coil_Wt
merged_df["Bliss_Coil_Wt"] = ((merged_df["Bliss Wt"].fillna(0) * merged_df["Recovery"].fillna(0)) / 100).round(2)
merged_df["Davy_Coil_Wt"] = ((merged_df["Davy Wt"].fillna(0) * merged_df["Recovery"].fillna(0)) / 100).round(2)

# Step 3: Number of coils
merged_df["Bliss No of coils"] = (merged_df["Bliss Vol"] / merged_df["Bliss_Coil_Wt"]).replace([float('inf'), -float('inf')], 0).fillna(0).round(2)
merged_df["Davy No of coils"] = (merged_df["Davy Vol"] / merged_df["Davy_Coil_Wt"]).replace([float('inf'), -float('inf')], 0).fillna(0).round(2)

# Step 4: Number of passes
merged_df["Bliss Number of passes"] = (merged_df["Bliss No of coils"] * merged_df["Bliss Coil Passes"]).fillna(0).round(2)
merged_df["Davy Number of passes"] = (merged_df["Davy No of coils"] * merged_df["Davy Coil Passes"]).fillna(0).round(2)

# Step 5: MIS Summary
bliss_total_pass = merged_df["Bliss Number of passes"].sum().round(0)
davy_total_pass = merged_df["Davy Number of passes"].sum().round(0)

st.subheader("📋 MIS Summary")
col1, col2 = st.columns(2)
col1.metric("🔄 Bliss Total Passes", f"{int(bliss_total_pass):,}")
col2.metric("🔄 Davy Total Passes", f"{int(davy_total_pass):,}")

# Confirm and Save
if st.button("✅ Confirm and Save Total Passes"):
    save_total_passes(bliss_total_pass, davy_total_pass)
    st.success("Total passes saved successfully.")

# --- Final Calculated Table ---
st.subheader("🧾 Detailed Pass Calculation Table")
st.dataframe(merged_df)

# --- Optional CSV Export ---
csv_data = merged_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Output as CSV", data=csv_data, file_name="pass_prediction_output.csv", mime="text/csv")
