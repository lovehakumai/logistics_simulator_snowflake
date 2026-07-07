# classes/analytics/monitor.py
from snowflake.snowpark.context import get_active_session
import pandas as pd
import streamlit as st

class Monitor:
    def __init__(self):
        self.session = get_active_session()
        self.session.sql("ALTER SESSION SET QUERY_TAG = 'logistics_simulator'").collect()
        self.session.sql("USE DATABASE KAGGLE_LOGISTICS").collect()
    
    def get_billing_logs(self):
        query_string = """
            SELECT 
                START_TIME
                , DATE_TRUNC(DAY, START_TIME)::DATE AS START_DATE
                , QUERY_ID
                , QUERY_TEXT
                , USER_NAME 
                , (TOTAL_ELAPSED_TIME / 1000 / 3600) AS total_hour 
                , (TOTAL_ELAPSED_TIME / 1000 / 3600) * CASE WAREHOUSE_SIZE  
                    WHEN 'X-Small' THEN 1
                    WHEN 'Small'   THEN 2
                    WHEN 'Medium'  THEN 4
                    WHEN 'Large'   THEN 8
                    END AS total_credit
            FROM TABLE(KAGGLE_LOGISTICS.INFORMATION_SCHEMA.QUERY_HISTORY(RESULT_LIMIT => 10000)) 
            WHERE 
            (QUERY_TAG = 'logistics_simulator' AND QUERY_TEXT NOT LIKE '%INFORMATION_SCHEMA.QUERY_HISTORY%')
            OR (
                QUERY_TEXT ILIKE '%MRT__DIM_COUNTRY_FACTOR%'
                OR QUERY_TEXT ILIKE '%MRT__DIM_MODE_FACTOR%'
                OR QUERY_TEXT ILIKE '%INT__BASE%'           
                OR QUERY_TEXT ILIKE '%INT__FCT_AGG_FUEL_PRICE%'
                OR QUERY_TEXT ILIKE '%INT__FCT_AGG_LOGS%'      
                OR QUERY_TEXT ILIKE '%INT__FCT_DEST_AGG%'      
                OR QUERY_TEXT ILIKE '%INT__FCT_LOGS_RAW%'
            )
            ORDER BY START_TIME DESC
        """
        
        log_df = self.session.sql(query_string).to_pandas()
        return log_df