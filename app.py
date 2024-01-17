import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import time
import pandas as pd
import requests
import src
import yfinance as yf

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


# url = './img/img4.JPG'
# st.image(url,use_column_width=True)

# horizontal menu
selected = option_menu(None, 
                       ["Stocks", "P&L", "+Banks"], 
                       icons=['list-task', 'bank2', "graph-up"], 
                       menu_icon="cast", default_index=0, orientation="horizontal",
                       styles={# "container": {"padding": "0!important", "background-color": "#fafafa"},
                               "icon": {"color": "#2DCCCD", "font-size": "14px"}, 
                               "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                               "nav-link-selected": {"font-size": "14px", "background-color": "#072146"}})

if selected == 'P&L':

    selector = st.selectbox("Select a Date",
                            dates_full,
                            placeholder="Select date",
                            # label_visibility='collapsed',
                            index=1,
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
        
elif selected == "+Banks":
    try:
        selector = st.selectbox("Select a Date",
                            dates_full,
                            placeholder="Select date",
                            # label_visibility='collapsed',
                            index=1,
                            key='selector')
        # Estado Financiero
        get2 = requests.get(f'https://www.bde.es/app/sif/documentosAsociaciones/periodos/{dates[1]}/select2-estados-es.json')
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
        my_bar = st.progress(0, text="Collecting Data from Banco de España")
        my_bar.progress(75, text='Collecting Data from Banco de España')
        output = src.pnl_bank(url, st.session_state.banks)
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
    except:
        message = st.chat_message("assistant")
        message.write("The selected date is not avalible. Please, select another date") 
            
elif selected == 'Stocks':
    dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC','Unicaja':'UNI.MC', # Bancos
                   'Telefónica':'TEF.MC','Iberdrola':'IBE.MC','IAG':'IAG.MC','Grifols':'GRF.MC',
                  }
    periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
    companies = st.multiselect("Select a Company",options=sorted(list(dict_ibex35.keys())), default=sorted(list(dict_ibex35.keys()))[0], key='stock_select_box')
    # companies = st.selectbox(, ,index=0,key='companies_select_box')
    period_ = st.selectbox(label='Select Period', options=periods, index=5, key='stock_select_box2')
    
    src.plot_yf(companies=companies,period=period_)
    
    def header(url):
         st.markdown(f'<p style="background-color:#072146;color:#ffffff;font-size:20px;border-radius:10px;text-align: center;">{url}</p>', unsafe_allow_html=True)

    header('Last Update')
    
    def last_update():
        dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC'}
        dict_img = {'BBVA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/BBVA_2019.svg/238px-BBVA_2019.svg.png',
                    'Santander': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Banco_Santander_Logotipo.svg/238px-Banco_Santander_Logotipo.svg.png',
                    'Sabadell': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/BSabadell_Logo.svg/238px-BSabadell_Logo.svg.png',
                    'CaixaBank': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Logo_CaixaBank.svg/238px-Logo_CaixaBank.svg.png',
                    'Bankinter': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Bankinter.svg/238px-Bankinter.svg.png'}
        df = pd.DataFrame()
        for k,v in dict_ibex35.items():
            comp = yf.Ticker(v)
            hist = comp.history(period='1d')
            hist.reset_index(inplace=True)
            hist['Dividend Yield'] = (comp.info['dividendRate']/hist['Close'][0])*100
            hist['Bank'] = dict_img[k]
            df = pd.concat([df, hist], ignore_index=True, sort=False)

        df.drop(columns=['Date','Dividends','Stock Splits','Volume'], inplace=True)
        cols = df.columns
        return df[['Bank']+cols[0:5].to_list()]
    table = last_update()
    table[table.columns[1:]] = table[table.columns[1:]].round(2)
    table.rename(columns={'Close':'Close/Current'}, inplace=True)
    
    # st.dataframe(table,#.style.applymap(lambda _: "background-color: #002D62; color: white; font-weight: bold"),
    #              height=35*len(table)+38,
    #              width = 700,
    #              hide_index=True)
    st.data_editor(
    table,
    column_config={
        "Bank": st.column_config.ImageColumn(
            "Bank", help="Streamlit app preview screenshots",
            width='medium',
        ),
        # "Dividend Yield": st.column_config.NumberColumn(
        # "Stock Dividend Yield",
        # help="Stock Dividend Yield",
        # min_value=0,
        # max_value=1000,
        # step=1,
        # format="%.2f%",)
    },
     height=35*len(table)+38,
     width = 700,
     hide_index=True)


    
    
        




