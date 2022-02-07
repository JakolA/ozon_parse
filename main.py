from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time
import pandas as pd
import os


def get_content(urls):
    driver = webdriver.Chrome()
    names = []
    links = []
    for url in urls:
        try:
            driver.get(url)
            time.sleep(3)
            name = driver.find_element(By.CLASS_NAME, 'h1k')  # название товара
            names.append(name.text)

        except NoSuchElementException:
            names.append('Not Found')

        try:
            link = driver.find_element(By.CLASS_NAME, 'h1k').get_attribute('href')
            links.append(link)
        except NoSuchElementException:
            links.append('Not Found')

    return names, links


def main():
    df = pd.read_excel('input.xlsx', sheet_name='Лист1')
    os.remove('out.csv')
    articles = df['article'].to_list()
    urls = ['https://www.ozon.ru/search/?from_global=true&text=' + art for art in articles]

    names, links = get_content(urls)
    codes = [link.split('/')[4].split('-')[-1] if link != 'Not Found' else 'Not Found' for link in links]

    df['name'], df['code'] = names, codes

    df.to_csv('out.csv')

    return None


if __name__ == '__main__':
    main()

#  TODO по-разному показываются элементы - разные классы у тегов. Обобщить
