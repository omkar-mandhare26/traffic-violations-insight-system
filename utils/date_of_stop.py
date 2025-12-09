import pandas as pd

def clean_date_of_stop(val):
    today = pd.Timestamp.today()
    date_of_stop = pd.to_datetime(str(val).strip(),errors="coerce")

    if pd.isna(date_of_stop): return None
    if date_of_stop > today: return None
    if date_of_stop.year > today.year + 1: return None
    
    return date_of_stop