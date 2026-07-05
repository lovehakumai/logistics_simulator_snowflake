from snowflake.snowpark.context import get_active_session
import pandas as pd 
from class.setup.setup_state import setup_state

class Setup_data():

    def __init__(self):
        self.session = get_active_session()
        self.mode_dim = 'DEV_ANALYTICS.MRT__DIM_MODE_FACTOR'
        self.counrty_dim = 'DEV_ANALYTICS.MRT__DIM_COUNTRY_FACTOR'
        
        session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()    
        self.mode_dim = session.sql(f"SELECT * FROM {mode_dim}").to_pandas()
        self.country_dim = session.sql(f"SELECT * FROM {country_dim}").to_pandas()

        self.air_vehicle = None 
        self.air_fuel = None 
        self.air_distance = None 

        self.sea_vehicle = None
        self.sea_fuel = None 
        self.sea_size = None 

        self.road_vehicle = None
        self.road_fuel = None 

        self.rail_vehicle = None 
        self.rail_fuel = None 

    def get_base_point(self, country_name):
        df = country_dim[country_dim['COUNTRY_NAME'] == country_name]
        air_list = df[df["TRANSPORT_MODE"] == 'AIR']['BASE_POINT'].unique()
        sea_list = df[df["TRANSPORT_MODE"] == 'SEA']['BASE_POINT'].unique()
        road_list = df[df["TRANSPORT_MODE"] == 'ROAD']['BASE_POINT'].unique()
        rail_list = df[df["TRANSPORT_MODE"] == 'RAIL']['BASE_POINT'].unique()
        return {"AIR":air_list, "SEA":sea_list, "ROAD":road_list, "RAIL":rail_list}

    def get_port_name(self, base_name):
        df = country_dim[(country_dim['BASE_POINT'] == base_name)]
        air_list = df[df["TRANSPORT_MODE"] == 'AIR']['PORT_NAME_RN'].unique()
        sea_list = df[df["TRANSPORT_MODE"] == 'SEA']['PORT_NAME_RN'].unique()
        road_list = df[df["TRANSPORT_MODE"] == 'ROAD']['PORT_NAME_RN'].unique()
        rail_list = df[df["TRANSPORT_MODE"] == 'RAIL']['PORT_NAME_RN'].unique()
        return {"AIR":air_list, "SEA":sea_list, "ROAD":road_list, "RAIL":rail_list}
        return result_list

    def update_air_params(self):
        air_mode_dim = self.mode_dim[self.mode_dim['TRANSPORT_MODE'] == "AIR"]
        self.air_vehicle = air_mode_dim['VEHICLE_TYPE'].unique()
        self.air_fuel = air_mode_dim['FUEL_TYPE'].unique()
        self.air_distance = air_mode_dim['AIR_DISTANCE'].unique()

    def update_sea_params(self):
        sea_mode_dim = self.mode_dim[self.mode_dim['TRANSPORT_MODE'] == "SEA"]
        self.sea_vehicle = sea_mode_dim['VEHICLE_TYPE'].unique()
        self.sea_fuel = sea_mode_dim['FUEL_TYPE'].unique()
        self.sea_size = sea_mode_dim['SEA_SIZE'].unique()

    def update_road_params(self):
        road_mode_dim = self.mode_dim[self.mode_dim['TRANSPORT_MODE'] == "ROAD"]
        self.road_vehicle = road_mode_dim['VEHICLE_TYPE'].unique()
        self.road_fuel = road_mode_dim['FUEL_TYPE'].unique()

    def update_rail_params(self):
        rail_mode_dim = self.mode_dim[self.mode_dim['TRANSPORT_MODE'] == "RAIL"]
        self.rail_vehicle = rail_mode_dim['VEHICLE_TYPE'].unique()
        self.rail_fuel = rail_mode_dim['FUEL_TYPE'].unique()
        
    @property
    def get_country_list(self):
        return self.country_dim['COUNTRY_NAME'].unique()