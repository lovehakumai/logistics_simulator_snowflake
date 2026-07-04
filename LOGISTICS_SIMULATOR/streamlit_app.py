from snowflake.snowpark.context import get_active_session
import streamlit as st 
import pandas as pd 
from form_components.form_air import form_air
from form_components.form_ship import form_ship
from form_components.form_road import form_road
from form_components.form_rail import form_rail

def store_value(key):
    st.session_state[key] = st.session_state['_' + key]
def store_form_result(key):
    st.session_state['status_' + key] = True 
def load_value(key):
    st.session_state['_' + key] = st.session_state[key]
def init_value(key, init_val):
    if key not in st.session_state:
        st.session_state[key] = init_val 

session_state_key_dict = {
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
}

session_state_key_list = list(session_state_key_dict.keys())

for i in session_state_key_list:
    init_value(i, session_state_key_dict[i])

session = get_active_session()
session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()

mode_dim = session.sql("SELECT * FROM KAGGLE_LOGISTICS.DEV_ANALYTICS.MRT__DIM_MODE_FACTOR").to_pandas()
country_dim = session.sql("SELECT * FROM KAGGLE_LOGISTICS.DEV_ANALYTICS.MRT__DIM_COUNTRY_FACTOR").to_pandas()

def get_base_point(country_dim, country_name):
    df = country_dim[country_dim['COUNTRY_NAME'] == country_name]
    air_list = df[df["TRANSPORT_MODE"] == 'AIR']['BASE_POINT'].unique()
    sea_list = df[df["TRANSPORT_MODE"] == 'SEA']['BASE_POINT'].unique()
    road_list = df[df["TRANSPORT_MODE"] == 'ROAD']['BASE_POINT'].unique()
    rail_list = df[df["TRANSPORT_MODE"] == 'RAIL']['BASE_POINT'].unique()
    return {"AIR":air_list, "SEA":sea_list, "ROAD":road_list, "RAIL":rail_list}

def get_port_name(country_dim, base_name):
    result_list = country_dim[country_dim['BASE_POINT'] == base_name]['PORT_NAME_EN'].unique()
    return result_list

air_mode_dim = mode_dim[mode_dim['TRANSPORT_MODE'] == "AIR"]
sea_mode_dim = mode_dim[mode_dim['TRANSPORT_MODE'] == "SEA"]
road_mode_dim = mode_dim[mode_dim['TRANSPORT_MODE'] == "ROAD"]
rail_mode_dim = mode_dim[mode_dim['TRANSPORT_MODE'] == "RAIL"]

country = country_dim['COUNTRY_NAME'].unique()

air_vehicle = air_mode_dim['VEHICLE_TYPE'].unique()
sea_vehicle = sea_mode_dim['VEHICLE_TYPE'].unique()
road_vehicle = road_mode_dim['VEHICLE_TYPE'].unique()
rail_vehicle = rail_mode_dim['VEHICLE_TYPE'].unique()

air_fuel = air_mode_dim['FUEL_TYPE'].unique()
sea_fuel = sea_mode_dim['FUEL_TYPE'].unique()
road_fuel = road_mode_dim['FUEL_TYPE'].unique()
rail_fuel = rail_mode_dim['FUEL_TYPE'].unique()

air_distance = air_mode_dim['AIR_DISTANCE'].unique()
sea_size = sea_mode_dim['SEA_SIZE'].unique()
fuel_type = mode_dim['FUEL_TYPE'].unique()

st.session_state['origin_country'] = country[0]
st.session_state['destination_country'] = country[-1]

st.header("⚙️SETUP")
st.subheader("🌏 COUNTRY")
with st.form("f_countries"):
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("origin", country, key='_origin_country')
    with col2: 
        st.selectbox("destination", sorted(country, reverse=True), key='_destination_country')
    st.form_submit_button("submit", key='f_countries', on_click=store_form_result, args=['f_countries'])

if st.session_state['f_countries']:
    store_value('origin_country')
    store_value('destination_country')

origin_base_dict = get_base_point(country_dim, st.session_state['origin_country'])
destination_base_dict = get_base_point(country_dim, st.session_state['destination_country'])

