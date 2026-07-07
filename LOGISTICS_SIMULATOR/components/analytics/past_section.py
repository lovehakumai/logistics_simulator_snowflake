import streamlit as st
from classes.analytics.analytics_data import Analytics_data
from classes.analytics.analytics_state import Analytics_state

def past_section(analytics_data: Analytics_data, analytics_state: Analytics_state):

    st.subheader("Past metrics")
    
    filter_list = sorted(list(analytics_state.past_date_range_dict.keys()))
    risk_count_df = analytics_data.get_past_data(st.session_state['past_date_range'])
    raw_df = analytics_data.get_past_data(st.session_state['past_date_range'], True)

    with st.form('form_past_date_range'):
        past_date_range = st.selectbox(
            "DateRange", 
            filter_list,
            format_func= lambda x : analytics_state.past_date_range_dict[x],
            key = '_past_date_range'
        )
        st.form_submit_button("submit", key='_f_past_date_range')
    
    if st.session_state['_f_past_date_range']:
        analytics_state.store_value('past_date_range')
        
    def metrics_container(mode):
        if f'{mode}_selected_detail' not in st.session_state:
            st.session_state[f'{mode}_selected_detail'] = None 
        
        with st.container(border=True):
            
            col1, col2, col3= st.columns(3)
            with col1:
                st.subheader(f"{mode_dict[mode]}")
                st.write(f"{st.session_state[f'{mode}_origin_base']} ==>{st.session_state[f'{mode}_dest_base']}")
                
            with col2:
                st.metric(
                    "BadWeather", 
                    risk_count_df[risk_count_df['transport_mode']==mode]['bad_weather_cnt'].iloc[0],
                    border=True
                )
                if st.button("🔍Show Detail", key=f"{mode}_detail_weather", use_container_width = True):
                    if st.session_state[f'{mode}_selected_detail'] == "weather":
                        st.session_state[f'{mode}_selected_detail'] = None 
                    else: 
                        st.session_state[f'{mode}_selected_detail'] = "weather" 
                    
            with col3:
                st.metric(
                    "Desrupt", 
                    risk_count_df[risk_count_df['transport_mode']==mode]['desrupt_cnt'].iloc[0],
                    border=True
                )
                if st.button("🔍Show Detail", key=f"{mode}_detail_desrupt", use_container_width = True):
                    if st.session_state.get(f'{mode}_selected_detail', None) == "desrupt":
                        st.session_state[f'{mode}_selected_detail'] = None 
                    else: 
                        st.session_state[f'{mode}_selected_detail'] = "desrupt"
                        
            if st.session_state.get(f'{mode}_selected_detail', None) == "weather":
                st.write("⚡️ Weather Details")
                weather_df = raw_df[raw_df['TRANSPORT_MODE'] == mode.upper() ].groupby(
                    ['DATE', 'WEATHER_CONDITION']).agg({"SHIPMENT_ID": 'nunique'}).reset_index()
                st.line_chart(
                    data = weather_df,
                    x = 'DATE',
                    y = 'SHIPMENT_ID',
                    color = 'WEATHER_CONDITION'
                )
                    
            elif st.session_state.get(f'{mode}_selected_detail', None) == "desrupt":
                st.write("⚠️ Desrupt Details")
                desrupt_df = raw_df[(raw_df['TRANSPORT_MODE'] == mode.upper()) & (raw_df['DISRUPTION_OCCURRED']==1) ].groupby(
                    ['DATE']).agg({"SHIPMENT_ID": 'nunique'}).reset_index()
                st.line_chart(
                    data = desrupt_df,
                    x = 'DATE',
                    y = 'SHIPMENT_ID'
                )
    
    mode_dict = {
        'air' : '✈️AIR',
        'sea' : '🚢SEA',
        'road': '🚚ROAD',
        'rail': '🚃RAIL'
    }
    mode_list = sorted(list(mode_dict.keys()))
    for mode in mode_list:
        metrics_container(mode)
                    
