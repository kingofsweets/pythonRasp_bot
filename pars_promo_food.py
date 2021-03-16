import bs4
import requests
from selenium import webdriver


def get_dodo():
    link = 'https://www.pepper.ru/coupons/dodopizza.ru'
    browser = webdriver.Chrome(executable_path = 'C:/chromedriver.exe')

    browser.get(link)
    generated_html = browser.page_source


    soup = bs4.BeautifulSoup(generated_html, 'html.parser')
    promos = soup.find_all('input')
    promos_va = []
    for promo in promos:
        promos_va.append(promo.value)
    print(promos)
    input()


get_dodo()
