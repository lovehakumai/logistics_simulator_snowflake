from snowflake.snowpark.context import get_active_session
import pandas as pd 

class Setup_data():

    def __init__(self):
        self.session = get_active_session()
        self.mode_dim = 'DEV_ANALYTICS.MRT__DIM_MODE_FACTOR'
        self.country_dim = 'DEV_ANALYTICS.MRT__DIM_COUNTRY_FACTOR'
        
        self.session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()    
        self.mode_dim = self.session.sql(f"SELECT * FROM {self.mode_dim}").to_pandas()
        self.country_dim = self.session.sql(f"SELECT * FROM {self.country_dim}").to_pandas()

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

        self.air_list_base = None 
        self.sea_list_base = None 
        self.road_list_base = None 
        self.rail_list_base = None

        self.air_list_port = None 
        self.sea_list_port = None 
        self.road_list_port = None 
        self.rail_list_port = None 

    def get_base_point(self, country_name):
        df = self.country_dim[self.country_dim['COUNTRY_NAME'] == country_name]
        air_list_base = df[df["TRANSPORT_MODE"] == 'AIR']['BASE_POINT'].unique()
        sea_list_base = df[df["TRANSPORT_MODE"] == 'SEA']['BASE_POINT'].unique()
        road_list_base = df[df["TRANSPORT_MODE"] == 'ROAD']['BASE_POINT'].unique()
        rail_list_base = df[df["TRANSPORT_MODE"] == 'RAIL']['BASE_POINT'].unique()
        return {"AIR":air_list_base, "SEA":sea_list_base, "ROAD":road_list_base, "RAIL":rail_list_base}

    def get_port_name(self, base_name):
        df = self.country_dim[self.country_dim['BASE_POINT'] == base_name]
        air_list_port = df[df["TRANSPORT_MODE"] == 'AIR']['PORT_NAME_EN'].unique()
        sea_list_port = df[df["TRANSPORT_MODE"] == 'SEA']['PORT_NAME_EN'].unique()
        road_list_port = df[df["TRANSPORT_MODE"] == 'ROAD']['PORT_NAME_EN'].unique()
        rail_list_port = df[df["TRANSPORT_MODE"] == 'RAIL']['PORT_NAME_EN'].unique()
        return {"AIR":air_list_port, "SEA":sea_list_port, "ROAD":road_list_port, "RAIL":rail_list_port}
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