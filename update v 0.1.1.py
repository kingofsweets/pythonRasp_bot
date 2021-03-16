import random
import io

from bs4 import BeautifulSoup
import requests as req
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

from chatterbot.trainers import ListTrainer
import chatterbot

# Парсер расписания
import requests
from bs4 import BeautifulSoup
import urllib.request

# БОт для бедных студаков

from chatterbot import ChatBot

chatbot = ChatBot("Умный чел")
trainer = ListTrainer(chatbot)

t1 = open('anim_0.txt', 'r', encoding='utf-8').readlines()
t2 = open('anim_1.txt', 'r', encoding='utf-8').readlines()
t3 = open('Типичный японский боевик.txt', 'r', encoding='utf-8').readlines()
t4 = open('Яп_2.txt', 'r', encoding='utf-8').readlines()


# trainer.train(t1)
# trainer.train(t2)
# trainer.train(t3)
# trainer.train(t4)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("lol.json", "r", encoding="UTF-8").read()})


token = "abc758868205e672a182e6ad3bb781bcc0e4b0b63328f5af5181379f81b64e2cd610b481bf1be35481007"
vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            request = event.text

            url = 'https://ictis.alex-b.me/3.htm'
            r = requests.get(url)

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
                if i > 8 and i < 16:
                    timel.append(pars[i])

            for i in range(len(pars)):
                if i > 15 and i < 24:
                    pnd.append(pars[i])
            for i in range(len(pars)):
                if i > 23 and i < 32:
                    vt.append(pars[i])
            for i in range(len(pars)):
                if i > 31 and i < 40:
                    sred.append(pars[i])
            for i in range(len(pars)):
                if i > 39 and i < 48:
                    chetv.append(pars[i])
            for i in range(len(pars)):
                if i > 47 and i < 56:
                    pyatnica.append(pars[i])
            for i in range(len(pars)):
                if i > 55 and i < 64:
                    subbota.append(pars[i])

            if request == "/Help" or request == "/help":
                write_msg(event.user_id, ''''
                Вас приветсвует помощник в исользовании бота.
                Список команд(Регситр первой буквы не учитываеся):
                /Расписание (день недели) - узнать расписание в определённый день( день недели указывать без скобок)
                /Help - список команд
                Остальные сообщения будут рассматриваться ботом как общение, он начнёт пудрить вам мозги.
                Желаем удачи!


                ''')

            elif request == "/Расписание понедельник" or request == "/расписание понедельник":
                for i in range(len(pnd)):
                    if i == 0:
                        write_msg(event.user_id, str(pnd[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + pnd[i]))
            elif request == "/Расписание вторник" or request == "/расписание вторник":
                for i in range(len(vt)):
                    if i == 0:
                        write_msg(event.user_id, str(vt[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + vt[i]))
            elif request == "/Расписание среда" or request == "/расписание среда":
                for i in range(len(sred)):
                    if i == 0:
                        write_msg(event.user_id, str(sred[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + sred[i]))
            elif request == "/Расписание четверг" or request == "/расписание четверг":
                for i in range(len(chetv)):
                    if i == 0:
                        write_msg(event.user_id, str(chetv[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + chetv[i]))
            elif request == "/Расписание пятница" or request == "/расписание пятница":
                for i in range(len(pyatnica)):
                    if i == 0:
                        write_msg(event.user_id, str(pyatnica[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + pyatnica[i]))
            elif request == "/Расписание суббота" or request == "/расписание суббота":
                for i in range(len(subbota)):
                    if i == 0:
                        write_msg(event.user_id, str(subbota[i]))
                    else:
                        write_msg(event.user_id, str(timel[i - 1] + ': ' + subbota[i]))

            else:
                response = chatbot.get_response(request)
                write_msg(event.user_id, response)
                print(request)
                print(response)