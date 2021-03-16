import random
import time

import requests
import vk_api
from gtts import gTTS
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()


def write_msgwbot(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64),
                                'keyboard': open("vbot.json", "r", encoding="UTF-8").read()})


def send_messageks(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open("aoa.json", "r", encoding="UTF-8").read()
    )

def send_messageksm(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open("sub_m.json", "r", encoding="UTF-8").read()
    )
def send_messagekph(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open("physics.json", "r", encoding="UTF-8").read()
    )



def send_messageksinfo(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open("info.json", "r", encoding="UTF-8").read()
    )


def send_message(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64)
    )


def send_messagept(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        attachment='photo-198883617_457239019'
    )


def send_messageat(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        attachment='audio246767805_456239312'
    )


def bazar(text, ida):
    if len(text.split()) <= 500:
        tts = gTTS(text=text, lang='ru')
        name = "say.mp3"
        tts.save(name)
        upload_url = vk.method('docs.getUploadServer', {"type": "audio_message", "peer_id": id, "v": "5.90"})
        # b = requests.post(a['upload_url'], files={'file': open(name, 'rb')}).json()
        # c = vk.method("docs.save", {"file": b["file"]})[0]
        # d = 'doc{}_{}'.format(c['owner_id'], c['id'])
        # vk.method('messages.send', {'peer_id': id, 'attachment': d, "random_id": random.randint(1, 2147483647)})


bot_session = vk_api.VkApi(
    token="448a161c4370d920f09782b8ea67453e58f64ebe60444d3a6e3c99de30c1f6214ff9e838e3f713e7ee246")
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 198702757)
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.from_chat:
            message = event.obj['text'].lower()
            if '[club198702757|@club198702757]' in message:
                message = message.replace('[club198702757|@club198702757] ', '')
                print(message)
            zapros = message.replace('[club198702757|тайное общество ктбо 1-3] ', '')
            #                print(message)
            print(event.object)
            if message == 'купить волгу':
                send_messagept(event.chat_id, 'Держите')
            if message == '/помощь':
                send_message(event.chat_id, '''
                Вас приветствует Первый Помощник!
                Основные команды:
                '/Помощь' - список всех команд
                "Кто гей?" - узнать кто гей
                "Кто геи" - узнать кто геи
                "Заключить пивной договор!" - пакт о передаче алкоголя
                "Узнать судьбу"



                ''')
            if message == 'тест гс':
                bazar('Пососи бибу', event.chat_id)
            if message == 'кто гей?':
                members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)['items']
                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                idm = random.randint(0, 12)
                send_message(event.chat_id, 'гей - @id' + str(members_ids[idm]) + '(Всеми любимый)')
            elif message == 'кто геи?':
                members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)['items']
                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                send_message(event.chat_id, 'Вот они мои родные слева на право:')
                for ids in range(len(members_ids)):
                    send_message(event.chat_id, 'гей - @id' + str(members_ids[ids]) + '(Всеми любимый)')
            elif message == 'заключить пивной договор!':
                members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)['items']
                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                send_message(event.chat_id, 'Вас понял, господин...')
                idm = random.randint(0, 7)
                idm1 = random.randint(0, 7)
                send_message(event.chat_id,
                             'Договор заключен. Теперь на следующем празднике культурного пития @id' + str(
                                 members_ids[idm]) + '(этот сильный духом муж)' + ' покупает сидр @id' + str(
                                 members_ids[idm1]) + '(нуждающимуся) .')
            elif message == 'узнать судьбу':
                preds = open('Предсказания.txt', 'r', encoding='utf-8').readlines()
                predsm = []
                for line in preds:
                    predsm.append(line)
                random_preds = random.randint(0, 17)
                send_message(event.chat_id, predsm[random_preds])

            elif message == 'аоа':
                send_messageks(event.chat_id, 'На')

            elif message == 'ссылочки':
                print('safs')
                send_messageksinfo(event.chat_id, 'На')
            elif message == 'инфа':
                print('safs')
                send_messageksm(event.chat_id, 'На')
            elif message == 'физика':
                print('safs')
                send_messagekph(event.chat_id, 'На')
            elif message == 'кинематика':
                vk.messages.send(
                    chat_id=event.chat_id,
                    message='кинематика',
                    random_id=random.getrandbits(64),
                    attachment='photo-198702757_457239076'
                )
                vk.messages.send(
                    chat_id=event.chat_id,
                    message='eee',
                    random_id=random.getrandbits(64),
                    attachment='photo-198702757_457239077'
                )
            elif message == 'динамика':
                vk.messages.send(
                    chat_id=event.chat_id,
                    message='динамика',
                    random_id=random.getrandbits(64),
                    attachment='photo-198702757_457239078'
                )
                vk.messages.send(
                    chat_id=event.chat_id,
                    message='eee',
                    random_id=random.getrandbits(64),
                    attachment='photo-198702757_457239079'
                )
