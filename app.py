import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import src
import yfinance as yf
import navbar

def header(url):
     st.markdown(f'<p style="background-color:#072146;color:#ffffff;font-size:36px;border-radius:10px;text-align: center;">{url}</p>', unsafe_allow_html=True)
        
header('BRE_AI_KING NEWS DATA')

# Display the menu
navbar.nav('Stocks')

dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC','Unicaja':'UNI.MC', # Bancos
                'Telefónica':'TEF.MC','Iberdrola':'IBE.MC','IAG':'IAG.MC','Grifols':'GRF.MC', 'IBEX 35':'^IBEX',
                }
periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
companies = st.multiselect("Select a Company",options=sorted(list(dict_ibex35.keys())), default=sorted(list(dict_ibex35.keys()))[0], key='stock_select_box')
# companies = st.selectbox(, ,index=0,key='companies_select_box')
period_ = st.selectbox(label='Select Period', options=periods, index=5, key='stock_select_box2')

src.plot_yf(companies=companies,period=period_)

# Expander
with st.expander("Comparative Percent Performance Chart"):
    src.plot_yf_per_change(companies=companies,period=period_)

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