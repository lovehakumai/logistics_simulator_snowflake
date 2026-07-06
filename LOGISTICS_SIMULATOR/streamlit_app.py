import streamlit as st 
from page.selected_page import selected_page
from components.common.side_bar import side_bar

st.set_page_config(layout="wide")

with st.sidebar:
    side_bar()
    
selected_page()