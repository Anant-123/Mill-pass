# data_upload.py

import streamlit as st
import pandas as pd
from report_utils import get_data_storage_timestamp, load_uploaded_file, load_data_storage
from report_utils import get_last_pass_data, save_pass_data, get_pass_data_timestamp

DATA_STORAGE_PATH = "Data_storage.xlsx"
DATA_STORAGE_SHEET = "Loading"
st.set_page_config(page_title="Upload page", layout="wide")

st.sidebar.markdown("🖥️ **Developed by Anant Mandal**")


st.title("📥 Data Upload and Manual Entry")

# Display last update timestamp
st.markdown(f"**🕒 Last updated 'Data_storage.xlsx':** `{get_data_storage_timestamp()}`")

# File uploader
uploaded_file = st.file_uploader("Upload Monthly Loading File (with ID, Product Category, Total volume, Recovery)", type=["xlsx"])

if uploaded_file:
    try:
        # Load both dataframes
        uploaded_df = load_uploaded_file(uploaded_file)
        storage_df = load_data_storage()

        # Merge only on ID to check which exist
        common_ids = uploaded_df['ID'].isin(storage_df['ID'])
        unmatched_rows = uploaded_df[~common_ids]

        if not unmatched_rows.empty:
            st.warning("⚠️ Some IDs in the uploaded file were not found in the data storage!")
            st.dataframe(unmatched_rows[['ID', 'Product Category']])
        else:
            st.success("✅ All IDs matched successfully.")

        # Update matching rows
        updated_storage_df = storage_df.copy()
        updated_storage_df.set_index('ID', inplace=True)

        for _, row in uploaded_df.iterrows():
            if row['ID'] in updated_storage_df.index:
                updated_storage_df.at[row['ID'], 'Total volume'] = row['Total volume']
                updated_storage_df.at[row['ID'], 'Recovery'] = row['Recovery']

        updated_storage_df.reset_index(inplace=True)

        # Save updated file
        with pd.ExcelWriter(DATA_STORAGE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            updated_storage_df.to_excel(writer, sheet_name=DATA_STORAGE_SHEET, index=False)

        st.success("💾 Data_storage.xlsx updated successfully with new Total volume and Recovery.")

        # Store in session state
        st.session_state['matched_data'] = updated_storage_df

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
else:
    st.info("Please upload your monthly loading file to begin.")





# Load last values if any
last_bliss, last_davy = get_last_pass_data()

st.markdown(f"**🕒 Last updated 'pass_data.csv':** `{get_pass_data_timestamp()}`")

# Manual Entry for Till-date Passes with pre-filled values
st.subheader("✍️ Enter Till-date Number of Passes")

bliss_passes = st.number_input("Till-date Passes – Bliss Mill", min_value=0, step=1, value=last_bliss)
davy_passes = st.number_input("Till-date Passes – Davy Mill", min_value=0, step=1, value=last_davy)

if st.button("✅ Confirm Inputs"):
    # Store in session state
    st.session_state['bliss_passes'] = bliss_passes
    st.session_state['davy_passes'] = davy_passes

    # Save to CSV
    save_pass_data(bliss_passes, davy_passes)

    st.success("📝 Passes for Bliss and Davy recorded and saved successfully.")
