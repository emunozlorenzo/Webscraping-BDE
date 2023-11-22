import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import time
import pandas as pd
import requests
import src

# Dates
@st.cache_data
def get_dates():
    get1 = requests.get('https://www.bde.es/app/sif/documentosAsociaciones/select2-periodos-es.json')
    return get1

dates = [i['id'] for i in get_dates().json()['results']]
dates_full = [i['text'] for i in get_dates().json()['results']]
dict_dates = dict(zip(dates_full, dates))

# st.title('IBEX 35 BANKS')
# Front Image

url = './img/img4.JPG'
st.image(url,use_column_width=True)

# horizontal menu
selected = option_menu(None, 
                       ["P&L", "+ Banks", "Stocks", 'Settings'], 
                       icons=['list-task', 'bank2', "graph-up", 'gear'], 
                       menu_icon="cast", default_index=0, orientation="horizontal",
                       styles={# "container": {"padding": "0!important", "background-color": "#fafafa"},
                               "icon": {"color": "#2DCCCD", "font-size": "20px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                               "nav-link-selected": {"background-color": "#072146"}})

if selected == 'P&L':

    selector = st.selectbox("Select a Date",
                            dates_full,
                            placeholder="Select date",
                            # label_visibility='collapsed',
                            key='selector')

    my_bar = st.progress(0, text="Collecting Data from Banco de España")

    # Estado Financiero
    get2 = requests.get(f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dates[0]}/select2-estados-es.json')
    pnl = [i['id'] for i in get2.json()['results'][1]['children'] if i['text'] == 'Cuenta de pérdidas y ganancias consolidada pública'][0]
    url = f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dict_dates[st.session_state.selector]}/{pnl}/{pnl}_{dict_dates[st.session_state.selector]}.xls'

    my_bar.progress(75, text='Collecting Data from Banco de España')
    output = src.pnl_all(url)
    my_bar.empty()
    
    st.dataframe(output.style.applymap(lambda _: "background-color: #002D62; color: white; font-weight: bold", subset=([0,6,11,15,17,19], slice(None))),
                 height=35*len(output)+38,
                 width = 700,
                 hide_index=True)

    col1, col2 = st.columns(2)

    with col1:
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False, sep=';').encode('utf-8')

        csv = convert_df(output)

        st.download_button("Download DataFrame",
                           csv,
                           "file.csv",
                           "text/csv",
                           key='download-csv')

    with col2:
        st.markdown(f'<a href="{url}" style="display: inline-block; padding: 5px 10px; background-color: #fffff; color: #454752; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: 1px solid #e0e0e2;">Download Full Data</a>',
                    unsafe_allow_html=True)
        
elif selected == "+ Banks":
        selector = st.selectbox("Select a Date",
                            dates_full,
                            placeholder="Select date",
                            # label_visibility='collapsed',
                            key='selector')
        # Estado Financiero
        get2 = requests.get(f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dates[0]}/select2-estados-es.json')
        pnl = [i['id'] for i in get2.json()['results'][1]['children'] if i['text'] == 'Cuenta de pérdidas y ganancias consolidada pública'][0]
        url = f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dict_dates[st.session_state.selector]}/{pnl}/{pnl}_{dict_dates[st.session_state.selector]}.xls'
        ent = requests.get(f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dict_dates[st.session_state.selector]}/{pnl}/select2-entidades-es.json')
        banks = [i['text'] for i in ent.json()['results']]
        
        selector_banks = st.selectbox("Select a Bank",
                            banks,
                            placeholder="Select date",
                            # label_visibility='collapsed',
                            index=2,
                            key='banks')
        

        output = src.pnl_bank(url, st.session_state.banks)

    
        st.dataframe(output.style.applymap(lambda _: "background-color: #002D62; color: white; font-weight: bold", subset=([0,6,11,15,17,19], slice(None))),
                     height=35*len(output)+38,
                     width = 700,
                     hide_index=True)

        col1, col2 = st.columns(2)

        with col1:
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False, sep=';').encode('utf-8')

            csv = convert_df(output)

            st.download_button("Download DataFrame",
                               csv,
                               "file.csv",
                               "text/csv",
                               key='download-csv')

        with col2:
            st.markdown(f'<a href="{url}" style="display: inline-block; padding: 5px 10px; background-color: #fffff; color: #454752; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; border: 1px solid #e0e0e2;">Download Full Data</a>',
                        unsafe_allow_html=True)
            
elif selected == 'Stocks':
    dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC'}
    periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
    companies = st.multiselect("Select a Company",options=sorted(list(dict_ibex35.keys())), default=sorted(list(dict_ibex35.keys()))[0], key='stock_select_box')
    # companies = st.selectbox(, ,index=0,key='companies_select_box')
    period_ = st.selectbox(label='Select Period', options=periods, index=5, key='stock_select_box2')
    
    src.plot_yf(companies=companies,period=period_)

    
    
        




