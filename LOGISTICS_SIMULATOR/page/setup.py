from snowflake.snowpark.context import get_active_session
import streamlit as st 
import pandas as pd 
from components.setup.form_template import form_template
from components.setup.form_countries import form_countries
from classes.setup.setup_data import Setup_data
from classes.setup.setup_state import Setup_state

def setup():
    setup_data = Setup_data()
    setup_state = Setup_state() 

    country = setup_data.get_country_list
    if 'origin_country' not in st.session_state:
        st.session_state['origin_country'] = country[0]
    if 'origin_country' not in st.session_state:
        st.session_state['destination_country'] = country[-1]
    
    st.header("⚙️SETUP")
    st.subheader("🌏 COUNTRY")

    form_countries(setup_state, setup_data, country)
    
    air, ship,road, rail = st.columns(4)
    with air: 
        st.subheader('✈️ AIRPLANE')
        if st.session_state["status_f_air_vehicle"]:
            st.success('COMPLETED', icon="✅")
        else: 
            st.warning("NOT COMPLETED" ,icon="🚨")
        form_template(setup_state, setup_data, 'air')
    with ship: 
        st.subheader('🚢 SHIP')
        if st.session_state["status_f_sea_vehicle"]:
            st.success('COMPLETED', icon="✅")
        else: 
            st.warning("NOT COMPLETED" ,icon="🚨")
        form_template(setup_state, setup_data, 'sea')
    with road:
        st.subheader('🚚 ROAD')
        if st.session_state["status_f_road_vehicle"]:
            st.success('COMPLETED', icon="✅")
        else: 
            st.warning("NOT COMPLETED" ,icon="🚨")
        form_template(setup_state, setup_data, 'road')
    with rail: 
        st.subheader('🚃 RAIL')
        if st.session_state["status_f_rail_vehicle"]:
            st.success('COMPLETED', icon="✅")
        else: 
            st.warning("NOT COMPLETED" ,icon="🚨")
        form_template(setup_state, setup_data, 'rail')
    return