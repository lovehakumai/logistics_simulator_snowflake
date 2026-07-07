import streamlit as st 
class Side_bar:
    def __init__(self):
        session_state_key_dict = {
            "current_page": "analytics"
        }
        for key, val in session_state_key_dict.items():
            if key not in st.session_state:
                st.session_state[key] = val 

        self.page_map = {
                    "analytics": "📊ANALYTICS",
                    "monitor": "💰MONITOR",
                    "setup": "⚙️SETUP"
                }
        self.page_list = list(self.page_map.keys())
        
    def change_page(self):
        if 'sb_navigation' in st.session_state:
            chosen_api_name = st.session_state['sb_navigation']
            st.session_state['current_page'] = chosen_api_name 

    def get_value(self, key_name):
        return st.session_state[key_name]