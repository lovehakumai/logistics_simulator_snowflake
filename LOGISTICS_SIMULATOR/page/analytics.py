from snowflake.snowpark.context import get_active_session
import streamlit as st 
import pandas as pd 
from classes.analytics.analytics_state import Analytics_state
from classes.analytics.analytics_data import Analytics_data
from components.analytics.cost_section import cost_section
from components.analytics.past_section import past_section
from components.analytics.geograph_section import geograph_section

def analytics():
    analytics_state = Analytics_state() 
    analytics_state.setup_check()
    
    st.title("📈 Logistics Simulator")
    
    if not st.session_state['setup_check_flg']:
        st.warning("Setup is not Completed", icon="🚨")
        st.write("Go back to ⚙️SETUP Page and setup rest of the parameters")
        return
    else:
        analytics_data = Analytics_data()
        
    origin_country = analytics_state.get_value('origin_country')
    destination_country = analytics_state.get_value('destination_country')
        
    route_html = f"""
    <div style="
        display: flex; 
        align-items: center; 
        justify-content: space-around;
        width: 100%;
        gap: 15px; 
        font-family: sans-serif;
        margin: 20px auto;
    ">
        <div style="
            border: 2px solid #1E3A8A; 
            background-color: #F0FDF4; 
            padding: 10px 20px; 
            border-radius: 8px; 
            font-weight: bold; 
            font-size: 1.2rem;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        ">
            {origin_country}
        </div>
    
        <div style="
            font-size: 1.8rem; 
            color: #4B5563;
            font-weight: bold;
        ">
            ➔
        </div>
    
        <div style="
            border: 2px solid #1E3A8A; 
            background-color: #EFF6FF; 
            padding: 10px 20px; 
            border-radius: 8px; 
            font-weight: bold; 
            font-size: 1.2rem;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        ">
            {destination_country}
        </div>
    </div>
    """
    
    st.html(f"{route_html}")   
    
    cost_section(analytics_data, analytics_state)
    st.write('---')
    past_section(analytics_data, analytics_state)
    st.write('---')
    geograph_section(analytics_data, analytics_state)    