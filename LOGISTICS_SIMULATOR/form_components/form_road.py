import streamlit as st
def form_road():
    if not st.session_state['status_f_countries']:
        st.write('Please Chose Country First.')
    else:
        st.write('BASE POINT')
        with st.form('f_road_base'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", origin_base_dict["ROAD"], key='_road_origin_base')
            with col2:
                st.selectbox("DESTINATION", destination_base_dict["ROAD"], key='_road_dist_base')
            st.form_submit_button("submit", key="f_road_base", on_click=store_form_result, args=['f_road_base'])
        if st.session_state['f_road_base']:
            store_value('road_origin_base')
            store_value('road_dist_base')
    
        if not st.session_state['status_f_road_base']:
            st.write('Chose Base Point First')
        else:
            origin_road_port = get_port_name(country_dim, st.session_state['road_origin_base'])        
            destination_road_port = get_port_name(country_dim, st.session_state['road_dist_base'])
            st.write('PORTS')
            with st.form('f_road_port'):
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("ORIGIN", origin_road_port, key='_road_origin_port')
                with col2:
                    st.selectbox("DESTINATION", destination_road_port, key='_road_dist_port')
                st.form_submit_button("submit", key="f_road_port", on_click=store_form_result, args=['f_road_port'])
            if st.session_state['f_road_port']:
                store_value('road_origin_port')
                store_value('road_dist_port')
    
            if not st.session_state['status_f_road_port']:
                st.write('Chose Ports First')
            else:
                st.write('VEHICLE SETUP')
                with st.form('f_road_vehicle'):
                    st.selectbox("VEHICLE_TYPE", road_vehicle, key='_road_vehicle_type')
                    st.selectbox("FUEL_TYPE", road_fuel,  key='_road_fuel_type')
                    st.form_submit_button("submit", key="f_road_vehicle", on_click=store_form_result, args=['f_road_vehicle'])
                if st.session_state['status_f_road_vehicle']:
                    store_value('road_vehicle_type')
                    store_value('road_fuel_type')
    return