import streamlit as st
from classes.setup.setup_state import Setup_state
from classes.setup.setup_data import Setup_data
def form_countries(setup_state: Setup_state, setup_data: Setup_data, country):
    with st.form("form_countries"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("origin", country, key='_origin_country')
        with col2: 
            st.selectbox("destination", sorted(country, reverse=True), key='_destination_country')
        st.form_submit_button(
            "submit", 
            key='f_countries', 
            on_click=setup_state.store_status_value, 
            args=['f_countries']
        )
    if st.session_state['f_countries']:
        setup_state.store_value('origin_country')
        setup_state.store_value('destination_country')
        
    return 