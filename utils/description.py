import pandas as pd
import re

def clean_description(val):
    if pd.isna(val): return None

    val = str(val).strip().title()
    val = re.sub(r'\s+', ' ', val) # Removing Extra spaces

    if val.isdigit(): return f"Vehicle Speed Of {val}"
    if val[:-1].isdigit() and val.endswith("+"): return f"Vehicle Speed Of {val}"
    if val == "Sus" or val == "Susp": val = "Suspicious"
    if len(val) < 5: return None # Filtering Noise

    return val