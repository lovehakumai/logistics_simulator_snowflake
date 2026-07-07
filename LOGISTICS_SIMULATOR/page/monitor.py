import streamlit as st 
from classes.monitor.monitor import Monitor
def monitor():
    

    st.title('💰Monitor')
    
    monitor = Monitor()
    log_df = monitor.get_billing_logs()
    date_log = log_df.groupby("START_DATE").sum(["TOTAL_HOUR", "TOTAL_CREDIT"])
    st.bar_chart(
        data = date_log,
        y = ["TOTAL_HOUR", "TOTAL_CREDIT"]
    )
    query_log = (
        log_df
        .groupby(["QUERY_TEXT"])[["TOTAL_CREDIT", "TOTAL_HOUR"]]
        .sum().reset_index()
        .sort_values(by = ["TOTAL_CREDIT"], ascending = False)
    )
    user_log = (
        log_df
        .groupby(["USER_NAME"])[["TOTAL_CREDIT", "TOTAL_HOUR"]]
        .sum().reset_index()
        .sort_values(by = ["TOTAL_CREDIT"], ascending = False)
    )
    query, user = st.columns(2)
    with query: 
        st.subheader("Query Text")
        st.dataframe(query_log)
    with user: 
        st.subheader("Users")
        st.dataframe(user_log)