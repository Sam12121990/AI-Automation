import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Clear session and rerun
st.session_state.authenticated = False

# Show logout message
st.success("You have been logged out. Redirecting to login...")

# Auto-redirect after 3 seconds
st.markdown("""<meta http-equiv="refresh" content="3; url=./">""", unsafe_allow_html=True)