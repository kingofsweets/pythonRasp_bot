import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def send_message(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
    )


bot_session = vk_api.VkApi(
    token="899e11e7dfeb9b999f40c7929da6da3044edfac3729c287fcf80ee9e572f53d8fec3625510dd86e1a9b37")
vk = bot_session.get_api()

while True:
    longpoll = VkBotLongPoll(bot_session, 198883617)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.from_chat:

                message = event.obj['text'].lower()
                zapros = message.replace('[club198702757|тайное общество ктбо 1-3]','')
                #                print(message)
                #                print(event.object)
                if message == '/Помощь':
                    send_message(event.chat_id,'''
                    Вас приветствует Первый Помощник!
                    Основные команды:
                    '/Помощь' - список всех команд
                    "Кто гей?" - узнать кто гей
                    "Кто геи" - узнать кто геи
                    "Заключить пивной договор!" - пакт о передаче алкоголя
                    "Узнать судьбу"
                    
                    
                    
                    ''')
                if message == 'кто гей?':
                    members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198883617)['items']
                    members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                    idm = random.randint(0, 8)
                    send_message(event.chat_id, 'гей - @id' + str(members_ids[idm]) + '(Всеми любимый)')
                elif message == 'кто геи?':
                    members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198883617)['items']
                    members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                    send_message(event.chat_id, 'Вот они мои родные слева на право:')
                    for ids in range(len(members_ids)):
                        send_message(event.chat_id, 'гей - @id' + str(members_ids[ids]) + '(Всеми любимый)')
                elif message == 'заключить пивной договор!':
                    members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198883617)['items']
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