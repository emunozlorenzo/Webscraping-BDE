import streamlit as st
import numpy as np
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager



# listbox = driver.find_element(By.XPATH,'//ul[@class="select2-results__options"]')
# lista = listbox.find_elements(By.CLASS_NAME,"select2-results__option")
# dates = []
# for i in lista:
#     dates.append(i.text)
# dates = dates[1:]
dates = ['30/06/2023',
 '31/03/2023',
 '31/12/2022',
 '30/09/2022',
 '30/06/2022',
 '31/03/2022',
 '31/12/2021',
 '30/09/2021',
 '30/06/2021',
 '31/03/2021',
 '31/12/2020',
 '30/09/2020',
 '30/06/2020',
 '31/03/2020',
 '31/12/2019',
 '30/09/2019',
 '30/06/2019',
 '31/03/2019',
 '31/12/2018',
 '30/09/2018',
 '30/06/2018',
 '31/03/2018']

st.title('P&L Spanish Banks')

col1, col2 = st.columns(2)

with col1:

    selector = st.selectbox(
        '',
        dates,
        placeholder="Select date",
        label_visibility='collapsed')

with col2:
    button_load = st.button('Load Data')

if button_load:
    progress_text = "Collecting Data from Banco de España"
    my_bar = st.progress(0, text=progress_text)
    
    # Configuramos opciones
    option = ChromeOptions()
    option.add_argument("--headless=new") # No se abre interfaz gráfica
    # option.add_argument('--no-startup-window')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=option))
    # driver = webdriver.Chrome(options=option)
    # Abrir la página
    driver.get('https://app.bde.es/sifdifu/es/#/')
    my_bar.progress(15, text='Loading Page')

    # Esperamos un poco a que se cargue la página
    time.sleep(1)

    # Cerrar el diálogo de aceptar cookies pulsando el botón
    btn_cookies = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//input[@class="cookie_policy_white"]')))
    btn_cookies.click()

    # Cerrar el diálogo de aceptar cookies pulsando el botón
    btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//span[@class="select2-selection select2-selection--single"]')))
    btn.click()

    #Selector1 Fecha
    select = Select(driver.find_element(By.XPATH,'//select[@class="select2-hidden-accessible"]'))
    # select.select_by_index('1')
    select.select_by_visible_text(selector)
    my_bar.progress(30, text='Selecting Date')

    # Esperamos un poco a que se cargue la página
    time.sleep(1)

    #Selector2 Estado Financiero
    select = Select(driver.find_element(By.XPATH,'//select[@id="selecttwo"]'))
    select.select_by_index('5')
    my_bar.progress(45, text='Selecting Report')

    # Esperamos un poco a que se cargue la página
    time.sleep(1)

    #Selector3 Entidad
    select = Select(driver.find_element(By.XPATH,'//select[@id="selectmultiple"]'))
    select.select_by_index('1')
    my_bar.progress(45, text='Selecting Financial Entities')

    # Consultar
    consult = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//span[@class="ui-button-text ui-clickable"]')))
    consult.click()
    # Esperamos un poco a que se cargue la página
    time.sleep(1)

    my_bar.progress(60, text='Downloading File')
    targets = driver.find_element(By.XPATH,  '//ul[@class="horlist centered"]')
    target = targets.find_elements(By.XPATH,  '(//a[@target="_blank"])[3]')
    for t in target:
        target = t

    url = target.get_attribute('href')

    driver.quit()

    my_bar.progress(75, text='Filtering Data')
    df = pd.read_excel(url,skiprows=2)

    df[df.select_dtypes(include=['number']).columns] /= 1000000
    df = df.fillna(0)

    cols =  df.columns[df.columns.str.startswith(('0182','0049','2100','0081','0128'))].tolist()
    df = df[['Importe en euros'] + [cols[3],cols[0], cols[4], cols[1], cols[2]]]
    df.columns = ['Importe en euros','BBVA', 'Santander', 'CaixaBank', 'Sabadell', 'Bankinter']

    df['Importe en euros'] = df['Importe en euros'].replace({'  A) MARGEN DE INTERESES':'1. MARGEN DE INTERESES',
                                                         '  Ingresos por dividendos':'4. Ingresos por Dividendos',
                                                         '  Resultado de entidades valoradas por el método de la participación': '5. Resultado de entidades valoradas por el método de la participación',
                                                         '    B) MARGEN BRUTO':'5. MARGEN BRUTO',
                                                         '    (Gastos de personal)':'6. - Gastos de Personal',
                                                         '    (Otros gastos de administración)':'6. - Otros Gastos de Administración',
                                                         '  (Amortización)':'6. - Amotización',
                                                         '  (Deterioro del valor o (-) reversión del deterioro del valor y ganancias o pérdidas por modificaciones de flujos de caja de activos financieros no valorados a valor razonable con cambios en resultados y pérdidas o (-) ganancias netas por modificación)':'8. Deterioro de activos financieros no valorados a valor razonable con cambios en resultados',
                                                         '  (Provisiones o (-) reversión de provisiones)':'9. Provisiones o reversión de provisiones',
                                                         '  C) GANANCIAS O (-) PÉRDIDAS ANTES DE IMPUESTOS PROCEDENTES DE LAS ACTIVIDADES CONTINUADAS':'11. RESULTADOS ANTES DE IMPUESTOS',
                                                         '  (Gastos o (-) ingresos por impuestos sobre los resultados de las actividades continuadas)':'12. Impuestos sobre Beneficio',
                                                         '  E) RESULTADO DEL EJERCICIO':'13. RESULTADO DEL EJERCICIO',
                                                         '    Atribuible a intereses minoritarios (participaciones no dominantes)':'14. Minoritarios',
                                                         '    Atribuible a los propietarios de la dominante':'15. RESULTADO ATRIBUIDO',
                                                         })

    df = df.set_index('Importe en euros')

    # Restar la fila 1 de la fila 0 y crear una nueva fila
    df.loc['2. Comisiones Netas'] = df.iloc[9] - df.iloc[10]
    df.loc['3. Resultados de operaciones financieras'] = df.iloc[11] + df.iloc[14] + df.iloc[18] +  df.iloc[22] + df.iloc[23] + df.iloc[24]
    df.loc['5. Otros resultados de explotación'] = df.iloc[25] + (-1*df.iloc[26]) + df.iloc[28] + (-1*df.iloc[29]) 
    df.loc['6. Gastos de Explotación'] = -1*(df.iloc[30] + df.iloc[33])
    df.loc[' 6. - Gastos de Personal'] = -1*(df.loc['6. - Gastos de Personal'])
    df.loc[' 6. - Otros Gastos de Administración'] = -1*(df.loc['6. - Otros Gastos de Administración'])
    df.loc[' 6. - Amotización'] = -1*(df.loc['6. - Amotización'])
    df.loc['7. MARGEN NETO'] = df.loc['5. MARGEN BRUTO'] + df.loc['6. Gastos de Explotación']
    df.loc['8. Deterioro de activos financieros no valorados a valor razonable con cambios en resultados'] = -1*(df.loc['8. Deterioro de activos financieros no valorados a valor razonable con cambios en resultados'])
    df.loc['9. Provisiones o reversión de provisiones'] = -1*(df.loc['9. Provisiones o reversión de provisiones'])
    df.loc['10. Otros Resultados'] = (-1*df.iloc[38]) + (-1*df.iloc[39]) + df.iloc[43] + df.iloc[45]
    df.loc['12. Impuestos sobre Beneficio'] = -1*(df.loc['12. Impuestos sobre Beneficio'])
    df.loc['14. Minoritarios'] = -1*(df.loc['14. Minoritarios'])

    df = df.iloc[2:]

    output = df.loc[['1. MARGEN DE INTERESES',
                    '2. Comisiones Netas',
                    '3. Resultados de operaciones financieras',
                    '4. Ingresos por Dividendos',
                    '5. Resultado de entidades valoradas por el método de la participación',
                    '5. Otros resultados de explotación',
                    '5. MARGEN BRUTO',
                    '6. Gastos de Explotación',
                    ' 6. - Gastos de Personal',
                    ' 6. - Otros Gastos de Administración',
                    ' 6. - Amotización',
                    '7. MARGEN NETO',
                    '8. Deterioro de activos financieros no valorados a valor razonable con cambios en resultados',
                    '9. Provisiones o reversión de provisiones',
                    '10. Otros Resultados',
                    '11. RESULTADOS ANTES DE IMPUESTOS',
                    '12. Impuestos sobre Beneficio',
                    '13. RESULTADO DEL EJERCICIO',
                    '14. Minoritarios',
                    '15. RESULTADO ATRIBUIDO'
                    ]]
    my_bar.empty()
    output = output.round(0).astype(int)
    output.reset_index(inplace=True)
    output['Importe en euros'] = output['Importe en euros'].str.split('.').str[1]
    st.dataframe(
        output.style.applymap(
            lambda _: "background-color: #002D62; color: white; font-weight: bold", subset=([0,6,11,15,17,19], slice(None))
        ),
        height=35*len(output)+38,
        hide_index=True,
    )
