from classes.analytics.analytics_data import Analytics_data
from classes.analytics.analytics_state import Analytics_state
import streamlit as st 

def cost_section(analytics_data: Analytics_data, analytics_state: Analytics_state):
    
    with st.form("form_risk_param"):
        fuel_increase_param = st.slider(
            'fuel_increase_param', 
            0.0, 5.0, 1.0, 
            step = 0.5
        )
        risk_avoidance_param = st.slider(
            'risk_avoidance_param', 
            0.0, 5.0, 1.0, 
            step = 0.5
        )
        weight = st.slider(
            'weight', 
            0.0, 5.0, 1.0, 
            step = 20.0
        )
        
        st.form_submit_button('Submit', key = 'f_risk_param')

    if st.session_state['f_risk_param']:
        st.session_state['fuel_increase_param'] = fuel_increase_param
        st.session_state['risk_avoidance_param'] = risk_avoidance_param
        st.session_state['weight_t'] = weight
        
        
    cost_per_mode_df = analytics_data.get_cost_per_transport()
    
    st.subheader("The Most efficient Transport")
    
    def cost_metrics(df, column_nm):
        air_val = df[df['transport_mode']=='air'][column_nm].iloc[0]
        sea_val = df[df['transport_mode']=='sea'][column_nm].iloc[0]
        road_val = df[df['transport_mode']=='road'][column_nm].iloc[0]
        rail_val = df[df['transport_mode']=='rail'][column_nm].iloc[0]
    
        air, sea, road, rail = st.columns(4)
        air.metric(label='✈️AIR', value = air_val, format='compact')
        sea.metric(label = '🚢SHIP', value = sea_val, format='compact')
        road.metric(label = '🚚ROAD', value = road_val, format='compact')
        rail.metric(label = '🚃RAIL', value = rail_val, format='compact')
        return
    
    with st.container(border=True):
        cost_metrics(cost_per_mode_df, "cost_total")
        st.bar_chart(
            data=cost_per_mode_df, 
            x = 'transport_mode', 
            y= 'cost_total' , 
            horizontal = True , 
            color='#1E3A8A', 
            sort = 'cost_total'
        )
    
    a, b = st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown("**⛽ FUEL PRICE**")
            cost_metrics(cost_per_mode_df, "cost_fuel_price")
            st.bar_chart(
                data=cost_per_mode_df, 
                x = 'transport_mode', 
                y= 'cost_fuel_price' , 
                horizontal = True , 
                color='#1E3A8A', 
                sort = 'cost_fuel_price'
            )
            
    with b:
        with st.container(border=True):
            st.markdown("**🚢 PORT FEE**")
            cost_metrics(cost_per_mode_df, "cost_port_fee")
            st.bar_chart(
                data=cost_per_mode_df, 
                x = 'transport_mode', 
                y= 'cost_port_fee' , 
                horizontal = True , 
                color='#1E3A8A', 
                sort = 'cost_port_fee'
            )
            
            
    c, d = st.columns(2)
    with c: 
        with st.container(border=True):
            st.markdown("**🌿 CARBON TAX**")
            cost_metrics(cost_per_mode_df, "cost_carbon_tax")
            st.bar_chart(
                data=cost_per_mode_df, 
                x = 'transport_mode', 
                y= 'cost_carbon_tax' , 
                horizontal = True , 
                color='#1E3A8A', 
                sort = 'cost_carbon_tax'
            )
            
            
    with d: 
        with st.container(border=True):
            st.markdown("**⚠️ DISRUPTION RISK**")
            cost_metrics(cost_per_mode_df, "cost_risk")
            st.bar_chart(
                data=cost_per_mode_df, 
                x = 'transport_mode', 
                y= 'cost_risk' , 
                horizontal = True , 
                color='#1E3A8A', 
                sort = 'cost_risk'
            )
    
    st.dataframe(cost_per_mode_df)