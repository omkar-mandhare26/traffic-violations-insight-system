import pandas as pd
import re

def clean_location(val):
    if pd.isna(val): return None
    val = str(val)

    if len(val) < 5: return None

    # Removing mutiple spaces
    val = re.sub(r'\s+', ' ', val).strip()

    # Standardizing '/' with '@' with correct spaces
    val = re.sub(r'\s*[/@]\s*', ' @ ', val)

    # Removing non-alphanumeric characters from the start & end
    val = re.sub(r'^\s*@\s*', '', val)
    val = re.sub(r'\s*@\s*$', '', val)
    val = re.sub(r'^[^A-Za-z0-9]+', '', val)
    val = re.sub(r'[^A-Za-z0-9]+$', '', val)

    # Final Cleanup
    val = re.sub(r'\s+', ' ', val).strip()

    return val