from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get('https://portafirmas.adif.es/ePortafirmas/Inicio.do?cr=')
time.sleep(1)
usuario = wait.until(EC.presence_of_element_located((By.ID, 'USUARIO')))
password = wait.until(EC.presence_of_element_located((By.ID, 'CLAVE')))
boton_entrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Entrar']")))

# Introduce usuario y contraseña
usuario.send_keys('2939876')
time.sleep(5)
password.send_keys('Termopilas21')
time.sleep(5)
# Haz clic en el botón "Entrar"
boton_entrar.click()

# Cierra el navegador al final


time.sleep(5)
driver.quit()
