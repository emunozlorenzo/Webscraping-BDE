import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import requests
import src
import navbar

# Dates
@st.cache_data
def get_dates():
    get1 = requests.get('https://www.bde.es/app/sif/documentosAsociaciones/select2-periodos-es.json')
    return get1

dates = [i['id'] for i in get_dates().json()['results']]
dates_full = [i['text'] for i in get_dates().json()['results']]
dict_dates = dict(zip(dates_full, dates))

def header(url):
     st.markdown(f'<p style="background-color:#072146;color:#ffffff;font-size:36px;border-radius:10px;text-align: center;">{url}</p>', unsafe_allow_html=True)
        
header('BRE_AI_KING NEWS DATA')

current_page = 'P&L'
navbar.nav(current_page)

selector = st.selectbox("Select a Date",
                        dates_full,
                        placeholder="Select date",
                        # label_visibility='collapsed',
                        index=0,
                        key='selector')



try:
    my_bar = st.progress(0, text="Collecting Data from Banco de España")
    # Estado Financiero
    get2 = requests.get(f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dates[1]}/select2-estados-es.json')
    pnl = [i['id'] for i in get2.json()['results'][1]['children'] if i['text'] == 'Cuenta de pérdidas y ganancias consolidada pública'][0]
    url = f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dict_dates[st.session_state.selector]}/{pnl}/{pnl}_{dict_dates[st.session_state.selector]}.xls'

    my_bar.progress(75, text='Collecting Data from Banco de España')
    output = src.pnl_all(url)
    my_bar.empty()
    
    st.dataframe(output.style.applymap(lambda _: "background-color: #002D62; color: white; font-weight: bold", subset=([0,6,11,15,17,19], slice(None))),
                height=35*len(output)+38,
                width = 700,
                hide_index=True)
    
    # Ratios
    columns_to_keep = [col for col in output.columns if col != 'Importe en euros']
    ratio_row = abs(output.iloc[7][columns_to_keep] / output.iloc[6][columns_to_keep])
    ratio_row['Importe en euros'] = 'Ratio de Eficiencia'
    # output2 = output.append(ratio_row, ignore_index=True, inplace=False)
    # output2 = output2[output2['Importe en euros'] == 'Ratio de Eficiencia']
    # output2[columns_to_keep] = output2[columns_to_keep].round(3)*100
    # st.dataframe(output2,
    #             #  height=35*len(output2)+38,
    #              width = 700,
    #              hide_index=True)

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
except:
    message = st.chat_message("assistant")
    message.write("The selected date is not avalible. Please, select another date")   
