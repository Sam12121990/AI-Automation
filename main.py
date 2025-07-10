import streamlit as st
from views.login import login

# ✅ Initialize session state keys if not already set

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# ---- PAGE SETUP ------

qlik_script_assessment = st.Page(
    page="views/script_assessment.py",
    title="Qlik Script Assessment",
    icon=":material/monitoring:",
    default=True,
)

qlik_script_flow_analyzer = st.Page(
    page="views/script_flow_analyzer.py",
    title="Qlik Script Flow Analyzer",
    icon=":material/bar_chart:",
)

horizontal_timeline_chart = st.Page(
    page="views/horizontal_timeline_chart.py",
    title="Horizontal Timeline Chart",
    icon=":material/download:",
)

logout = st.Page(
    page="views/logout.py",
    title="Logout",
    icon=":material/logout:",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(pages=[qlik_script_assessment, qlik_script_flow_analyzer, horizontal_timeline_chart, logout])

# --- RUN NAVIGATION ---
pg.run()