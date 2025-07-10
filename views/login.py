import streamlit as st
from config import constants


def login():
    st.set_page_config(page_title="Qlik Script Analyzer - Login", layout="centered", initial_sidebar_state="collapsed")

    with st.form("login_form", clear_on_submit=False):

        # st.title("🔐 Qlik Script Analyzer - Login")

        st.title("🔐 Login")

        username = st.text_input("👤 Username", placeholder="Enter your username")

        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

        submitted = st.form_submit_button("🚀 Login")

        if submitted and username == constants.USERNAME and password == constants.PASSWORD:

            st.session_state.authenticated = True

            st.rerun()

        elif submitted:

            st.error("❌ Invalid credentials")