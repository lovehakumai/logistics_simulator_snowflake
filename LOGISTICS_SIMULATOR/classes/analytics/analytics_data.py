import streamlit as st 
import pandas as pd 
import numpy as np
from snowflake.snowpark.context import get_active_session
import math 

class Analytics_data:
    def __init__(self):
        self.session = get_active_session()
        self.mode_dim = 'DEV_ANALYTICS.MRT__DIM_MODE_FACTOR'
        self.country_dim = 'DEV_ANALYTICS.MRT__DIM_COUNTRY_FACTOR'
        
        self.session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()    
        self.mode_dim = self.session.sql(f"SELECT * FROM {self.mode_dim}").to_pandas()
        self.country_dim = self.session.sql(f"SELECT * FROM {self.country_dim}").to_pandas() 

    def calc_distance_km(origin_df, dest_df):
        origin_lat = origin_df["LATITUDE"]
        origin_lon = origin_df["LONGITUDE"]
        dest_lat = dest_df["LATITUDE"]
        dest_lon = dest_df["LONGITUDE"]
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance_km = R * c
        return distance_km

    def get_cost_per_transport(self):        
        # create the data, 
        # grain : transport_mode(air, sea, road, rail), 
        # values : 
            # L place : country_name(ori/des), base_point(ori/des), port_name(ori/des)
            # L distance : km, num_containers,
            # L cost_factors : carbon_tax, air_minimum, air_cost_km_wt, other_cost_container
            # L prams: fuel_increase_param, risk_avoidance_param, weight_t
                # L point : wt => calclate 1 container as 20t weight 
        
        transport_mode_list = ['air', 'sea', 'road', 'rail']

        country_origin_name = st.session_state['origin_country']
        country_destination_name = st.session_state['destination_country']
        
        air_base_origin_name = st.session_state['air_origin_base']
        sea_base_origin_name = st.session_state['sea_origin_base']
        road_base_origin_name = st.session_state['road_origin_base']
        rail_base_origin_name = st.session_state['rail_origin_base']
        
        air_base_dest_name = st.session_state['air_dest_base']
        sea_base_dest_name = st.session_state['sea_dest_base']
        road_base_dest_name = st.session_state['road_dest_base']
        rail_base_dest_name = st.session_state['rail_dest_base']        

        air_port_origin_name = st.session_state['air_origin_port']
        sea_port_origin_name = st.session_state['sea_origin_port']
        road_port_origin_name = st.session_state['road_origin_port']
        rail_port_origin_name = st.session_state['rail_origin_port']
        
        air_port_dest_name = st.session_state['air_dest_port']
        sea_port_dest_name = st.session_state['sea_dest_port']
        road_port_dest_name = st.session_state['road_dest_port']
        rail_port_dest_name = st.session_state['rail_dest_port']        
        
        weight = st.session_state['weight_t']
        num_of_container = weight // 20 
        fuel_increase_param = st.session_state['fuel_increase_param']
        risk_avoidance_param = st.session_state['risk_avoidance_param']

        air_fuel_type = st.session_state['air_fuel_type']
        sea_fuel_type = st.session_state['sea_fuel_type']
        road_fuel_type = st.session_state['road_fuel_type']
        rail_fuel_type = st.session_state['rail_fuel_type']
        
        air_distance = None
        sea_distance = None
        road_distance = None
        rail_distance = None

        air_cost_km_wt = None 
        air_cost_minimum = None
        sea_cost_container = None
        road_cost_container = None
        rail_costr_container = None

        air_carbon_tax_t = None
        sea_carbon_tax_t = None
        road_carbon_tax_t = None
        rail_carbon_tax_t = None

        air_fuel_l_t_km = None
        sea_fuel_l_t_km = None
        road_fuel_l_t_km = None
        rail_fuel_l_t_km = None

        air_co2_emission = None
        sea_co2_emission = None
        road_co2_emission = None
        rail_co2_emission = None

        for i in transport_mode_list:
            origin = (
                self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f'{i}_origin_port']]
                [["LATITUDE", "LONGITUDE", "COST_PER_KM_WT", "COST_PER_CONTAINER", "MINIMUM_CHARGE", "CARBON_TAX_PER_T_CO2"]]
            )
            dest = (
                self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f'{i}_dest_port']]
                [["LATITUDE", "LONGITUDE", "COST_PER_KM_WT", "COST_PER_CONTAINER", "MINIMUM_CHARGE", "CARBON_TAX_PER_T_CO2"]]
            )

            if i == 'air':
                air_cost_km_wt = dest['COST_PER_KM_WT']
                air_cost_minimum = dest['MINIMUM_CHARGE']
                air_carbon_tax_t = dest['CARBON_TAX_PER_T_CO2']
                air_distance = calc_distance_km(air_origin, air_dest)
            elif i == 'sea':
                sea_cost_container = dest['COST_PER_CONTAINER']
                sea_carbon_tax_t = dest['CARBON_TAX_PER_T_CO2']
                sea_distance = calc_distance_km(sea_origin, sea_dest)
            elif i == 'road':
                road_cost_container = dest['COST_PER_CONTAINER']
                road_carbon_tax_t = dest['CARBON_TAX_PER_T_CO2']
                road_distance = calc_distance_km(road_origin, road_dest)
            elif i == 'rail':
                rail_costr_container = dest['COST_PER_CONTAINER']
                rail_carbon_tax_t = dest['CARBON_TAX_PER_T_CO2']
                rail_distance = calc_distance_km(rail_origin, rail_dest)

        # co2 emission per t,km
        air_df = self.mode_dim[
            (self.mode_dim["TRANSPORT_MODE"] == "AIR")
            &(self.mode_dim["VEHICLE_TYPE"] == st.session_state["air_vehicle_type"])
            &(self.mode_dim["AIR_DISTANCE"] == st.session_state["air_distance"])
            &(self.mode_dim["FUEL_TYPE"]== st.session_state["air_fuel_type"])
        ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
        sea_df = self.mode_dim[
            (self.mode_dim["TRANSPORT_MODE"] == "SEA")
            &(self.mode_dim["VEHICLE_TYPE"] == st.session_state["sea_vehicle_type"])
            &(self.mode_dim["SEA_SIZE"] == st.session_state['sea_size'])
            &(self.mode_dim["FUEL_TYPE"]== st.session_state["sea_fuel_type"])
        ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
        road_df = self.mode_dim[
            (self.mode_dim["TRANSPORT_MODE"] == "ROAD")
            &(self.mode_dim["VEHICLE_TYPE"] == st.session_state['road_vehicle_type'])
            &(self.mode_dim["FUEL_TYPE"] == st.session_state["road_fuel_type"])
        ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
        rail_df = self.mode_dim[
            (self.mode_dim["TRANSPORT_MODE"] == "RAIL")
            &(self.mode_dim["VEHICLE_TYPE"] == st.session_state['rail_vehicle_type'])
            &(self.mode_dim["FUEL_TYPE"] == st.session_state['rail_fuel_type'])
        ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
        
        air_co2_emission = air_df['WTW_CO2_G_T_KM']
        air_fuel_l_t_km = air_df['FUEL_L_T_KM']
        sea_co2_emission = sea_df['WTW_CO2_G_T_KM']
        sea_fuel_l_t_km = sea_df['FUEL_L_T_KM']
        road_co2_emission = road_df['WTW_CO2_G_T_KM']
        road_fuel_l_t_km = road_df['FUEL_L_T_KM']
        rail_co2_emission = rail_df['WTW_CO2_G_T_KM']
        rail_fuel_l_t_km = rail_df['FUEL_L_T_KM']
        
        merged_df = pd.DataFrame(
            {
                "transport_mode": ['air', 'sea', 'road', 'rail'],
                "country_origin_name": [country_origin_name] * 4,
                "country_destination_name":[country_destination_name] * 4,
                "base_origin_name":[air_base_origin_name, sea_base_origin_name, road_base_origin_name, rail_base_origin_name],
                "base_dest_name":[air_base_dest_name, sea_base_dest_name, road_base_dest_name, rail_base_dest_name],
                "port_origin_name":[air_port_origin_name, sea_port_origin_name, road_port_origin_name, rail_port_origin_name],
                "port_dest_name":[air_port_dest_name, sea_port_dest_name, road_port_dest_name, rail_port_dest_name],
                "weight":[weight]*4,
                "num_of_container": [num_of_container]*4,
                "fuel_increase_param": [fuel_increase_param]*4,
                "risk_avoidance_param":[risk_avoidance_param]*4,
                "distance":[air_distance, sea_distance, road_distance, rail_distance],
                "air_cost_km_wt": [air_cost_km_wt, 0, 0, 0],
                "air_cost_minimum":[air_cost_minimum, 0, 0, 0],
                "cost_container":[0, sea_cost_container, road_cost_container, rail_costr_container],
                "carbon_tax_t": [air_carbon_tax_t, sea_carbon_tax_t, road_carbon_tax_t, road_carbon_tax_t, rail_carbon_tax_t],
                "fuel_l_t_km":[air_fuel_l_t_km, sea_fuel_l_t_km, road_fuel_l_t_km, rail_fuel_l_t_km],
                "fuel_type":[air_fuel_type, sea_fuel_type, road_fuel_type, rail_fuel_type],
                "air_co2_emission_g_t_km":[air_co2_emission, sea_co2_emission, road_co2_emission, rail_co2_emission]
            }
        )

        # handling Fee
        def calculate_total_cost(row):
            if row['transport_mode'] == 'air':
                return row['air_cost_minimum'] + row['air_cost_km_wt']*row['distance']*row['weight']
            else: 
                return row['cost_container'] * row['num_of_container']

        merged_df['cost_port_fee'] = df.apply(calculate_total_cost, axis=1)

        # carbon tax
        merged_df['cost_carbon_tax'] = (
            (((merged_df['air_co2_emission_g_t_km'] * merged_df['weight'] * merged_df['distance'])/1_000_000) 
            * merged_df['carbon_tax_t'])
        )
        # TODO : 
        # fuel Fee : later, needs fact df
        # policitcal risk, desruption risk