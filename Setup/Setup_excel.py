import pandas as pd  # modinではなく標準のpandasを使用
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.files import SnowflakeFile  # ステージファイルを開くためのモジュール

import subprocess
import sys

def install_package(package_name):
    """Installs a python package using the current interpreter's pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")

# Example usage:
if __name__ == "__main__":
    install_package("openpyxl")


    # アクティブセッションの取得
    session = get_active_session()
    
    sheet_list = ["main_ports", "co2_emmision", "dim_transport_fuel", "fct_fuel_prices"]
    stage_path = '@"KAGGLE_LOGISTICS"."RAW"."DBT_SEED"/Gachi_Project03_LogisticsSimulator_seed (1).xlsx'
    df_dict = {}
    
    for i in sheet_list:
        # SnowflakeFileを使ってステージのファイルをバイナリで安全に開く
        with SnowflakeFile.open(stage_path, 'rb') as f:
            df = pd.read_excel(f, sheet_name=i)
            df_dict[i] = df 
    
    print(df_dict)