import random
import time
import re

import threading

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import INFO_STATUS
from INFO_STATUS import Infochar
import map_gg

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()


def upp_money():
    while True:
        maimes = INFO_STATUS.getter_members()
        for chel in maimes:
            INFO_STATUS.refactor_member('coins', chel.coins + chel.improve, chel.id)
        time.sleep(60)


def upload_photo(name):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(name)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


def send_messageklava(peer_id, message, klava):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        keyboard=open(klava, "r", encoding='utf-8-sig').read()
    )


def send_message(peer_id, message):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64)
    )


def send_messagept(peer_id, message, photo):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        attachment=photo
    )


def main_conept():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.from_chat:
                message = event.obj['text'].lower()
                if '[club198702757|@club198702757]' in message:
                    message = message.replace('[club198702757|@club198702757] ', '')
                    print(message)
                else:
                    message = message.replace('[club198702757|тайное общество ктбо 1-3] ', '')

                print(event.object)
                if message == '💜кто гей?💜':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 30:
                                INFO_STATUS.refactor_member('coins', chel.coins - 30, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 30 падших '
                                                            f'монет ради '
                                                            f'гейства')
                                members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)[
                                    'items']
                                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                                idm = random.randint(0, len(members_ids) - 1)
                                for sex in maimes:
                                    if sex.id == members_ids[idm]:
                                        INFO_STATUS.refactor_member('gay_lvl', sex.gay_lvl + 1, members_ids[idm])

                                send_message(event.chat_id, 'гей - @id' + str(members_ids[idm]) + '(Всеми любимый)')
                            else:
                                send_message(event.chat_id, 'Денег нету, гейство отменяется')

                if message == '🖤кто геи?🖤':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 150:
                                INFO_STATUS.refactor_member('coins', chel.coins - 150, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 150 падших '
                                                            f'монет ради '
                                                            f'ОГРОМНОГО гейства')
                                for sex in maimes:
                                    INFO_STATUS.refactor_member('gay_lvl', sex.gay_lvl + 1, sex.id)
                                    send_message(event.chat_id, 'гей - @id' + str(sex.id) + '(Всеми любимый)')
                            else:
                                send_message(event.chat_id, 'Денег нету, гейство отменяется')

                if message == '🍺заключить пивной договор!🍺':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 300:
                                INFO_STATUS.refactor_member('coins', chel.coins - 300, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 300 падших '
                                                            f'монет ради '
                                                            f'Пивного удовольствия')
                                members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)[
                                    'items']
                                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                                send_message(event.chat_id, 'Вас понял, господин...')
                                idm = random.randint(0, len(members_ids) - 1)
                                idm1 = random.randint(0, len(members_ids) - 1)
                                send_message(event.chat_id,
                                             f'Товарищ @id{members_ids[idm]}(Отдающий) пролетел аж на 60 рублей')
                                send_message(event.chat_id,
                                             f'Товарищ @id{members_ids[idm1]}(Принимающий) выиграл аж 60 рублей')
                                for sex in maimes:
                                    if sex.id == members_ids[idm]:
                                        INFO_STATUS.refactor_member('coins', sex.coins - 60, sex.id)
                                        send_message(event.chat_id,
                                                     'Договор заключен. Теперь на следующем празднике культурного '
                                                     'пития @id' + str(
                                                         members_ids[
                                                             idm]) + '(этот сильный духом муж)' + ' покупает сидр @id' + str(
                                                         members_ids[idm1]) + '(нуждающимуся) .')
                                    if sex.id == members_ids[idm1]:
                                        INFO_STATUS.refactor_member('coins', sex.coins + 60, sex.id)
                            else:
                                send_message(event.chat_id, 'Денег нету, пиво отменяется')

                elif message == '🔮узнать судьбу🔮':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            preds = open('Предсказания.txt', 'r', encoding='utf-8').readlines()
                            predsm = []
                            for line in preds:
                                predsm.append(line)
                            random_preds = random.randint(0, len(predsm))
                            send_message(event.chat_id, predsm[random_preds])
                            random_coins = random.randint(-30, 45)
                            INFO_STATUS.refactor_member('coins', chel.coins + random_coins, chel.id)
                            send_message(event.chat_id,
                                         f'Предсказание завело его в недра деньжат. @id{chel.id}({chel.name}) получает {random_coins} рубасиков')

                elif message == 'update_members':
                    members = vk.messages.getConversationMembers(peer_id=2000000001, group_id=198702757)['items']
                    members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                    for id in members_ids:
                        a = Infochar()
                        a.name = 'Безымянный'
                        a.gay_lvl = 0
                        a.coins = 0
                        a.lvl = 0
                        a.id = id

                elif message == '📘таблица мужей📘':
                    members = INFO_STATUS.getter_members()
                    state = 'Топ чаров:(Имя|Орден гейства|Падших Рублей|Уровень)\n'
                    state = state + '-----------------------------------------------------------\n'
                    i = 1
                    for member in members:
                        state = state + f'{i}. 🔸{member.name}🔸    | 🧙{member.gay_lvl}🧙  |💰{member.coins}💰    |🔮{member.lvl}🔮\n'
                        i += 1
                    send_message(event.chat_id, state)
                elif re.search(r'\bсменить имя на \b', message):
                    name = message.replace('сменить имя на ', '')
                    name = name.title()
                    id = event.obj['from_id']
                    try:
                        INFO_STATUS.refactor_member(property='name', value=name, id=id)
                        send_message(event.chat_id, f'Успешно изменено имя чела @id{id} на {name}')
                    except BaseException:
                        send_message(event.chat_id, 'Не удалось изменить имя')
                elif message == '🎭кто я?🎭':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            send_message(event.chat_id,
                                         f'🔸@id{chel.id}({chel.name})🔸 | 🧙Степень гейства🧙: {chel.gay_lvl} |  💰Падшие рубли💰: {chel.coins}')

                elif message == 'договор о земле':
                    send_message(event.chat_id, 'Ого! Господин хочет купить землю? Беллисимо, превосходно! Посмотрите '
                                                'на карту.')
                    map_gg.map_gen()
                    photo = upload_photo('temp_of_map_gen.png')

                    send_messagept(event.chat_id, 'Вот, выбери свободные участки и плати! Каждый стоит 3000 падших '
                                                  'монет!', photo)
                    points = INFO_STATUS.getter_map_for_buy()
                    info_map = ''
                    maimes = INFO_STATUS.getter_members()
                    for pk in points:
                        if pk.status == '1':
                            for chel in maimes:
                                if chel.id == pk.owner_id:
                                    info_map += f'{pk.point}, Хозяин: {chel.name}, Цвет: {pk.color}\n, Доход с точки: {pk.cost / 100}'
                    send_message(event.chat_id, 'Текущие занятые точки: \n' + info_map)


                elif re.search(r'\bкупить участок\b', message):
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.coins >= 3000:
                                point = message.replace('купить участок ', '').title()
                                print(point)
                                points = INFO_STATUS.getter_map_for_buy()
                                for pk in points:
                                    if pk.point == point:
                                        if pk.status != '1':
                                            send_message(event.chat_id,
                                                         f'Отличный выбор, договор заключен. @id{chel.id}({chel.name}) тратит {pk.cost * (chel.count_events + 1)} рубасиков на райский уголок.')
                                            INFO_STATUS.refactor_member('coins', chel.coins - (
                                                    pk.cost * (chel.count_events + 1)), chel.id)
                                            INFO_STATUS.refactor_map('status', '1', point)
                                            if chel.count_events <= 0:

                                                color = str(random.randint(1, 255)) + ',' + str(
                                                    random.randint(1, 255)) + ',' + str(random.randint(1, 255))
                                                INFO_STATUS.refactor_map('color', color, point)
                                            else:
                                                for spk in points:
                                                    if spk.owner_id == chel.id:
                                                        color = spk.color
                                                        break
                                                INFO_STATUS.refactor_map('color', color, point)
                                            INFO_STATUS.refactor_member('count_event', chel.count_events + 1, chel.id)
                                            INFO_STATUS.refactor_member('improve_money',
                                                                        ((chel.count_events + 1) * 450) / 100, chel.id)

                                            send_message(event.chat_id,
                                                         f'Теперь ваш доход составляет:{((chel.count_events + 1) * 450) / 100} (рубли/минута)')

                                            INFO_STATUS.refactor_map('Owner_id', chel.id, point)
                                            map_gg.map_gen()
                                            photo = upload_photo('temp_of_map_gen.png')
                                            send_messagept(event.chat_id, 'Карта изменена', photo)
                                        else:
                                            send_message(event.chat_id, 'Этот участок занят! Выберите другой.')
                            else:
                                send_message(event.chat_id, 'Недостаточно денег для покупки!')







                elif message == 'аоа':
                    send_messageklava(event.chat_id, 'На', r"keyboards/aoa.json")

                elif message == '💬социальный актив💬':
                    send_messageklava(event.chat_id, 'На', "keyboards/social.json")

                elif message == '👁всё о тебе👁':
                    send_messageklava(event.chat_id, 'На', "keyboards/world_and_you.json")

                elif message == 'ссылочки':
                    print('safs')
                    send_messageklava(event.chat_id, 'На', "keyboards/info.json")
                elif message == 'инфа':
                    print('safs')
                    send_messageklava(event.chat_id, 'На', "keyboards/sub_m.json")
                elif message == 'физика':
                    print('safs')
                    send_messageklava(event.chat_id, 'На', "keyboards/physics.json")

                elif message == 'кинематика':
                    send_messagept(event.chat_id, 'Держите', 'photo-198702757_457239076')
                    send_messagept(event.chat_id, 'Держите', 'photo-198702757_457239077')

                elif message == 'динамика':
                    send_messagept(event.chat_id, 'Держите', 'photo-198702757_457239078')
                    send_messagept(event.chat_id, 'Держите', 'photo-198702757_457239079')


while True:
    try:
        opa = threading.Thread(target=upp_money)
        opa.start()
        bot_session = vk_api.VkApi(
            token="448a161c4370d920f09782b8ea67453e58f64ebe60444d3a6e3c99de30c1f6214ff9e838e3f713e7ee246")
        vk = bot_session.get_api()
        longpoll = VkBotLongPoll(bot_session, 198702757)
        main_conept()
    except BaseException:
        print('reconnect')
