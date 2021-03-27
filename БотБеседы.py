import random
import time
import re
import easy_logic
import enemy
import threading
import os
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
        time.sleep(60)
        maimes = INFO_STATUS.getter_members()
        for chel in maimes:
            INFO_STATUS.refactor_member('coins', chel.coins + chel.improve * chel.lvl // 10, chel.id)
            if chel.energy < easy_logic.max_energy(chel.lvl):
                INFO_STATUS.refactor_member('energy', chel.energy + 5 * (chel.lvl + 1), chel.id)


def decris_calld():
    while True:
        time.sleep(1)
        maimes = INFO_STATUS.getter_members()
        for chel in maimes:
            if chel.time_calld != 0 and chel.state != 1:
                print(chel.time_calld)
                INFO_STATUS.refactor_member('time_calld', chel.time_calld - 1, chel.id)
                if chel.time_calld - 1 == 0:
                    send_message(1, f'Кулдаун у @id{chel.id}({chel.name}) снят')
                    send_messageklava(1, 'Выберите куда пойти:', "keyboards/go_p"
                                                                 ".json")


def upload_photo(name):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(name)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


# def upload_graffity(name):
#     upload = vk_api.VkUpload(vk)
#     photo = upload.graffiti(name)
#     print(photo)


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
                print(event.obj)
                try:
                    if event.obj['action']['type'] == 'chat_invite_user':
                        send_message(event.chat_id,
                                     f"Приветствуем @id{event.obj['action']['member_id']}(Безымянного) в "
                                     f"этом "
                                     f"довольно незавысловатом мире. Пусть в приключениях его сопровождает"
                                     f" исключительно удача.")
                        a = Infochar()
                        a.id = event.obj['action']['member_id']
                        a.saver()
                        send_message(event.chat_id, 'Аккаунт приключенца создан')

                    if event.obj['action']['type'] == 'chat_kick_user':
                        send_message(event.chat_id,
                                     f"@id{event.obj['action']['member_id']}(Покидающий) был хорошим малым "
                                     f"пусть его в собственных свержениях сопровождает чистый успех.")
                        INFO_STATUS.delete_member(event.obj['action']['member_id'])
                        points = INFO_STATUS.getter_map_for_draw()
                        for point in points:
                            if point.owner_id == event.obj['action']['member_id']:
                                INFO_STATUS.delete_point(point.owner_id)
                        send_message(event.chat_id, 'Аккаунт приключенца уничтожен')
                except KeyError:
                    print('action')
                message = event.obj['text'].lower()
                if '[club198702757|@club198702757]' in message:
                    message = message.replace('[club198702757|@club198702757] ', '')
                else:
                    message = message.replace('[club198702757|тайное общество ктбо 1-3] ', '')

                if message == 'пойти на охоту':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Происходит телепортация в земли зла. Приготовьте очко.')
                                INFO_STATUS.refactor_member('pointnow', easy_logic.gen_pos(), chel.id)

                                map_gg.map_gen_for_now()
                                gen_link = upload_photo('temp_of_map_demon_gen.png')
                                send_messagept(event.chat_id, 'Вы тута: 🪐Пивная застава демонов🪐', gen_link)
                            else:
                                send_message(event.chat_id, 'Чел, ты уже тепа на карте.')

                if message == 'показать локацию':
                    map_gg.map_gen_for_now()
                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                    send_messageklava(3, 'Выберите куда пойти:', "keyboards/go_p"
                                                                 ".json")

                if message == 'вперёд':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Вы не на охоте')
                                continue
                            if chel.state == 1:
                                send_message(event.chat_id, 'Вы в бою!')
                                continue
                            if chel.time_calld == 0:
                                pos = easy_logic.up(chel.pointnow)
                                if pos != chel.pointnow:
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    INFO_STATUS.refactor_member('time_calld', 7, chel.id)
                                    send_message(event.chat_id, 'Вы остановленны на 7 секунд')
                                    easy_logic.get_chek()
                                    chel_peop = INFO_STATUS.getter_members()
                                    for sa in chel_peop:
                                        if sa.id == chel.id:
                                            if sa.state == 1:
                                                send_message(event.chat_id, 'На вас напали!')
                                                vrag = INFO_STATUS.getter_enem()
                                                for mob in vrag:
                                                    if sa.id_enem == mob.id:
                                                        enemy.draw_enem_info(mob.name, mob.hp, 0, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(3, 'Выберите действие:', "keyboards/action"
                                                                                                   ".json")


                                else:
                                    send_message(event.chat_id, 'Вверху прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == 'назад':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Вы не на охоте')
                                continue
                            if chel.state == 1:
                                send_message(event.chat_id, 'Вы в бою!')
                                continue
                            if chel.time_calld == 0:
                                pos = easy_logic.down(chel.pointnow)
                                if pos != chel.pointnow:
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    INFO_STATUS.refactor_member('time_calld', 7, chel.id)
                                    send_message(event.chat_id, 'Вы остановленны на 7 секунд')
                                    easy_logic.get_chek()
                                    chel_peop = INFO_STATUS.getter_members()
                                    for sa in chel_peop:
                                        if sa.id == chel.id:
                                            if sa.state == 1:
                                                send_message(event.chat_id, 'На вас напали!')
                                                vrag = INFO_STATUS.getter_enem()
                                                for mob in vrag:
                                                    if sa.id_enem == mob.id:
                                                        enemy.draw_enem_info(mob.name, mob.hp, 0, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(3, 'Выберите действие:', "keyboards/action"
                                                                                                   ".json")

                                else:
                                    send_message(event.chat_id, 'Внизу прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == 'вправо':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Вы не на охоте')
                                continue
                            if chel.state == 1:
                                send_message(event.chat_id, 'Вы в бою!')
                                continue
                            if chel.time_calld == 0:
                                pos = easy_logic.right(chel.pointnow)
                                if pos != chel.pointnow:
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    INFO_STATUS.refactor_member('time_calld', 7, chel.id)
                                    send_message(event.chat_id, 'Вы остановленны на 7 секунд')
                                    easy_logic.get_chek()
                                    chel_peop = INFO_STATUS.getter_members()
                                    for sa in chel_peop:
                                        if sa.id == chel.id:
                                            if sa.state == 1:
                                                send_message(event.chat_id, 'На вас напали!')
                                                vrag = INFO_STATUS.getter_enem()
                                                for mob in vrag:
                                                    if sa.id_enem == mob.id:
                                                        enemy.draw_enem_info(mob.name, mob.hp, 0, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(3, 'Выберите действие:', "keyboards/action"
                                                                                                   ".json")

                                else:
                                    send_message(event.chat_id, 'Справа прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == 'влево':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Вы не на охоте')
                                continue
                            if chel.state == 1:
                                send_message(event.chat_id, 'Вы в бою!')
                                continue
                            if chel.time_calld == 0:
                                pos = easy_logic.left(chel.pointnow)
                                if pos != chel.pointnow:
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    INFO_STATUS.refactor_member('time_calld', 7, chel.id)
                                    send_message(event.chat_id, 'Вы остановленны на 7 секунд')
                                    easy_logic.get_chek()
                                    chel_peop = INFO_STATUS.getter_members()
                                    for sa in chel_peop:
                                        if sa.id == chel.id:
                                            if sa.state == 1:
                                                send_message(event.chat_id, 'На вас напали!')
                                                vrag = INFO_STATUS.getter_enem()
                                                for mob in vrag:
                                                    if sa.id_enem == mob.id:
                                                        enemy.draw_enem_info(mob.name, mob.hp, 0, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(3, 'Выберите действие:', "keyboards/action"
                                                                                                   ".json")

                                else:
                                    send_message(event.chat_id, 'Слева прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == 'покинуть охоту':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state != 1:
                                INFO_STATUS.refactor_member('pointnow', '0', chel.id)
                                send_message(event.chat_id, 'Вы успешно покинули землю.')

                if message == 'атака':
                    maimes = INFO_STATUS.getter_members()
                    vrag = INFO_STATUS.getter_enem()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state == 1:
                                for mob in vrag:
                                    if chel.id_enem == mob.id:
                                        if mob.hp - chel.attack <= 0:
                                            INFO_STATUS.refactor_member('state', 0, chel.id)
                                            INFO_STATUS.refactor_member('id_enem', 0, chel.id)
                                            send_message(event.chat_id, 'Моб убит')
                                            INFO_STATUS.delete_enem(mob.id)
                                            os.remove(f'{mob.id}.jpg')
                                            vrag = INFO_STATUS.getter_enem()
                                            if len(vrag) <= 3:
                                                INFO_STATUS.gen_enemies()
                                        else:
                                            INFO_STATUS.refactor_enem('hp', mob.hp - chel.attack, mob.id)
                                            enemy.draw_enem_info(mob.name, mob.hp - chel.attack, 0, mob.file_m,
                                                                 mob.id)
                                            gen_link = upload_photo(mob.id + '.jpg')
                                            send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                            send_messageklava(event.chat_id, 'Выберите действие:', "keyboards/action"
                                                                                                   ".json")

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
                                members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)[
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
                                members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)[
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
                            random_coins = random.randint(-180, 45)
                            INFO_STATUS.refactor_member('coins', chel.coins + random_coins, chel.id)
                            send_message(event.chat_id, 'Идите работать!')
                            send_message(event.chat_id,
                                         f'Предсказание завело его в недра деньжат. @id{chel.id}({chel.name}) получает {random_coins} рубасиков')

                elif message == 'update_members':
                    members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)['items']
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
                            info = f"""
                            Вы - ⚒{chel.classs}⚒, а так же законный {chel.titul}. Имеете при себе {chel.count_events} участков,
                            Получая при этом 💎{chel.improve}💎 монет в минуту.
                            Ваши характеристики следующие:\n
                            Уровень @id{chel.id}({chel.name}): {chel.lvl}   |||  Опыт:🔰{chel.xp}/{easy_logic.lvl_formula(chel.lvl)}🔰
                            Энергия 💚{chel.energy}/{easy_logic.max_energy(chel.lvl)}💚 ({5 * (chel.lvl + 1)} в минуту)


                            """
                            send_message(event.chat_id, info +
                                         f'🔸@id{chel.id}({chel.name})🔸 | 🧙Степень гейства🧙: {chel.gay_lvl} |  💰Падшие рубли💰: {chel.coins}')

                elif message == 'информация о землях':
                    send_message(event.chat_id,
                                 'Ого! Господин хочет купить землю? Беллисимо, превосходно! Посмотрите '
                                 'на карту.')
                    map_gg.map_gen_forbuy()
                    photo = upload_photo('temp_of_map_gen_forbuy.png')

                    send_messagept(event.chat_id,
                                   'Вот, выбери свободные участки и плати! Цены указаны на самих землях.', photo)
                    points = INFO_STATUS.getter_map_for_draw()
                    info_map = ''
                    maimes = INFO_STATUS.getter_members()
                    for pk in points:
                        print(pk.cost)
                        if pk.status == '1':
                            for chel in maimes:
                                if chel.id == pk.owner_id:
                                    info_map += f'🗺{pk.point}🗺, Хозяин: {chel.name}, Доход с точки: {pk.cost / 1000}\n'
                    send_message(event.chat_id, 'Текущие занятые точки: \n' + info_map)


                elif re.search(r'\bкупить участок\b', message):
                    maimes = INFO_STATUS.getter_members()
                    pointsd = INFO_STATUS.getter_map_all()
                    point = message.replace('купить участок ', '').title()
                    for pk in pointsd:
                        if pk.point == point:
                            sta = pk.cost
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            send_message(event.chat_id, f'Стоимость участка: {(chel.count_events + 1) * sta} рубасецов')
                            if chel.coins >= (chel.count_events + 1) * sta:
                                for pk in pointsd:
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
                                                for spk in pointsd:
                                                    if spk.owner_id == chel.id:
                                                        color = spk.color
                                                        break
                                                INFO_STATUS.refactor_map('color', color, point)
                                            INFO_STATUS.refactor_member('count_event', chel.count_events + 1, chel.id)
                                            INFO_STATUS.refactor_member('improve_money',
                                                                        (chel.improve + (pk.cost / 1000)) * chel.lvl,
                                                                        chel.id)

                                            send_message(event.chat_id,
                                                         f'Теперь ваш доход составляет:{(chel.improve + (pk.cost / 1000))} (рубли/минута)')

                                            INFO_STATUS.refactor_map('Owner_id', chel.id, point)
                                            map_gg.map_gen()
                                            photo = upload_photo('temp_of_map_gen.png')
                                            send_messagept(event.chat_id, 'Карта изменена', photo)
                                        else:
                                            send_message(event.chat_id, 'Этот участок занят! Выберите другой.')
                            else:
                                send_message(event.chat_id, 'Недостаточно денег для покупки!')

                elif re.search(r'\bсменить профессию на\b', message):
                    name = message.replace('сменить профессию на ', '')
                    name = name.title()
                    id = event.obj['from_id']
                    if name == 'Алхимик' or name == 'Ремесленник' or name == 'Повар' or name == 'Учитель Немецкого':
                        INFO_STATUS.refactor_member(property='class', value=name, id=id)
                        send_message(event.chat_id, f'Успешно изменена профессия чела @id{id} на {name}')
                    else:
                        send_message(event.chat_id, 'Такой профессии нет! Хавтит надо мной издеваться!')

                elif message == '⚒работать⚒':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.energy - (chel.lvl + 1) * 30 > 0:
                                energy = chel.energy - (chel.lvl + 1) * 30
                                INFO_STATUS.refactor_member('energy', energy, chel.id)
                                xp = random.randint((chel.lvl + 1) * 150, (chel.lvl + 1) * 500)
                                INFO_STATUS.refactor_member('xp', chel.xp + xp, chel.id)
                                info = f"""
                                🎯Работа🎯 {chel.classs}а очень тяжела, порой она заставляет взглянуть на мир по-другому.
                                @id{chel.id}({chel.name}) работал сегодня очень усрендно и получил {xp} опыта.
                                При этом он потратил 💚{(chel.lvl + 1) * 30}💚 энергии. У него осталось только 💚{energy}💚 энерии .
                                                                                        """
                                money = random.randint((chel.lvl + 1) * 3, (chel.lvl + 1) * 100)
                                INFO_STATUS.refactor_member('coins', chel.coins + money, chel.id)
                                if money < ((chel.lvl + 1) * 3 + (chel.lvl + 1) * 25) // 2:
                                    info_2 = f'Однако начальник его не взлюбил, поэтому дал всего лишь 💰{money}💰 падших рублей.'
                                else:
                                    info_2 = f'И ему повезло, ведь начальник дал ему целых 💰{money}💰 падших рублей.'
                                info = info + info_2
                                send_message(event.chat_id, info)
                                send_message(event.chat_id,
                                             f'Уровень @id{chel.id}({chel.name}): {chel.lvl}||| Опыт: 🔰{chel.xp + xp}/{easy_logic.lvl_formula(chel.lvl)}🔰')
                                if chel.xp + xp >= easy_logic.lvl_formula(chel.lvl):
                                    send_message(event.chat_id, f'🏆Уровень повышен до {chel.lvl + 1}🏆')
                                    INFO_STATUS.refactor_member('lvl', chel.lvl + 1, chel.id)
                                    send_message(event.chat_id, f'💚Энергия полностью восстановлена💚')
                                    INFO_STATUS.refactor_member('energy', easy_logic.max_energy(chel.lvl), chel.id)
                            else:
                                send_message(event.chat_id, f'💚Недостаточно энергии💚')



                elif message == 'аоа':
                    send_messageklava(event.chat_id, 'На', r"keyboards/aoa.json")

                elif message == '💬социальный актив💬':
                    send_messageklava(event.chat_id, 'На', "keyboards/social.json")

                elif message == '👁всё о тебе👁':
                    send_messageklava(event.chat_id, 'На', "keyboards/world_and_you.json")
                elif message == '📜управление землёй📜':
                    send_messageklava(event.chat_id, 'На', "keyboards/my_earth.json")

                elif message == 'глоссарий по боту':
                    send_messageklava(event.chat_id, 'На', "keyboards/bot_info.json")

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

        opa1 = threading.Thread(target=decris_calld)
        opa1.start()
        bot_session = vk_api.VkApi(
            token="448a161c4370d920f09782b8ea67453e58f64ebe60444d3a6e3c99de30c1f6214ff9e838e3f713e7ee246")
        vk = bot_session.get_api()
        longpoll = VkBotLongPoll(bot_session, 198702757)
        main_conept()
    except BaseException:
        print('RDS')
