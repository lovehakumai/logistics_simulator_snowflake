import streamlit as st
def form_air():
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
    return 