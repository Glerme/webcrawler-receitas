import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

url = "https://www.tudoreceitas.com/"
response = requests.get(url)

# Inicializa o navegador
driver = webdriver.Chrome()

# Abre a página desejada
driver.get(url)
driver.maximize_window()
time.sleep(5)

# Obtém o conteúdo HTML da página
html = driver.page_source


ac = webdriver.ActionChains(driver)

time.sleep(2)


driver.find_element(By.ID, 'q').send_keys('sobremesas', webdriver.Keys.ENTER)


time.sleep(5)
