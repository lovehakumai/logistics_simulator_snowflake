import streamlit as st 
class Analytics_state:
    def __init__(self):
        analytics_param_dict = {
            'fuel_increase_param':1.0,
            'risk_avoidance_param':1.0,
            'weight_t':20,
            'setup_check_flg': False
        }
        for key, val in analytics_param_dict.items():
            if key not in st.session_state:
                st.session_state[key] = val 

    def setup_check(self):
        setup_param_keys = [
            # Countries
            "origin_country",
            "destination_country",
            # Base Points
            "air_origin_base",
            "sea_origin_base",
            "road_origin_base",
            "rail_origin_base",
            "air_dest_base",
            "sea_dest_base",
            "road_dest_base",
            "rail_dest_base",
            # Port Names
            "air_origin_port",
            "sea_origin_port",
            "road_origin_port",
            "rail_origin_port",
            "air_dest_port",
            "sea_dest_port",
            "road_dest_port",
            "rail_dest_port",
            # Vehicle Params
            "air_distance",
            "air_vehicle_type",
            "air_fuel_type",
            "sea_size",
            "sea_vehicle_type",
            "sea_fuel_type",
            "road_vehicle_type",
            "road_fuel_type",
            "rail_vehicle_type",
            "rail_fuel_type",
        ]
        index = 0 
        for i in setup_param_keys:
            if i in st.session_state:
                index += 1 
        if index == len(setup_param_keys):
            self.setup_check_flg = True
            
    def load_value(self, key_name):
        widget_key = '_' + key_name
        if key_name in st.session_state:
            st.session_state[widget_key] = st.session_state[key_name]
        
    def store_value(self, key_name):
        widget_key = '_' + key_name
        if widget_key in st.session_state:
            st.session_state[key_name] = st.session_state[widget_key]
            
    def get_value(self, key_name):
        if key_name in st.session_state:
            return st.session_state[key_name]