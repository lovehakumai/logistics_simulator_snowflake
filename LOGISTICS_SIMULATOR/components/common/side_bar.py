import streamlit as st 
from classes.common.side_bar import Side_bar

def side_bar():
    side_bar = Side_bar()
    st.title('Logistics Simulator')
    st.write('---')
    selected_page = st.radio(
        "Navigation",
        options=side_bar.page_list,
        label_visibility="collapsed",
        format_func = lambda x: side_bar.page_map[x],
        on_change=side_bar.change_page,
        key = 'sb_navigation'
    )
    
    