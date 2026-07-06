import streamlit as st
from classes.setup.setup_state import Setup_state
from classes.setup.setup_data import Setup_data

def form_template(setup_state:Setup_state, setup_data:Setup_data, transport_mode_low):
    
    transport_mode_up = transport_mode_low.upper()
# ========================================================================================================
# Base Points
# ========================================================================================================
    if not st.session_state['status_f_countries']:
        st.write('Chose Country First.')
    else:
        st.write('BASE POINT')
        
        st.session_state[f'_{transport_mode_low}_origin_base_dict'] = setup_data.get_base_point(setup_state.get_value('origin_country'))
        st.session_state[f'_{transport_mode_low}_destination_base_dict'] = setup_data.get_base_point(setup_state.get_value('destination_country'))
        setup_state.store_value(f'{transport_mode_low}_origin_base_dict')
        setup_state.store_value(f'{transport_mode_low}_destination_base_dict')
        
        with st.form(f'form_{transport_mode_low}_base'):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("ORIGIN", st.session_state[f'{transport_mode_low}_origin_base_dict'][transport_mode_up], key=f'_{transport_mode_low}_origin_base')
            with col2:
                st.selectbox("DESTINATION", st.session_state[f'{transport_mode_low}_destination_base_dict'][transport_mode_up], key=f'_{transport_mode_low}_dest_base')
            st.form_submit_button("submit", key=f"f_{transport_mode_low}_base", on_click=setup_state.store_status_value, args=[f'f_{transport_mode_low}_base'])
            
        if st.session_state[f'f_{transport_mode_low}_base']:
            setup_state.store_value(f'{transport_mode_low}_origin_base')
            setup_state.store_value(f'{transport_mode_low}_dest_base')
            
            st.session_state[f'_{transport_mode_low}_origin_port_list'] = setup_data.get_port_name(setup_state.get_value(f'{transport_mode_low}_origin_base'))
            setup_state.store_value(f'{transport_mode_low}_origin_port_list')
            st.session_state[f'_{transport_mode_low}_destination_port_list'] = setup_data.get_port_name(setup_state.get_value(f'{transport_mode_low}_dest_base'))
            setup_state.store_value(f'{transport_mode_low}_destination_port_list')

# ========================================================================================================
# Ports
# ========================================================================================================
        if not st.session_state[f'status_f_{transport_mode_low}_base']:
            st.write('Chose Base Point First')
        else:
            origin_port = setup_state.get_value(f'{transport_mode_low}_origin_port_list')
            destination_port = setup_state.get_value(f'{transport_mode_low}_destination_port_list')

            st.write('PORTS')
            with st.form(f'form_{transport_mode_low}_port'):
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("ORIGIN", origin_port[transport_mode_up], key=f'_{transport_mode_low}_origin_port')
                with col2:
                    st.selectbox("DESTINATION", destination_port[transport_mode_up], key=f'_{transport_mode_low}_dest_port')
                st.form_submit_button("submit", key=f"f_{transport_mode_low}_port", on_click=setup_state.store_status_value, args=[f'f_{transport_mode_low}_port'])
            if st.session_state[f'f_{transport_mode_low}_port']:
                setup_state.store_value(f'{transport_mode_low}_origin_port')
                setup_state.store_value(f'{transport_mode_low}_dest_port')
# ========================================================================================================
# Vehicle Params
# ========================================================================================================
            if not st.session_state[f'status_f_{transport_mode_low}_port']:
                st.write('Chose Ports First')
            else:
                st.write('VEHICLE SETUP')
                # ---------------------------------------------------------------------------------------
                # Air
                # ---------------------------------------------------------------------------------------
                if transport_mode_low == 'air':
                    setup_data.update_air_params()
                    with st.form(f'form_{transport_mode_low}_vehicle'):
                        st.selectbox("DISTANCE", setup_data.air_distance, key='_air_distance')
                        st.selectbox("VEHICLE_TYPE", setup_data.air_vehicle, key='_air_vehicle_type')
                        st.selectbox("FUEL_TYPE", setup_data.air_fuel, key='_air_fuel_type')
                        st.form_submit_button("submit", key="f_air_vehicle", on_click=setup_state.store_status_value, args=['f_air_vehicle'])
                    if st.session_state['status_f_air_vehicle']:
                        setup_state.store_value('air_distance')
                        setup_state.store_value('air_vehicle_type')
                        setup_state.store_value('air_fuel_type')
                # ---------------------------------------------------------------------------------------
                # Sea
                # ---------------------------------------------------------------------------------------
                elif transport_mode_low == 'sea':
                    setup_data.update_sea_params()
                    with st.form('form_sea_vehicle'):
                        st.selectbox("SIZE", setup_data.sea_size, key='_sea_size')
                        st.selectbox("VEHICLE_TYPE", setup_data.sea_vehicle, key='_sea_vehicle_type')
                        st.selectbox("FUEL_TYPE", setup_data.sea_fuel, key='_sea_fuel_type')
                        st.form_submit_button("submit", key="f_sea_vehicle", on_click=setup_state.store_status_value, args=['f_sea_vehicle'])
                    if st.session_state['status_f_sea_vehicle']:
                        setup_state.store_value('sea_size')
                        setup_state.store_value('sea_vehicle_type')
                        setup_state.store_value('sea_fuel_type')
                # ---------------------------------------------------------------------------------------
                # Road
                # ---------------------------------------------------------------------------------------
                elif transport_mode_low == 'road':
                    setup_data.update_road_params()
                    with st.form('form_road_vehicle'):
                        st.selectbox("VEHICLE_TYPE", setup_data.road_vehicle, key='_road_vehicle_type')
                        st.selectbox("FUEL_TYPE", setup_data.road_fuel,  key='_road_fuel_type')
                        st.form_submit_button("submit", key="f_road_vehicle", on_click=setup_state.store_status_value, args=['f_road_vehicle'])
                    if st.session_state['status_f_road_vehicle']:
                        setup_state.store_value('road_vehicle_type')
                        setup_state.store_value('road_fuel_type')
                # ---------------------------------------------------------------------------------------
                # Rail
                # ---------------------------------------------------------------------------------------
                elif transport_mode_low == 'rail':
                    setup_data.update_rail_params()
                    with st.form('form_rail_vehicle'):
                        st.selectbox("VEHICLE_TYPE", setup_data.rail_vehicle, key='_rail_vehicle_type')
                        st.selectbox("FUEL_TYPE", setup_data.rail_fuel,  key='_rail_fuel_type')
                        st.form_submit_button("submit", key="f_rail_vehicle", on_click=setup_state.store_status_value, args=['f_rail_vehicle'])
                    if st.session_state['status_f_rail_vehicle']:
                        setup_state.store_value('rail_vehicle_type')
                        setup_state.store_value('rail_fuel_type')   
                    
    return 