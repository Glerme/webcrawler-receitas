import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

url = "https://www.tudoreceitas.com/"
# Inicializa o navegador
driver = webdriver.Chrome()

ac = ActionChains(driver)

# Abre a página desejada
driver.get(url)
driver.maximize_window()
time.sleep(2)

driver.find_element(By.ID, 'q').send_keys('sobremesas', webdriver.Keys.ENTER)
time.sleep(2)

recipesTitles = driver.find_elements(
    By.CLASS_NAME, 'titulo')

linkForRecipes = []

for recipe in recipesTitles:
    recipleLink = recipe.get_attribute('href')

    if (recipleLink != None):
        linkForRecipes.append(recipleLink)


for recipeUrl in linkForRecipes:
    newDriver = webdriver.Chrome()

    newDriver.get(recipeUrl)
    elemento_ingredientes = newDriver.find_element(
        By.CSS_SELECTOR, "div.ingredientes")

    texto_ingredientes = elemento_ingredientes.text

    lista_ingredientes = texto_ingredientes.split("\n")

    print(lista_ingredientes)
