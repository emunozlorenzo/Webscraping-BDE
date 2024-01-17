import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Span
from bokeh.plotting import figure
import yfinance as yf
import streamlit as st

def pnl_all(url):
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
    output = output.round(0).astype(int)
    output.reset_index(inplace=True)
    output['Importe en euros'] = output['Importe en euros'].str.split('.').str[1]
    return output


def pnl_bank(url, bank):
    df = pd.read_excel(url,skiprows=2)

    df[df.select_dtypes(include=['number']).columns] /= 1000000
    df = df.fillna(0)

    cols =  df.columns[df.columns.str.startswith(bank[0:4])].tolist()
    df = df[['Importe en euros']+ cols]
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
    output = output.round(0).astype(int)
    output.reset_index(inplace=True)
    output['Importe en euros'] = output['Importe en euros'].str.split('.').str[1]
    return output

def plot_yf(companies,period):
    dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC','Unicaja':'UNI.MC', # Bancos
                   'Telefónica':'TEF.MC','Iberdrola':'IBE.MC','IAG':'IAG.MC','Grifols':'GRF.MC', 'IBEX 35':'^IBEX',
                  }
    dict_color = {'BBVA':'#004481','Santander':'#ec0000','Sabadell':'#0099cc','CaixaBank':'#000000','Bankinter':'#ff7300','Unicaja':'#4E9E47', # Bancos
                  'Telefónica':'#003145','Iberdrola':'#759F2F','IAG':'#DA162A','Grifols':'#004186',
                 }
    p = figure(height =250, x_axis_type="datetime", tools="", toolbar_location=None,
               title=",".join(companies), sizing_mode="scale_width")
    p.background_fill_color="#f5f5f5"
    p.grid.grid_line_color="white"
    p.yaxis.axis_label = 'Price'
    p.axis.axis_line_color = None
    for company in companies:
        comp = yf.Ticker(dict_ibex35[company])
        if period != '1d':
            hist = comp.history(period=period, auto_adjust = False)
            close = hist[['Close','Volume']]
            close.index = close.index.strftime('%Y-%m-%d')
            close['Date'] = pd.to_datetime(close.index, format='%Y-%m-%d')
            close["DateString"] = close["Date"].dt.strftime("%Y-%m-%d")
            close['Name'] = company
        else:
            hist = comp.history(period=period, auto_adjust = False, interval='5m')
            close = hist[['Close','Volume']]
            close.index = close.index.strftime('%Y-%m-%d %HH:%MM')
            close['Date'] = pd.to_datetime(close.index, format='%Y-%m-%d %HH:%MM')
            close["DateString"] = close["Date"].dt.strftime("%Y-%m-%d")
            close['Name'] = company
        source = ColumnDataSource(data={
            'name': close['Name'],
            'date'      : close['Date'],
            'adj close' : close['Close'],
            'volume'    : close['Volume'],
        })
        p.line(x='date', y='adj close', line_width=2, color=dict_color[company], source=source)
    p.add_tools(
        HoverTool(
            tooltips=[
                ( 'Company',   '@name'          ),
                ( 'Date',   '@date{%F}'            ),
                ( 'Close',  '@{adj close}{%0.2f}€' ), # use @{ } for field names with spaces
                ( 'Volume', '@volume{0.00 a}'      ),
            ],

            formatters={
                '@date'        : 'datetime', # use 'datetime' formatter for '@date' field
                '@{adj close}' : 'printf',   # use 'printf' formatter for '@{adj close}' field
                                             # use default 'numeral' formatter for other fields
            },

            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='mouse'
        )
    )
    return st.bokeh_chart(p, use_container_width=True)

def plot_yf_per_change(companies,period):
    dict_ibex35 = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC','CaixaBank':'CABK.MC','Bankinter':'BKT.MC','Unicaja':'UNI.MC', # Bancos
                   'Telefónica':'TEF.MC','Iberdrola':'IBE.MC','IAG':'IAG.MC','Grifols':'GRF.MC', 'IBEX 35':'^IBEX',
                  }
    dict_color = {'BBVA':'#004481','Santander':'#ec0000','Sabadell':'#0099cc','CaixaBank':'#000000','Bankinter':'#ff7300','Unicaja':'#4E9E47', # Bancos
                  'Telefónica':'#003145','Iberdrola':'#759F2F','IAG':'#DA162A','Grifols':'#004186','IBEX 35':'#ffa500',
                 }
    p = figure(height =250, x_axis_type="datetime", tools="", toolbar_location=None,
               sizing_mode="scale_width")
    p.background_fill_color="#f5f5f5"
    p.grid.grid_line_color="white"
    p.yaxis.axis_label = 'Percentage'
    p.axis.axis_line_color = None
    for company in companies:
        comp = yf.Ticker(dict_ibex35[company])
        if period != '1d':
            hist = comp.history(period=period, auto_adjust = False)
            hist = hist[1:]
            first_value = hist['Close'].round(2)[0]
            hist['Change'] = ((hist['Close'].round(2)/first_value)-1)*100
            close = hist[['Close','Change']]
            close.index = close.index.strftime('%Y-%m-%d')
            close['Date'] = pd.to_datetime(close.index, format='%Y-%m-%d')
            close["DateString"] = close["Date"].dt.strftime("%Y-%m-%d")
            close['Name'] = company
        else:
            hist = comp.history(period=period, auto_adjust = False, interval='5m')
            hist = hist[1:]
            first_value = hist['Close'].round(2)[0]
            hist['Change'] = ((hist['Close'].round(2)/first_value)-1)*100
            close = hist[['Close','Change']]
            close.index = close.index.strftime('%Y-%m-%d %HH:%MM')
            close['Date'] = pd.to_datetime(close.index, format='%Y-%m-%d %HH:%MM')
            close["DateString"] = close["Date"].dt.strftime("%Y-%m-%d")
            close['Name'] = company
        source = ColumnDataSource(data={
            'name': close['Name'],
            'date': close['Date'],
            'change': close['Change'],
            'close': close['Close'],
        })
        p.line(x='date', y='change', line_width=2, color=dict_color[company], source=source)
        p.add_tools(
            HoverTool(
                tooltips=[
                    ( 'Company',   '@name'          ),
                    ( 'Date',   '@date{%F}'          ),
                    ( '% Change',  '@{change}{%0.2f}%' ), # use @{ } for field names with spaces
                    ( 'Close', '@close{0.00 a}'      ),
                ],

                formatters={
                    '@date'     : 'datetime', # use 'datetime' formatter for '@date' field
                    '@{change}' : 'printf',   # use 'printf' formatter for '@{adj close}' field
                                              # use default 'numeral' formatter for other fields
                },

                # display a tooltip whenever the cursor is vertically in line with a glyph
                mode='mouse'
            )
        )
    # Agregar la línea horizontal en y=0
    zero_line = Span(location=0, dimension='width', line_color='#434b4d', line_width=1, line_dash='solid')
    p.add_layout(zero_line)
    return st.bokeh_chart(p, use_container_width=True)
