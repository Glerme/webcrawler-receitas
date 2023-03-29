import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class ReceitasScraper:
    def __init__(self, url, nome_pasta):
        self.url = url
        self.nome_pasta = nome_pasta

        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=self.chrome_options)

    def scrape(self):
        # Abre a página desejada
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(2)

        print('Entrando na tela...')

        self.driver.find_element(By.ID, 'q').send_keys(
            'sobremesas', webdriver.Keys.ENTER)
        time.sleep(2)

        recipes_titles = self.driver.find_elements(By.CLASS_NAME, 'titulo')

        link_for_recipes = []

        print('Buscando...')

        for recipe in recipes_titles:
            recipe_link = recipe.get_attribute('href')

            if (recipe_link is not None):
                print('Pegando os links das tags a', recipe_link)
                link_for_recipes.append(recipe_link)

        for recipe_url in link_for_recipes:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            new_driver = webdriver.Chrome(options=chrome_options)
            print('Buscando os ingredientes na pagina')

            new_driver.get(recipe_url)
            elemento_ingredientes = new_driver.find_element(
                By.CSS_SELECTOR, "div.ingredientes")

            texto_ingredientes = elemento_ingredientes.text

            lista_ingredientes = texto_ingredientes.split("\n")

            nome_arquivo = new_driver.title
            caminho_arquivo = os.path.join(self.nome_pasta, nome_arquivo)

            with open(caminho_arquivo, mode='w', newline='') as file:
                print('Escrevendo no .txt')
                for ingrediente in lista_ingredientes:
                    file.write(ingrediente + '\n')

            new_driver.quit()

    def close_navigator(self):
        self.driver.quit()


if __name__ == '__main__':
    scraper = ReceitasScraper('https://www.tudoreceitas.com/', 'receitas')
    scraper.scrape()
    scraper.close_navigator()