# =================================================================================
# AIRPLANE
# =================================================================================
st.subheader('✈️ AIRPLANE')
if not st.session_state['status_f_countries']:
    st.write('Please Chose Country First.')
else:
    st.write('BASE POINT')
    with st.form('f_air_base'):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("ORIGIN", origin_base_dict["AIR"], key='_air_origin_base')
        with col2:
            st.selectbox("DESTINATION", destination_base_dict["AIR"], key='_air_dist_base')
        st.form_submit_button("submit", key="f_air_base", on_click=store_form_result, args=['f_air_base'])
    if st.session_state['f_air_base']:
        store_value('air_origin_base')
        store_value('air_dist_base')

    if not st.session_state['status_f_air_base']:
        st.write('Chose Base Point First')
    else:
        origin_air_port = get_port_name(country_dim, st.session_state['air_origin_base'])        
        destination_air_port = get_port_name(country_dim, st.session_state['air_dist_base'])
        st.write('PORTS')
        with st.form('f_air_port'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_air_port, key='_air_origin_port')
            with col2:
                st.selectbox("DESTINATION", destination_air_port, key='_air_dist_port')
            st.form_submit_button("submit", key="f_air_port", on_click=store_form_result, args=['f_air_port'])
        if st.session_state['f_air_port']:
            store_value('air_origin_port')
            store_value('air_dist_port')

        if not st.session_state['status_f_air_port']:
            st.write('Chose Ports First')
        else:
            st.write('VEHICLE SETUP')
            with st.form('f_air_vehicle'):
                st.selectbox("DISTANCE", air_distance, key='_air_distance')
                st.selectbox("VEHICLE_TYPE", air_vehicle, key='_air_vehicle_type')
                st.selectbox("FUEL_TYPE", air_fuel, key='_air_fuel_type')
                st.form_submit_button("submit", key="f_air_vehicle", on_click=store_form_result, args=['f_air_vehicle'])
            if st.session_state['status_f_air_vehicle']:
                store_value('air_distance')
                store_value('air_vehicle_type')
                store_value('air_fuel_type')

# =================================================================================
# SHIP
# =================================================================================
st.subheader('🚢 SHIP')
if not st.session_state['status_f_countries']:
    st.write('Please Chose Country First.')
else:
    st.write('BASE POINT')
    with st.form('f_sea_base'):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("ORIGIN", origin_base_dict["SEA"], key='_sea_origin_base')
        with col2:
            st.selectbox("DESTINATION", destination_base_dict["SEA"], key='_sea_dist_base')
        st.form_submit_button("submit", key="f_sea_base", on_click=store_form_result, args=['f_sea_base'])
    if st.session_state['f_sea_base']:
        store_value('sea_origin_base')
        store_value('sea_dist_base')

    if not st.session_state['status_f_sea_base']:
        st.write('Chose Base Point First')
    else:
        origin_sea_port = get_port_name(country_dim, st.session_state['sea_origin_base'])        
        destination_sea_port = get_port_name(country_dim, st.session_state['sea_dist_base'])
        st.write('PORTS')
        with st.form('f_sea_port'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_sea_port, key='_sea_origin_port')
            with col2:
                st.selectbox("DESTINATION", destination_sea_port, key='_sea_dist_port')
            st.form_submit_button("submit", key="f_sea_port", on_click=store_form_result, args=['f_sea_port'])
        if st.session_state['f_sea_port']:
            store_value('sea_origin_port')
            store_value('sea_dist_port')

        if not st.session_state['status_f_sea_port']:
            st.write('Chose Ports First')
        else:
            st.write('VEHICLE SETUP')
            with st.form('f_sea_vehicle'):
                st.selectbox("SIZE", sea_size, key='_sea_size')
                st.selectbox("VEHICLE_TYPE", sea_vehicle, key='_sea_vehicle_type')
                st.selectbox("FUEL_TYPE", sea_fuel, key='_sea_fuel_type')
                st.form_submit_button("submit", key="f_sea_vehicle", on_click=store_form_result, args=['f_sea_vehicle'])
            if st.session_state['status_f_sea_vehicle']:
                store_value('sea_size')
                store_value('sea_vehicle_type')
                store_value('sea_fuel_type')

