import streamlit as st 
class Setup_state:
    def __init__(self):
        session_state_key_dict = {
            "f_countries_disable": False,
            "origin_country" : "USA", 
            "destination_country" : "KOREA", 
            "air_distance": '',
            "f_countries": False,
            "f_ports": False,
            "f_bases": False,
            'f_vehicles': False,
            "status_f_countries": False,
            "status_f_air_base": False,
            "status_f_air_port": False,
            "status_f_air_vehicle": False,
            "status_f_sea_base": False,
            "status_f_sea_port": False,
            "status_f_sea_vehicle": False,
            "status_f_road_base": False,
            "status_f_road_port": False,
            "status_f_road_vehicle": False,
            "status_f_rail_base": False,
            "status_f_rail_port": False,
            "status_f_rail_vehicle": False,
            "air_origin_base": '',
            "air_dist_base": ''
        }
        for key, val in session_state_key_dict.items():
            if key not in st.session_state:
                st.session_state[key] = val
    
    def load_value(self, key_name):
        widget_key = '_' + key_name
        if key_name in st.session_state:
            st.session_state[widget_key] = st.session_state[key_name]
        
    def store_value(self, key_name):
        widget_key = '_' + key_name
        if widget_key in st.session_state:
            st.session_state[key_name] = st.session_state[widget_key]
            
    def store_status_value(self, key_name):
        widget_key = 'status' + '_' + key_name
        st.session_state[widget_key] = True

    @property 
    def get_value(self, key_name):
        if key_name in st.session_state:
            return st.session_state[key_name]