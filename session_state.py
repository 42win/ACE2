import streamlit as st

# Menangani status login menggunakan session state
class SessionState:
    def __init__(self):
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        if 'username' not in st.session_state:
            st.session_state['username'] = ""

    def login(self, username):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username

    def logout(self):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""

    def is_logged_in(self):
        return st.session_state['logged_in']

# Inisialisasi sesi
session_state = SessionState()