# =================================================================================
# ROAD
# =================================================================================
st.subheader('🚚 ROAD')
if not st.session_state['status_f_countries']:
    st.write('Please Chose Country First.')
else:
    st.write('BASE POINT')
    with st.form('f_road_base'):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("ORIGIN", origin_base_dict["ROAD"], key='_road_origin_base')
        with col2:
            st.selectbox("DESTINATION", destination_base_dict["ROAD"], key='_road_dist_base')
        st.form_submit_button("submit", key="f_road_base", on_click=store_form_result, args=['f_road_base'])
    if st.session_state['f_road_base']:
        store_value('road_origin_base')
        store_value('road_dist_base')

    if not st.session_state['status_f_road_base']:
        st.write('Chose Base Point First')
    else:
        origin_road_port = get_port_name(country_dim, st.session_state['road_origin_base'])        
        destination_road_port = get_port_name(country_dim, st.session_state['road_dist_base'])
        st.write('PORTS')
        with st.form('f_road_port'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_road_port, key='_road_origin_port')
            with col2:
                st.selectbox("DESTINATION", destination_road_port, key='_road_dist_port')
            st.form_submit_button("submit", key="f_road_port", on_click=store_form_result, args=['f_road_port'])
        if st.session_state['f_road_port']:
            store_value('road_origin_port')
            store_value('road_dist_port')

        if not st.session_state['status_f_road_port']:
            st.write('Chose Ports First')
        else:
            st.write('VEHICLE SETUP')
            with st.form('f_road_vehicle'):
                st.selectbox("VEHICLE_TYPE", road_vehicle, key='_road_vehicle_type')
                st.selectbox("FUEL_TYPE", road_fuel,  key='_road_fuel_type')
                st.form_submit_button("submit", key="f_road_vehicle", on_click=store_form_result, args=['f_road_vehicle'])
            if st.session_state['status_f_road_vehicle']:
                store_value('road_vehicle_type')
                store_value('road_fuel_type')
                
# =================================================================================
# RAIL
# =================================================================================
st.subheader('🚃 RAIL')
if not st.session_state['status_f_countries']:
    st.write('Please Chose Country First.')
else:
    st.write('BASE POINT')
    with st.form('f_rail_base'):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("ORIGIN", origin_base_dict["ROAD"], key='_rail_origin_base')
        with col2:
            st.selectbox("DESTINATION", destination_base_dict["RAIL"], key='_rail_dist_base')
        st.form_submit_button("submit", key="f_rail_base", on_click=store_form_result, args=['f_rail_base'])
    if st.session_state['f_rail_base']:
        store_value('rail_origin_base')
        store_value('rail_dist_base')

    if not st.session_state['status_f_rail_base']:
        st.write('Chose Base Point First')
    else:
        origin_rail_port = get_port_name(country_dim, st.session_state['rail_origin_base'])        
        destination_rail_port = get_port_name(country_dim, st.session_state['rail_dist_base'])
        st.write('PORTS')
        with st.form('f_rail_port'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_road_port, key='_rail_origin_port')
            with col2:
                st.selectbox("DESTINATION", destination_road_port, key='_rail_dist_port')
            st.form_submit_button("submit", key="f_rail_port", on_click=store_form_result, args=['f_rail_port'])
        if st.session_state['f_rail_port']:
            store_value('rail_origin_port')
            store_value('rail_dist_port')

        if not st.session_state['status_f_rail_port']:
            st.write('Chose Ports First')
        else:
            st.write('VEHICLE SETUP')
            with st.form('f_rail_vehicle'):
                st.selectbox("VEHICLE_TYPE", road_vehicle, key='_rail_vehicle_type')
                st.selectbox("FUEL_TYPE", road_fuel,  key='_rail_fuel_type')
                st.form_submit_button("submit", key="f_rail_vehicle", on_click=store_form_result, args=['f_rail_vehicle'])
            if st.session_state['status_f_rail_vehicle']:
                store_value('rail_vehicle_type')
                store_value('rail_fuel_type')        

