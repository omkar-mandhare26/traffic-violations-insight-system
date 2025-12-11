import pandas as pd

def clean_latitude(val):
    if pd.isna(val): return None

    if val < 18.9 or val > 71 or int(val) == 0: return None
    return val

def clean_longitude(val):
    if pd.isna(val): return None

    if val < -124.67 or val > -66.95 or int(val) == 0: return None
    return val