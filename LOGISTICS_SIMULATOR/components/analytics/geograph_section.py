import streamlit as st 
import pydeck as pdk
import pandas as pd 
from classes.analytics.analytics_data import Analytics_data
from classes.analytics.analytics_state import Analytics_state

def geograph_section(analytics_data: Analytics_data, analytics_state: Analytics_state):
    
    st.subheader("🌐 Global Route Visualization")
    
    df = analytics_data.get_port_coordinate()
    df["line_width"] = 4.0
    layer = pdk.Layer(
        "ArcLayer",
        data=df,
        get_source_position="[origin_lon, origin_lat]", 
        get_target_position="[dest_lon, dest_lat]", 
        get_source_color="color_rgb",             
        get_target_color="color_rgb",             
        get_width="line_width", 
        pickable=False,         
    )
    
    view_state = pdk.ViewState(
        latitude=35.0, 
        longitude=-20.0, 
        zoom=1.2, 
        pitch=45, 
        bearing=0
    )
    
    with st.container(border=True):
        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                # map_style="mapbox://styles/mapbox/navigation-day-v1"
            )
        )