import pandas as pd
import re

def clean_time_of_stop(val):
    if pd.isna(val): return None

    # Replace non numeric values to ':'
    time_stamp = re.sub(r'[^0-9]', ':', str(val).strip())
    time_stamp_parts = time_stamp.split(':')

    if len(time_stamp_parts) == 3: hh, mm, ss = time_stamp_parts
    else: return None  

    # Fixing timing (5 -> 05)
    hh = hh.zfill(2)
    mm = mm.zfill(2)
    ss = ss.zfill(2)
    time_stamp = f"{hh}:{mm}:{ss}"

    return pd.to_datetime(time_stamp, format="%H:%M:%S", errors="coerce").time()
