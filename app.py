from components import analysis_question
from utils.db import get_engine
import streamlit as st

@st.cache_resource
def get_engine_cached():
    print("Engine Loaded")
    return get_engine()

try:
    engine = get_engine_cached()
except Exception as e:
    raise RuntimeError(f"Connection Failed: {e}")

st.set_page_config(layout="wide")

st.sidebar.title("Traffic Violations Insight System")
option = st.sidebar.radio(
    "Check Out", ("Dashboard", "Analysis")
)

if option == "Dashboard": st.write("Yet to build")
elif option == "Analysis": analysis_question(st,engine)