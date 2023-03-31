import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


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
        time.sleep(5)

        print('Entrando na tela...')

        # Pesquisar por sobremesas salgadas
        self.driver.find_element(By.ID, 'q').send_keys(
            'sobremesas salgadas', webdriver.Keys.ENTER)
        time.sleep(5)

        salgadas_titles = self.driver.find_elements(By.CLASS_NAME, 'titulo')

        salgadas_links = []

        print('Buscando sobremesas salgadas...')

        for recipe in salgadas_titles:
            recipe_link = recipe.get_attribute('href')

            if (recipe_link is not None):
                print('Pegando os links das sobremesas salgadas', recipe_link)
                salgadas_links.append(recipe_link)

            if len(salgadas_links) >= 10:
                break

        # Pesquisar por sobremesas doces
        self.driver.find_element(By.ID, 'q').clear()
        self.driver.find_element(By.ID, 'q').send_keys(
            'sobremesas doces', webdriver.Keys.ENTER)
        time.sleep(2)

        doces_titles = self.driver.find_elements(By.CLASS_NAME, 'titulo')

        doces_links = []

        print('Buscando sobremesas doces...')

        for recipe in doces_titles:
            recipe_link = recipe.get_attribute('href')

            if (recipe_link is not None):
                print('Pegando os links das sobremesas doces', recipe_link)
                doces_links.append(recipe_link)

            if len(doces_links) >= 10:
                break

        all_links = salgadas_links + doces_links

        for recipe_url in all_links:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--blink-settings=imagesEnabled=false")
            chrome_options.add_argument("--disable-javascript")

            new_driver = webdriver.Chrome(options=chrome_options)
            print('Buscando os ingredientes na pagina')

            new_driver.get(recipe_url)
            new_driver.maximize_window()
            time.sleep(5)

            try:
                elemento_ingredientes = new_driver.find_element(
                    By.CSS_SELECTOR, "div.ingredientes")

                texto_ingredientes = elemento_ingredientes.text

                lista_ingredientes = texto_ingredientes.split("\n")

                nome_arquivo = new_driver.title
                caminho_arquivo = os.path.join(self.nome_pasta, nome_arquivo)

                with open(caminho_arquivo, mode='w', newline='') as file:
                    for ingrediente in lista_ingredientes:
                        print('Escrevendo no .txt', ingrediente)
                        file.write(ingrediente + '\n')

            except NoSuchElementException:
                print('Não foi possível encontrar a div de ingredientes')
                continue

            new_driver.quit()

    def close_navigator(self):
        self.driver.quit()


if __name__ == '__main__':
    scraper = ReceitasScraper('https://www.tudoreceitas.com/', 'receitas')
    scraper.scrape()
    scraper.close_navigator()
