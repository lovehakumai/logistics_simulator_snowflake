import streamlit as st
def form_rail():
    if not st.session_state['status_f_countries']:
        st.write('Please Chose Country First.')
    else:
        st.write('BASE POINT')
        with st.form('f_rail_base'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_base_dict["ROAD"], key='_rail_origin_base')
            with col2:
                st.selectbox("DESTINATION", destination_base_dict["RAIL"], key='_rail_dist_base')
            st.form_submit_button("submit", key="f_rail_base", on_click=store_form_result, args=['f_rail_base'])
        if st.session_state['f_rail_base']:
            store_value('rail_origin_base')
            store_value('rail_dist_base')
    
        if not st.session_state['status_f_rail_base']:
            st.write('Chose Base Point First')
        else:
            origin_rail_port = get_port_name(country_dim, st.session_state['rail_origin_base'])        
            destination_rail_port = get_port_name(country_dim, st.session_state['rail_dist_base'])
            st.write('PORTS')
            with st.form('f_rail_port'):
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("ORIGIN", origin_road_port, key='_rail_origin_port')
                with col2:
                    st.selectbox("DESTINATION", destination_road_port, key='_rail_dist_port')
                st.form_submit_button("submit", key="f_rail_port", on_click=store_form_result, args=['f_rail_port'])
            if st.session_state['f_rail_port']:
                store_value('rail_origin_port')
                store_value('rail_dist_port')
    
            if not st.session_state['status_f_rail_port']:
                st.write('Chose Ports First')
            else:
                st.write('VEHICLE SETUP')
                with st.form('f_rail_vehicle'):
                    st.selectbox("VEHICLE_TYPE", road_vehicle, key='_rail_vehicle_type')
                    st.selectbox("FUEL_TYPE", road_fuel,  key='_rail_fuel_type')
                    st.form_submit_button("submit", key="f_rail_vehicle", on_click=store_form_result, args=['f_rail_vehicle'])
                if st.session_state['status_f_rail_vehicle']:
                    store_value('rail_vehicle_type')
                    store_value('rail_fuel_type')     
    return 