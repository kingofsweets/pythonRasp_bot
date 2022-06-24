# Импортируем библиотеки

import random
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from chatterbot.trainers import ListTrainer
import requests
from bs4 import BeautifulSoup
from chatterbot import ChatBot

# Создаем экземпляр пространства для бота
# chatbot = ChatBot("Умный чел")
# trainer = ListTrainer(chatbot)
# # Открываем файлы с датасетами
# # t1 = open('anim_0.txt', 'r', encoding='utf-8').readlines()
# # t2 = open('anim_1.txt', 'r', encoding='utf-8').readlines()
# t3 = open('Data_sets/Типичный японский боевик.txt', 'r', encoding='utf-8').readlines()
# t4 = open('Data_sets/Яп_2.txt', 'r', encoding='utf-8').readlines()


# # Подгружаем данные для тренировки бота
# # trainer.train(t1)
# # trainer.train(t2)
# trainer.train(t3)
# trainer.train(t4)

# Создаем функции ответа бота для каждого типа клавиатуры
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/mainklav.json", "r", encoding="UTF-8").read()})


def write_msggs(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/mainklav.json", "r", encoding="UTF-8").read()})


def bazar(id):
    a = vk.method('docs.getUploadServer')
    b = requests.post(a['upload_url'], files={'file': open('say.mp3', 'rb')}).json()
    c = vk.method("docs.save", {"file": b["file"]})[0]
    d = 'doc{}_{}'.format(c['owner_id'], c['id'])
    vk.method('messages.send', {'peer_id': id, 'attachment': d, "random_id": random.randint(1, 2147483647)})


def write_msginbeseda(chat_id, message):
    vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': random.getrandbits(64)})


def write_msgwbot(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/vbot.json", "r", encoding="UTF-8").read()})


def write_msginrasptek(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/raspklav.json", "r", encoding="UTF-8").read()})


def write_msginraspsled(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/raspsledklav.json", "r", encoding="UTF-8").read()})


def write_msgmaininf(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/info.json", "r", encoding="UTF-8").read()})

def write_msgback(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/return.json", "r", encoding="UTF-8").read()})
    
def write_msgback_lof(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/return_copy.json", "r", encoding="UTF-8").read()})
    
def write_kafedra(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("common/keyboards/kafedra.json", "r", encoding="UTF-8").read()})


# Подлюкчаем токен группы
token = "448a161c4370d920f09782b8ea67453e58f64ebe60444d3a6e3c99de30c1f6214ff9e838e3f713e7ee246"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

# Парсим расписание с сайта первака
abs = 'https://ictis.alex-b.me/48.htm'
r = requests.get(abs)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')

pars = []
timel = []
pnd = []
vt = []
sred = []
chetv = []
pyatnica = []
subbota = []
for tr in table.find_all('tr'):
    tds = tr.find_all('td')
    for td in tds:
        pars.append(td.get_text())
for i in range(len(pars)):
    if pars[i] == '':
        pars[i] = 'Окно'
for i in range(len(pars)):
    if 8 < i < 16:
        timel.append(pars[i])

for i in range(len(pars)):
    if 15 < i < 24:
        pnd.append(pars[i])

print(pnd)
for i in range(len(pars)):
    if 23 < i < 32:
        vt.append(pars[i])
for i in range(len(pars)):
    if 31 < i < 40:
        sred.append(pars[i])
for i in range(len(pars)):
    if 39 < i < 48:
        chetv.append(pars[i])
for i in range(len(pars)):
    if 47 < i < 56:
        pyatnica.append(pars[i])
for i in range(len(pars)):
    if 55 < i < 64:
        subbota.append(pars[i])

url = 'https://ictis.alex-b.me/48.htm'
m = requests.get(url)

soup1 = BeautifulSoup(m.text, 'html.parser')
table1 = soup1.find('table')
pars1 = []
pnd1 = []
vt1 = []
sred1 = []
chetv1 = []
pyatnica1 = []
subbota1 = []
for tr in table1.find_all('tr'):
    tds = tr.find_all('td')
    for td in tds:
        pars1.append(td.get_text())
for i in range(len(pars1)):
    if pars1[i] == '':
        pars1[i] = 'Окно'

for i in range(len(pars1)):
    if 15 < i < 24:
        pnd1.append(pars1[i])
print(pnd1)
for i in range(len(pars1)):
    if 23 < i < 32:
        vt1.append(pars1[i])
for i in range(len(pars1)):
    if 31 < i < 40:
        sred1.append(pars1[i])
for i in range(len(pars1)):
    if 39 < i < 48:
        chetv1.append(pars1[i])
for i in range(len(pars1)):
    if 47 < i < 56:
        pyatnica1.append(pars1[i])
for i in range(len(pars1)):
    if 55 < i < 64:
        subbota1.append(pars1[i])

# Запускаем цикл с телом бота

while True:
    # Классический режим бота
    for event in longpoll.listen():
        # Если пришло сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            # Влс
            if event.to_me:

                request = event.text

                if request == "/Help" or request == "/help":
                    write_msg(event.user_id, ''''
                    Вас приветсвует помощник в исользовании бота.
                    Список команд(Регситр первой буквы не учитываеся):
                    /Расписание (день недели) - узнать расписание в определённый день( день недели указывать без скобок)
                    /Help - список команд
                    Остальные сообщения будут рассматриваться ботом как общение, он начнёт пудрить вам мозги.
                    Желаем удачи!


                    ''')
                if request == "Расписание: текущая неделя":
                    write_msginrasptek(event.user_id, 'Выберите день:')
                elif request == 'N!Понедельник':
                    for i in range(len(pnd)):
                        if i == 0:
                            write_msg(event.user_id, str(pnd[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + pnd[i]))
                elif request == 'N!Вторник':
                    for i in range(len(vt)):
                        if i == 0:
                            write_msg(event.user_id, str(vt[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + vt[i]))
                elif request == 'N!Среда':
                    for i in range(len(sred)):
                        if i == 0:
                            write_msg(event.user_id, str(sred[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + sred[i]))
                elif request == 'N!Четверг':
                    for i in range(len(chetv)):
                        if i == 0:
                            write_msg(event.user_id, str(chetv[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + chetv[i]))
                elif request == 'N!Пятница':
                    for i in range(len(pyatnica)):
                        if i == 0:
                            write_msg(event.user_id, str(pyatnica[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + pyatnica[i]))
                elif request == 'N!Суббота':
                    for i in range(len(subbota)):
                        if i == 0:
                            write_msg(event.user_id, str(subbota[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + subbota[i]))

                if request == "Расписание: следующая неделя":
                    write_msginraspsled(event.user_id, 'Выберите день:')
                elif request == 'S!Понедельник':
                    for i in range(len(pnd1)):
                        if i == 0:
                            write_msg(event.user_id, str(pnd1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + pnd1[i]))
                elif request == 'S!Вторник':
                    for i in range(len(vt1)):
                        if i == 0:
                            write_msg(event.user_id, str(vt1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + vt1[i]))
                elif request == 'S!Среда':
                    for i in range(len(sred1)):
                        if i == 0:
                            write_msg(event.user_id, str(sred1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + sred1[i]))
                elif request == 'S!Четверг':
                    for i in range(len(chetv1)):
                        if i == 0:
                            write_msg(event.user_id, str(chetv1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + chetv1[i]))
                elif request == 'S!Пятница':
                    for i in range(len(pyatnica1)):
                        if i == 0:
                            write_msg(event.user_id, str(pyatnica1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + pyatnica1[i]))
                elif request == 'S!Суббота':
                    for i in range(len(subbota1)):
                        if i == 0:
                            write_msg(event.user_id, str(subbota1[i]))
                        else:
                            write_msg(event.user_id, str(timel[i - 1] + ': ' + subbota1[i]))
                elif request == 'Включить душевные беседы':
                    write_msgwbot(event.user_id, 'Переключемся. Напишите что-нибудь')
                    break
                elif request == 'Для абитуриентов':
                    write_msgmaininf(event.user_id, 'Основная информация')
                elif request == 'Информация по хэштегам':
                    write_msgback(event.user_id, '''
                              Хэштеги для поиска по стене в группе:

#кафедраСАиТ@sait_ictis — наш хэштег в сети
#абитуриенту@sait_ictis — информация для поступающих
#студенту@sait_ictis — информация для студентов
#статья@sait_ictis — полезные и интересные IT статьи
#видеокурс@sait_ictis — видеоматериалы для самообучения
#книга@sait_ictis — полезные книги про IT и не только
#вакансия@sait_ictis — IT вакансии, стажировки
#карьера@sait_ictis — материалы для построения успешной карьеры в IT
#конференция@sait_ictis, #хакатон@sait_ictis — информация о проводимых мероприятиях
                              ''')
                elif request == 'Расписание по физ-ре':
                    write_msgback(event.user_id, '''
                              Актуальное расписание занятий по физической культуре. Не забудьте взять с собой Медицинскую справку и карту-пропуск!

Актуальная информация дисциплины - https://vk.com/club101308251
                              ''')
                elif request == 'Контактная информация':
                    write_msgback(event.user_id, '''
                              Контактная информация:

Тел.: +7 (8634) 37-17-87
Email: skucherov@sfedu.ru
Сайт - sait.sfedu.ru
Адрес - ул. Энгельса, 1 ауд. Г-137
                              ''')
                elif request == 'Вернуться к основной информации':
                    write_msgmaininf(event.user_id, 'Основная информация')
                
                elif request == 'Информация про кафедру':
                    write_kafedra(event.user_id, 'Что именно вы хотите узнать?')
                
                elif request == 'Вернуться к вопросам':
                    write_kafedra(event.user_id, 'Что именно вы хотите узнать?')
                elif request == 'Какие предметы тут изучают?':
                    write_msgback_lof(event.user_id, '''
                                  Мы обучаем самым важным предметам, которые пригодятся хорошему IT-специалисту: программирование, базы данных, моделирование и проектирование информационных систем, программная инженерия и др.

Подробнее по ссылке: goo.gl/yhufQW
                                  ''')
                elif request == 'Смогу ли я стать крутым программистом?':
                    write_msgback_lof(event.user_id, '''
Конечно, сможете! Вы будете изучать программирование, как десктоп приложений, так мобильных и Web-приложений, а ещё мы можем предложить вам курсы 1С.

Подробнее по ссылке: goo.gl/yhufQW                              ''')
                
                elif request == 'Кем устраиваются выпускники?':
                    write_msgback_lof(event.user_id, '''
Наши выпускники становятся разработчиками десктопных, мобильных и Web-приложений, робототехнических систем и «умной» электроники, руководителями ИТ-проектов (CTO, IT-директор, Project Manager), системными интеграторами, системными аналитиками, инженерами по качеству ИС (QA-инженер, тестировщик ПО).

Подробнее по ссылке: goo.gl/yhufQW                              ''')
                    
                elif request == 'Где работают выпускники?':
                    write_msgback_lof(event.user_id, '''
Наши выпускники работают не только в лучших IT-компаниях региона, но и по всей России: Intel Corporation, 1С-Гэндальф, Inostudio, Oggetto web, Lodoss, Distillery, Umbrella, CBOSS, Авиаок, ОКБ Сухого, ТАНТК им. Г.М. Бериева, Ростелеком, Вымпелком, Мегафон, Т2 Мобайл (Tele2), Positive Technologies, КриптоСтандарт, НИП Информзащита, Сбербанк России, ВТБ 24, силовые структуры и ведомства (ВС РФ, ФСБ, МВД) и т.д.                              ''')
                
                elif request == 'Кого у вас готовят?':
                    write_msgback_lof(event.user_id, '''
Тут готовят IT-специалистов широкого профиля, владеющих современными практиками разработки и интеграции программно-аппаратных систем, а также умеющих применять полученные знания на практике. Наши выпускники разбираются во всех тонкостях жизненного цикла программных продуктов: от постановки задачи и проектирования систем до разработки и внедрения готовых решений. Полученные знания позволяют им управлять IT-проектами, возглавлять проектные группы, производить исследование бизнес-процессов и полную автоматизацию предприятий.

Подробнее по ссылке: goo.gl/yhufQW                              ''')
                    
                elif request == 'Test_gs':
                    bazar(event.user_id)
                else:
                    write_msg(event.user_id, 'Выберите команду')

    # Запуск бота в режиме разговора
    # for event in longpoll.listen():

    #     if event.type == VkEventType.MESSAGE_NEW:

    #         if event.to_me:
    #             request = event.text
    #             if request == 'Отключить разговоры с ботом':
    #                 write_msg(event.user_id, 'Возвращаемся...Напишите что-нибудь')
    #                 break
    #             response = chatbot.get_response(request)
    #             write_msgwbot(event.user_id, response)
    #             print(request)
    #             print(response)
