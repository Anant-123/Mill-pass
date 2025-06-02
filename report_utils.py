import os
import pandas as pd
from datetime import datetime

DATA_STORAGE_PATH = "Data_storage.xlsx"
DATA_STORAGE_SHEET = "Loading"
PASS_DATA_CSV = "pass_data.csv"

def get_data_storage_timestamp():
    try:
        timestamp = os.path.getmtime(DATA_STORAGE_PATH)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except FileNotFoundError:
        return "File not found"

def get_pass_data_timestamp():
    try:
        timestamp = os.path.getmtime(PASS_DATA_CSV)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except FileNotFoundError:
        return "File not found"

def load_uploaded_file(uploaded_file):
    return pd.read_excel(uploaded_file)

def load_data_storage():
    return pd.read_excel(DATA_STORAGE_PATH, sheet_name=DATA_STORAGE_SHEET)

def save_pass_data(bliss_passes, davy_passes):
    df = pd.DataFrame([{
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Bliss Passes': bliss_passes,
        'Davy Passes': davy_passes
    }])
    df.to_csv(PASS_DATA_CSV, index=False)

def get_last_pass_data():
    try:
        df = pd.read_csv(PASS_DATA_CSV)
        if not df.empty:
            latest_row = df.iloc[-1]
            return int(latest_row['Bliss Passes']), int(latest_row['Davy Passes'])
    except Exception:
        pass
    return 0, 0  # default values if file doesn't exist or is empty

def load_master_data():
    """Load the Master sheet from Data_storage.xlsx."""
    return pd.read_excel(DATA_STORAGE_PATH, sheet_name="Master")

def save_total_passes(bliss_total_pass, davy_total_pass):
    total_pass_csv = "total_passes.csv"
    
    data = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bliss_total_pass": int(bliss_total_pass),
        "davy_total_pass": int(davy_total_pass)
    }])
    
    data.to_csv(total_pass_csv, index=False)  # Overwrite the file with single row


