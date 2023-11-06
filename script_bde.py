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

# Configuramos opciones
option = ChromeOptions()
# option.add_argument('--headless') # No se abre interfaz gráfica
option.add_argument('--disable-notifications') # Evitar que nos pregunte si queremos recibir notificaciones y otras cosas
option.add_experimental_option('detach', True) # Evitar que el navegador se cierre al terminar
option.add_argument('--window-size=800,600') # La página es responsive, forzamos el tamaño porque si no los elementos cambian de nombre
prefs = {
    "download.default_directory": "C:/Users/aranc/Downloads/prueba",
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
}

option.add_experimental_option("prefs", prefs)
# option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=option))

# Abrir la página
driver.get('https://app.bde.es/sifdifu/es/#/')

# Esperamos un poco a que se cargue la página
time.sleep(3)

# Cerrar el diálogo de aceptar cookies pulsando el botón
btn_cookies = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//input[@class="cookie_policy_white"]')))
btn_cookies.click()

#Selector1 Fecha
select = Select(driver.find_element(By.XPATH,'//select[@class="select2-hidden-accessible"]'))
select.select_by_index('1')

# Esperamos un poco a que se cargue la página
time.sleep(1)

#Selector2 Estado Financiero
select = Select(driver.find_element(By.XPATH,'//select[@id="selecttwo"]'))
select.select_by_index('5')

# Esperamos un poco a que se cargue la página
time.sleep(1)

#Selector3 Entidad
select = Select(driver.find_element(By.XPATH,'//select[@id="selectmultiple"]'))
select.select_by_index('1')

# Consultar
consult = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//span[@class="ui-button-text ui-clickable"]')))
consult.click()

# Consultar
consult = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//span[@class="fa fa-4x fa-file-o fa-file-custom fa-file-excel"]')))
consult.click()

# Esperamos un poco a que se cargue la página
time.sleep(1)
