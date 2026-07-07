import streamlit as st 
import pandas as pd 
import numpy as np
from snowflake.snowpark.context import get_active_session
import math 

class Analytics_data:
    def __init__(self):
        self.session = get_active_session()
        self.mode_dim_table = 'DEV_ANALYTICS.MRT__DIM_MODE_FACTOR'
        self.country_dim_table = 'DEV_ANALYTICS.MRT__DIM_COUNTRY_FACTOR'
        self.fct_fuel_price_table = 'DEV_INTERMEDIATE.INT__FCT_AGG_FUEL_PRICE'
        self.fct_risk_table = 'DEV_INTERMEDIATE.INT__FCT_DEST_AGG'
        self.fct_agg_logs = 'DEV_INTERMEDIATE.INT__FCT_AGG_LOGS'
        
        self.session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()    
        
        self.mode_dim = self.session.sql(f"SELECT * FROM {self.mode_dim_table}").to_pandas()
        self.country_dim = self.session.sql(f"SELECT * FROM {self.country_dim_table}").to_pandas() 
        self.fct_fuel_price = self.session.sql(f"SELECT * FROM {self.fct_fuel_price_table}").to_pandas() 
        self.fct_risk = self.session.sql(f"SELECT * FROM {self.fct_risk_table}").to_pandas() 
        
        
        
    @staticmethod
    def calc_distance_km(lat1, lon1, lat2, lon2):
        # @staticmethod : doesn't need self in args. just a calculation
        R = 6371.0 # 地球の半径 (km)
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_past_data(self, range_val, call_from = None):
        
        self.fact_logs_table = "KAGGLE_LOGISTICS.DEV_INTERMEDIATE.INT__FCT_LOGS_RAW"
        self.fact_logs = self.session.sql(
            f"""
                SELECT 
                    f.* FROM {self.fact_logs_table} f
                CROSS JOIN (
                    SELECT MAX(DATE) AS MAX_DATE FROM {self.fact_logs_table}
                ) p
                WHERE 
                    f.DATE >= DATEADD(MONTH, -{range_val}, p.MAX_DATE)
            """
        ).to_pandas()
        
        transport_mode = ['air', 'sea', 'road', 'rail']
        
        bad_weather_uc_dt = {}
        desrupt_uc_dt = {}
        
        for mode in transport_mode:
            df = self.fact_logs[
                (self.fact_logs['ORIGIN_BASE_POINT'] == st.session_state[f'{mode}_origin_base'])
                &(self.fact_logs['DESTINATION_BASE_POINT'] == st.session_state[f'{mode}_dest_base'])
                ]
            bad_weather_uc_dt[mode] = df[df['WEATHER_CONDITION'] != 'Clear']['SHIPMENT_ID'].nunique()
            desrupt_uc_dt[mode] = df[df['DISRUPTION_OCCURRED'] == 1]['SHIPMENT_ID'].nunique()
            
        result_df = pd.DataFrame({
            'transport_mode': transport_mode,
            'bad_weather_cnt': [bad_weather_uc_dt[mode] for mode in transport_mode],
            'desrupt_cnt': [desrupt_uc_dt[mode] for mode in transport_mode]
        })

        if call_from == None:
            return result_df
        else: 
            return df    

    def get_port_coordinate(self):
        mode_list = ['air', 'sea', 'road', 'rail']
        ori_port_nm = {}
        dest_port_nm = {}
        ori_lat = {}
        ori_lon = {}
        dest_lat = {}
        dest_lon = {}
        color_rgb = {}
        

            
        for mode in mode_list:                        
            ori_cord_df = self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f"{mode}_origin_port"]][["LATITUDE", "LONGITUDE"]]
            dest_cord_df = self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f"{mode}_dest_port"]][["LATITUDE", "LONGITUDE"]]

            if mode == 'air':    
                color_rgb[mode] = [30, 144, 255, 200]
            elif mode == 'sea':  
                color_rgb[mode] = [46, 139, 87, 200]
            elif mode == 'road': 
                color_rgb[mode] = [218, 165, 32, 200]
            elif mode == 'rail': 
                color_rgb[mode] = [138, 43, 226, 200]
            
            ori_port_nm[mode] = st.session_state[f"{mode}_origin_port"]
            dest_port_nm[mode] = st.session_state[f"{mode}_dest_port"]
            ori_lat[mode] = ori_cord_df['LATITUDE'].iloc[0]
            ori_lon[mode] = ori_cord_df['LONGITUDE'].iloc[0]
            dest_lat[mode] = dest_cord_df['LATITUDE'].iloc[0]
            dest_lon[mode] = dest_cord_df['LONGITUDE'].iloc[0]

        result_df = pd.DataFrame({
            'origin_port_nm': ori_port_nm,
            'dest_port_nm': dest_port_nm,
            'origin_lat': ori_lat,
            'origin_lon': ori_lon,
            'dest_lat': dest_lat,
            'dest_lon': dest_lon,
            'color_rgb':color_rgb
        })
        return result_df 
        
        
    def get_cost_per_transport(self):        
        # create the data, 
        # grain : transport_mode(air, sea, road, rail), 
        # values : 
            # L place : country_name(ori/des), base_point(ori/des), port_name(ori/des)
            # L distance : km, num_containers,
            # L cost_factors : carbon_tax, air_minimum, air_cost_km_wt, other_cost_container
            # L prams: fuel_increase_param, risk_avoidance_param, weight_t
                # L point : wt => calclate 1 container as 20t weight 
        country_origin_name = {}
        country_dest_name = {}
        base_origin_name = {}
        base_dest_name = {}
        port_origin_name = {}
        port_dest_name = {}
        
        weight = {}
        num_of_container = {}
        
        fuel_increase_param = {}
        risk_avoidance_param = {}
        
        cost_km_wt = {}
        cost_minimum = {}
        carbon_tax_t = {}
        distance = {}
        cost_container = {}

        fuel_type = {}
        fuel_l_t_km = {}
        co2_emission = {}
        
        transport_mode_list = ['air', 'sea', 'road', 'rail']
        for mode in transport_mode_list:
            country_origin_name[mode] = st.session_state['origin_country']
            country_dest_name[mode] = st.session_state['destination_country']
            base_origin_name[mode] = st.session_state[f'{mode}_origin_base']
            base_dest_name[mode] = st.session_state[f'{mode}_dest_base']
            port_origin_name[mode] = st.session_state[f'{mode}_origin_port']
            port_dest_name[mode] = st.session_state[f'{mode}_dest_port']
            fuel_increase_param[mode] = st.session_state.get('fuel_increase_param', 1.0)
            risk_avoidance_param[mode] = st.session_state.get('risk_avoidance_param', 1.0)
            
            weight[mode] = st.session_state.get('weight_t', 20.0)
            num_of_container[mode] = max(1.0, weight[mode] // 20)
            
            origin_country_dim = (
                self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f'{mode}_origin_port']]
                [["LATITUDE", "LONGITUDE", "COST_PER_KM_WT", "COST_PER_CONTAINER", "MINIMUM_CHARGE", "CARBON_TAX_PER_T_CO2"]]
            )
            dest_country_dim = (
                self.country_dim[self.country_dim['PORT_NAME_EN'] == st.session_state[f'{mode}_dest_port']]
                [["LATITUDE", "LONGITUDE", "COST_PER_KM_WT", "COST_PER_CONTAINER", "MINIMUM_CHARGE", "CARBON_TAX_PER_T_CO2"]]
            )
            
            cost_km_wt[mode] = dest_country_dim['COST_PER_KM_WT'].iloc[0]
            cost_minimum[mode] = dest_country_dim['MINIMUM_CHARGE'].iloc[0]
            cost_container[mode] = dest_country_dim['COST_PER_CONTAINER'].iloc[0]
            carbon_tax_t[mode] = dest_country_dim['CARBON_TAX_PER_T_CO2'].iloc[0]
            fuel_type[mode] = st.session_state[f'{mode}_fuel_type']
            
            lat1, lon1 = origin_country_dim["LATITUDE"].iloc[0], origin_country_dim['LONGITUDE'].iloc[0]
            lat2, lon2 = dest_country_dim["LATITUDE"].iloc[0], dest_country_dim['LONGITUDE'].iloc[0]
            distance[mode] = self.calc_distance_km(lat1, lon1, lat2, lon2)

            if mode == 'air':
                df = self.mode_dim[
                    (self.mode_dim["TRANSPORT_MODE"] == "AIR")
                    &(self.mode_dim["VEHICLE_TYPE"] == st.session_state["air_vehicle_type"])
                    &(self.mode_dim["AIR_DISTANCE"] == st.session_state["air_distance"])
                    &(self.mode_dim["FUEL_TYPE"]== st.session_state["air_fuel_type"])
                    ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
                fuel_l_t_km[mode] = df['FUEL_L_T_KM'].iloc[0]
                co2_emission[mode] = df['WTW_CO2_G_T_KM'].iloc[0]
                
            elif mode == 'sea':
                df = self.mode_dim[
                    (self.mode_dim["TRANSPORT_MODE"] == "SEA")
                    &(self.mode_dim["VEHICLE_TYPE"] == st.session_state["sea_vehicle_type"])
                    &(self.mode_dim["SEA_SIZE"] == st.session_state['sea_size'])
                    &(self.mode_dim["FUEL_TYPE"]== st.session_state["sea_fuel_type"])
                     ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
                fuel_l_t_km[mode] = df['FUEL_L_T_KM'].iloc[0]
                co2_emission[mode] = df['WTW_CO2_G_T_KM'].iloc[0]
            elif mode == 'road':
                df = self.mode_dim[
                    (self.mode_dim["TRANSPORT_MODE"] == "ROAD")
                    &(self.mode_dim["VEHICLE_TYPE"] == st.session_state['road_vehicle_type'])
                    &(self.mode_dim["FUEL_TYPE"] == st.session_state["road_fuel_type"])
                    ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
                fuel_l_t_km[mode] = df['FUEL_L_T_KM'].iloc[0]
                co2_emission[mode] = df['WTW_CO2_G_T_KM'].iloc[0]
            elif mode == 'rail':
                df = self.mode_dim[
                    (self.mode_dim["TRANSPORT_MODE"] == "RAIL")
                    &(self.mode_dim["VEHICLE_TYPE"] == st.session_state['rail_vehicle_type'])
                    &(self.mode_dim["FUEL_TYPE"] == st.session_state['rail_fuel_type'])
                    ][["WTW_CO2_G_T_KM", "FUEL_L_T_KM"]]
                fuel_l_t_km[mode] = df['FUEL_L_T_KM'].iloc[0]
                co2_emission[mode] = df['WTW_CO2_G_T_KM'].iloc[0]
        
        merged_df = pd.DataFrame(
            {
                "transport_mode": transport_mode_list,
                "country_origin_name": [country_origin_name[mode] for mode in transport_mode_list],
                "country_destination_name":[country_dest_name[mode] for mode in transport_mode_list],
                "base_origin_name":[base_origin_name[mode] for mode in transport_mode_list],
                "base_dest_name":[base_dest_name[mode] for mode in transport_mode_list],
                "port_origin_name":[port_origin_name[mode] for mode in transport_mode_list],
                "port_dest_name":[port_dest_name[mode] for mode in transport_mode_list],
                "weight":[weight[mode] for mode in transport_mode_list],
                "num_of_container": [num_of_container[mode] for mode in transport_mode_list],
                "fuel_increase_param": [fuel_increase_param[mode] for mode in transport_mode_list],
                "risk_avoidance_param":[risk_avoidance_param[mode] for mode in transport_mode_list],
                "distance":[distance[mode] for mode in transport_mode_list],
                "air_cost_km_wt": [cost_km_wt[mode] for mode in transport_mode_list],
                "air_cost_minimum":[cost_minimum[mode] for mode in transport_mode_list],
                "cost_container":[cost_container[mode] for mode in transport_mode_list],
                "carbon_tax_t": [carbon_tax_t[mode] for mode in transport_mode_list],
                "fuel_l_t_km":[fuel_l_t_km[mode] for mode in transport_mode_list],
                "fuel_type":[fuel_type[mode] for mode in transport_mode_list],
                "co2_emission_g_t_km":[co2_emission[mode] for mode in transport_mode_list]
            }
        )

        # handling Fee
        def calculate_total_cost(row):
            if row['transport_mode'] == 'air':
                return row['air_cost_minimum'] + row['air_cost_km_wt']*row['distance']*row['weight']
            else: 
                return row['cost_container'] * row['num_of_container']

        merged_df['cost_port_fee'] = merged_df.apply(calculate_total_cost, axis=1)

        # carbon tax
        merged_df['cost_carbon_tax'] = (
            (((merged_df['co2_emission_g_t_km'] * merged_df['weight'] * merged_df['distance'])/1_000_000) 
            * merged_df['carbon_tax_t'])
        )
        # LEFT JOIN Fuel market price
        merged_df = pd.merge(merged_df, self.fct_fuel_price, how = 'left', left_on = 'fuel_type', right_on = 'FUEL_TYPE')
        merged_df['cost_fuel_price'] = (
                ((merged_df['distance'] * merged_df['weight']) * merged_df['fuel_l_t_km'])
                * merged_df['FUEL_PRICE_USD_PER_L'] 
                * merged_df['fuel_increase_param']
        )
        # LEFT JOIN risk factors
        merged_df['tmp_mode'] = merged_df['transport_mode'].str.upper()
        merged_df = pd.merge(
            merged_df, self.fct_risk, 
            how='left', 
            left_on = ['base_dest_name', 'tmp_mode'],
            right_on = ['DESTINATION_BASE_POINT', 'TRANSPORT_MODE']
        )
        merged_df['cost_risk'] = (
            merged_df['cost_carbon_tax'] * (1 + merged_df['risk_avoidance_param'] * merged_df['DISRUPTION_RATE'])
        )
        merged_df['cost_total'] = (
            merged_df['cost_fuel_price'] + merged_df['cost_risk'] + merged_df['cost_port_fee']
        )
        return merged_df 
