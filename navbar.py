import streamlit as st
from streamlit_option_menu import option_menu

# Define the pages and their file paths
pages = {'Stocks':'app.py',
         'P&L':'p&l.py',
         '+Banks':'banks.py'}

# Create a list of the page names
page_list = list(pages.keys())

def nav(current_page=page_list[0]):
    p = option_menu(None,
        page_list,
        icons=['list-task', 'bank2', "graph-up"],
        menu_icon="cast",
        default_index=page_list.index(current_page), 
        orientation="horizontal",
        styles={# "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#2DCCCD", "font-size": "14px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"font-size": "14px", "background-color": "#072146"}})

    if current_page != p:
        if p == 'Stocks':
            path_to_page = os.path.join(os.getcwd(), "app.py")
        else:
            path_to_page = os.path.join(os.getcwd(), "pages", pages[p])
        st.switch_page(path_to_page)


