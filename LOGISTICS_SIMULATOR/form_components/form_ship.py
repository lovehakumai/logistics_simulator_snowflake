import streamlit as st
def form_ship():
    if not st.session_state['status_f_countries']:
        st.write('Please Chose Country First.')
    else:
        st.write('BASE POINT')
        with st.form('f_sea_base'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_base_dict["SEA"], key='_sea_origin_base')
            with col2:
                st.selectbox("DESTINATION", destination_base_dict["SEA"], key='_sea_dist_base')
            st.form_submit_button("submit", key="f_sea_base", on_click=store_form_result, args=['f_sea_base'])
        if st.session_state['f_sea_base']:
            store_value('sea_origin_base')
            store_value('sea_dist_base')
    
        if not st.session_state['status_f_sea_base']:
            st.write('Chose Base Point First')
        else:
            origin_sea_port = get_port_name(country_dim, st.session_state['sea_origin_base'])        
            destination_sea_port = get_port_name(country_dim, st.session_state['sea_dist_base'])
            st.write('PORTS')
            with st.form('f_sea_port'):
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("ORIGIN", origin_sea_port, key='_sea_origin_port')
                with col2:
                    st.selectbox("DESTINATION", destination_sea_port, key='_sea_dist_port')
                st.form_submit_button("submit", key="f_sea_port", on_click=store_form_result, args=['f_sea_port'])
            if st.session_state['f_sea_port']:
                store_value('sea_origin_port')
                store_value('sea_dist_port')
    
            if not st.session_state['status_f_sea_port']:
                st.write('Chose Ports First')
            else:
                st.write('VEHICLE SETUP')
                with st.form('f_sea_vehicle'):
                    st.selectbox("SIZE", sea_size, key='_sea_size')
                    st.selectbox("VEHICLE_TYPE", sea_vehicle, key='_sea_vehicle_type')
                    st.selectbox("FUEL_TYPE", sea_fuel, key='_sea_fuel_type')
                    st.form_submit_button("submit", key="f_sea_vehicle", on_click=store_form_result, args=['f_sea_vehicle'])
                if st.session_state['status_f_sea_vehicle']:
                    store_value('sea_size')
                    store_value('sea_vehicle_type')
                    store_value('sea_fuel_type')
    return 