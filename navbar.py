import streamlit as st
from streamlit_option_menu import option_menu

# Define the pages and their file paths
pages = {'Stocks':'app2.py',
         'P&L':'pages/p&l.py',
         '+Banks':'pages/banks.py'}

# Create a list of the page names
page_list = list(pages.keys())

def nav(current_page=page_list[0]):
    p = option_menu(None, page_list, 
        default_index=page_list.index(current_page), 
        menu_icon="cast",
        orientation="horizontal",
        styles={# "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#2DCCCD", "font-size": "14px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"font-size": "14px", "background-color": "#072146"}})

    if current_page != p:
        st.switch_page(pages[p])