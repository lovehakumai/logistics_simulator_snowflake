import streamlit as st 
from page.setup import setup
from page.home_page import home_page
from page.analytics import analytics
from page.monitor import monitor
def selected_page():
    if st.session_state['current_page'] == 'setup':
        setup() 
    elif st.session_state['current_page'] == 'analytics':
        analytics()
    elif st.session_state['current_page'] == 'monitor':
        monitor()