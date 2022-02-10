import bs4
import requests
import vk_api
from selenium import webdriver


def get_dodo():
    token = "f45412cbf45412cbf45412cb17f422606fff454f45412cb947e8546cc9f371e85897262"  # Сервисный ключ доступа
    vk_session = vk_api.VkApi(token=token)
    vkApi = vk_session.get_api()

    cs = vkApi.wall.get(domain='dodo_promokodi', count=15)['items']
    cs_text = []
    for i in cs:
        cs_text.append(i['text'])
    cs_text.pop(0)
    print(cs_text)



get_dodo()
