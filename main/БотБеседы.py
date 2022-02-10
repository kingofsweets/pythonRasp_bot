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
import inventory
import requests
from bs4 import BeautifulSoup

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()


def pars_it_news():
    site = 'https://habr.com/ru/news/'
    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.select('.post__title_link')
    numas = []
    hrefs = []
    for tr in table:
        numas.append(
            tr.get_text() + '\nСсылка на статью: ')
        hrefs.append(tr['href'])
    return numas, hrefs


def upp_money():
    while True:
        time.sleep(60)
        maimes = INFO_STATUS.getter_members()
        for chel in maimes:
            INFO_STATUS.refactor_member('coins', chel.coins + chel.improve, chel.id)
            if chel.energy + 5 * (chel.lvl + 1) <= easy_logic.max_energy(
                    chel.lvl) and chel.state != 1:
                INFO_STATUS.refactor_member('energy', chel.energy + 5 * (chel.lvl + 1), chel.id)
            elif easy_logic.max_energy(chel.lvl) - chel.energy < chel.energy + 5 * (
                    chel.lvl + 1) and chel.state != 1:
                INFO_STATUS.refactor_member('energy', easy_logic.max_energy(chel.lvl), chel.id)

            if chel.hp + 3 * (chel.lvl + 1) <= easy_logic.max_hp(
                    chel.lvl) and chel.state != 1 and chel.pointnow == '0':
                INFO_STATUS.refactor_member('hp', chel.hp + 3 * (chel.lvl + 1), chel.id)

            elif easy_logic.max_hp(chel.lvl) - chel.hp < chel.hp + 5 * (
                    chel.lvl + 1) and chel.state != 1 and chel.pointnow == '0':
                INFO_STATUS.refactor_member('hp', easy_logic.max_hp(chel.lvl), chel.id)


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
            if chel.piv_calld != 0:
                INFO_STATUS.refactor_member('piv_calld', chel.piv_calld - 1, chel.id)
                if chel.piv_calld - 1 == 0:
                    send_message(1, 'Эффект от пива прошел')
                    INFO_STATUS.refactor_member('attack', chel.attack // 2, chel.id)
                    INFO_STATUS.refactor_member('defence', chel.defence // 2, chel.id)


def upload_photo(name):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(name)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


def up_lvl(chat_id, chel_xp, xp, chel_lvl, chel_id):
    if chel_xp + xp >= easy_logic.lvl_formula(chel_lvl):
        while chel_xp + xp >= easy_logic.lvl_formula(chel_lvl):
            chel_lvl += 1
        send_message(chat_id, f'🏆Уровень повышен до {chel_lvl}🏆')
        INFO_STATUS.refactor_member('lvl', chel_lvl, chel_id)
        send_message(chat_id, f'💚Энергия и здоровье полностью восстановлены💚')
        INFO_STATUS.refactor_member('energy', easy_logic.max_energy(chel_lvl), chel_id)
        INFO_STATUS.refactor_member('hp', easy_logic.max_hp(chel_lvl), chel_id)

        if 10 <= chel_lvl < 20:
            send_message(chat_id, 'Теперь вы Барон')
            INFO_STATUS.refactor_member('titul', 'Барон', chel_id)
        if 20 <= chel_lvl < 30:
            send_message(chat_id, 'Теперь вы Граф')
            INFO_STATUS.refactor_member('titul', 'Граф', chel_id)
        if 30 <= chel_lvl < 40:
            send_message(chat_id, 'Теперь вы Герцог')
            INFO_STATUS.refactor_member('titul', 'Герцог', chel_id)
        if 40 <= chel_lvl < 50:
            send_message(chat_id, 'Теперь вы Советник')
            INFO_STATUS.refactor_member('titul', 'Советник', chel_id)


def adventure(chat, ident, name, lvl, coins, xp, energ_p, energo):
    send_message(chat, '🏕Путешествие по землям демонов никогда не было простым делом.🏕')
    lut1 = random.randint(1, (lvl + 1) * 15)
    lut2 = random.randint(1, (lvl + 1) * 45)
    INFO_STATUS.refactor_member('coins', coins + lut1, ident)
    INFO_STATUS.refactor_member('xp', xp + lut2, ident)
    INFO_STATUS.refactor_member('energy', energ_p - energo, ident)
    send_message(chat,
                 f"""@id{ident}({name}) наткнулся на 💰{lut1}💰 монет. Эта вылазка научила его чему-то, поэтмому он получил 🔰{lut2}🔰 опыта. После длинного пути он потратил 💚{energo}💚 энергии. 
Ему стоит отдохнуть. Ваши патаметры:
Энергия: 💚{energ_p - energo}/{easy_logic.max_energy(lvl)}💚
Опыт: 🔰{xp + lut2}/{easy_logic.lvl_formula(lvl)}🔰
Падшие монеты: 💰{coins + lut1}💰
                    
                """)
    up_lvl(chat, xp, lut2, lvl, ident)


def chancekl(hillk, res, lvl, ida, chat):
    chance = random.randint(0, 1)
    chance2 = random.randint(0, 100)

    if chance == 1:
        send_message(chat, 'Каким-то чудом вы смогли получить немного ресурсов')
        lut1 = random.randint(1, (lvl + 1) * 5)
        send_message(chat, f'♻Получено {lut1} ресурсов.♻')
        INFO_STATUS.refactor_member('res_count', res + lut1, ida)

    if chance2 == 100:
        send_message(chat, '💚Вам несказанно повезло! В одном из ящиков оказался потрепанный, но всё ещё действенный '
                           'элексир восстановления энергии.💚')
        INFO_STATUS.refactor_member('ener_count', hillk + 1, ida)


def otvetka(chat_id, cdid, enemy_id, block):
    chels = INFO_STATUS.getter_members()
    for chel in chels:
        if chel.id == cdid:
            coins_p = chel.coins
            hp_chel = chel.hp
            xp_p = chel.xp
            lvl_p = chel.lvl

    enemys = INFO_STATUS.getter_enem()
    for chel in enemys:
        if chel.id == enemy_id:
            enemy_attack = chel.attack
            lvl_e = chel.lvl
    enemy_attack = random.randint((lvl_e + 1) * enemy_attack, (lvl_e + 2) * enemy_attack)
    send_message(chat_id, 'Противник атакует! Приготовтьесь!')
    choise = random.randint(1, 4)
    if choise == 1:
        attack = int(enemy_attack * (random.randint(1, 25) / 100))
        send_message(chat_id, f'🗡Вам повезло. Проивник наносит всего лишь {attack} урона.🗡')
    elif choise == 2:
        attack = int(enemy_attack * (random.randint(26, 50) / 100))
        send_message(chat_id, f'🗡Не так уж и больно. Проивник наносит {attack} урона.🗡')
    elif choise == 3:
        attack = int(enemy_attack * (random.randint(51, 75) / 100))
        send_message(chat_id, f'🗡Опасно. Проивник наносит {attack} урона.🗡')
    elif choise == 4:
        attack = int(enemy_attack * (random.randint(76, 100) / 100))
        send_message(chat_id, f'🗡Страшно. Проивник использует весь свой потенциал и наносит {attack} урона.🗡')
    if block != 0:
        if block >= attack:
            send_message(chat_id, f'🛡Урон польностью поглощен!🛡')
            attack = 0
        else:
            send_message(chat_id, f'🛡Вы поглотили {block}!🛡')
            attack = attack - block

    if hp_chel - attack > 0:
        send_message(chat_id, f'Ваше здоровье: ❤{hp_chel - attack}/{easy_logic.max_hp(lvl_p)}❤')
        INFO_STATUS.refactor_member('hp', hp_chel - attack, cdid)
        return 1
    else:
        send_message(chat_id, f'Вы погибли. Ваше здоровье:❤ 0/{easy_logic.max_hp(lvl_p)}❤')
        send_message(chat_id, f'Вы получате дебаф.')
        coins = random.randint(int(coins_p * 0.01), int(coins_p * 0.25))
        xp = random.randint(int(xp_p * 0.01), int(xp_p * 0.25))
        send_message(chat_id, f'💰Вы получате дебаф. Монеты: -{coins}💰')
        send_message(chat_id, f'🔰Вы получате дебаф. Опыт: -{xp}🔰')
        INFO_STATUS.refactor_member('coins', coins_p - coins, cdid)
        INFO_STATUS.refactor_member('xp', xp_p - xp, cdid)
        INFO_STATUS.refactor_member('hp', easy_logic.max_hp(lvl_p), cdid)
        INFO_STATUS.refactor_member('energy', easy_logic.max_energy(lvl_p), cdid)
        INFO_STATUS.refactor_member('state', 0, cdid)
        INFO_STATUS.refactor_member('pointnow', '0', cdid)
        INFO_STATUS.refactor_member('id_enem', '0', cdid)
        INFO_STATUS.refactor_enem('hp', easy_logic.max_hp(lvl_e), enemy_id)
        INFO_STATUS.refactor_enem('state', 0, enemy_id)
        INFO_STATUS.refactor_member('time_calld', 300, cdid)

        return 0


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


def send_messagemusic(peer_id, message, music):
    vk.messages.send(
        chat_id=peer_id,
        message=message,
        random_id=random.getrandbits(64),
        attachment=music
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
                nomens = INFO_STATUS.getter_members()
                flg_p = 0
                for chelsa in nomens:
                    if chelsa.id == event.obj['from_id']:
                        flg_p = 1
                if flg_p == 0:
                    send_message(event.chat_id, 'У вас не было аккаунта')
                    a = Infochar()
                    a.id = event.obj['from_id']
                    a.saver()
                message = event.obj['text'].lower()
                if '[club198702757|@club198702757]' in message:
                    message = message.replace('[club198702757|@club198702757] ', '')
                else:
                    message = message.replace('[club198702757|тайное общество ктбо 1-3] ', '')

                if message == '⚔пойти на охоту⚔':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.time_calld != 0:
                                send_message(event.chat_id,
                                             f'Вы не можете войти в локацию ещё {chel.time_calld} секунд')
                                continue
                            if chel.pointnow == '0':
                                send_message(event.chat_id, 'Происходит телепортация в земли зла. Приготовьте очко.')
                                INFO_STATUS.refactor_member('pointnow', easy_logic.gen_pos(), chel.id)

                                map_gg.map_gen_for_now()
                                gen_link = upload_photo('temp_of_map_demon_gen.png')
                                send_messagept(event.chat_id, 'Вы тута: 🪐Пивная застава демонов🪐', gen_link)
                                send_messageklava(event.chat_id, 'Выберите куда пойти:', "keyboards/go_p"
                                                                                         ".json")
                            else:
                                send_message(event.chat_id, 'Вы уже на карте.')
                                send_messageklava(event.chat_id, 'Выберите куда пойти:', "keyboards/go_p"
                                                                                         ".json")

                if message == '🗺показать локацию🗺':
                    map_gg.map_gen_for_now()
                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)

                if message == '⬆вперёд⬆':
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
                                    pan = easy_logic.rand_energy(chel.lvl)
                                    if chel.energy - pan <= 0:
                                        INFO_STATUS.refactor_member('time_calld', 30, chel.id)
                                        send_message(event.chat_id, 'Недостаточно энергии')
                                        send_message(event.chat_id, 'Вы остановленны на 30 секунд')
                                        continue
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    pan = easy_logic.rand_energy(chel.lvl)

                                    adventure(event.chat_id, chel.id, chel.name, chel.lvl, chel.coins, chel.xp,
                                              chel.energy, pan)
                                    chancekl(chel.en_c, chel.r_c, chel.lvl, chel.id, event.chat_id)
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
                                                        enemy.draw_enem_info(mob.name, mob.hp, mob.lvl, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(event.chat_id, 'Выберите действие:',
                                                                          "keyboards/action"
                                                                          ".json")


                                else:
                                    send_message(event.chat_id, 'Вверху прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == '⬇назад⬇':
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
                                    pan = easy_logic.rand_energy(chel.lvl)
                                    if chel.energy - pan <= 0:
                                        INFO_STATUS.refactor_member('time_calld', 30, chel.id)
                                        send_message(event.chat_id, 'Недостаточно энергии')
                                        send_message(event.chat_id, 'Вы остановленны на 30 секунд')
                                        continue
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                    pan = easy_logic.rand_energy(chel.lvl)

                                    adventure(event.chat_id, chel.id, chel.name, chel.lvl, chel.coins, chel.xp,
                                              chel.energy, pan)
                                    chancekl(chel.en_c, chel.r_c, chel.lvl, chel.id, event.chat_id)
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
                                                        enemy.draw_enem_info(mob.name, mob.hp, mob.lvl, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(event.chat_id, 'Выберите действие:',
                                                                          "keyboards/action"
                                                                          ".json")

                                else:
                                    send_message(event.chat_id, 'Внизу прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == '➡вправо➡':
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
                                    pan = easy_logic.rand_energy(chel.lvl)
                                    if chel.energy - pan <= 0:
                                        INFO_STATUS.refactor_member('time_calld', 30, chel.id)
                                        send_message(event.chat_id, 'Недостаточно энергии')
                                        send_message(event.chat_id, 'Вы остановленны на 30 секунд')
                                        continue
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)

                                    adventure(event.chat_id, chel.id, chel.name, chel.lvl, chel.coins, chel.xp,
                                              chel.energy, pan)
                                    chancekl(chel.en_c, chel.r_c, chel.lvl, chel.id, event.chat_id)
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
                                                        enemy.draw_enem_info(mob.name, mob.hp, mob.lvl, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(event.chat_id, 'Выберите действие:',
                                                                          "keyboards/action"
                                                                          ".json")

                                else:
                                    send_message(event.chat_id, 'Справа прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == '⬅влево⬅':
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
                                    pan = easy_logic.rand_energy(chel.lvl)
                                    if chel.energy - pan <= 0:
                                        INFO_STATUS.refactor_member('time_calld', 30, chel.id)
                                        send_message(event.chat_id, 'Недостаточно энергии')
                                        send_message(event.chat_id, 'Вы остановленны на 30 секунд')
                                        continue
                                    INFO_STATUS.refactor_member('pointnow', pos, chel.id)
                                    enemies = INFO_STATUS.getter_enem_for_gen()
                                    for mob in enemies:
                                        mob.random_go()
                                    map_gg.map_gen_for_now()
                                    gen_link = upload_photo('temp_of_map_demon_gen.png')
                                    send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)

                                    adventure(event.chat_id, chel.id, chel.name, chel.lvl, chel.coins, chel.xp,
                                              chel.energy, pan)
                                    chancekl(chel.en_c, chel.r_c, chel.lvl, chel.id, event.chat_id)
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
                                                        enemy.draw_enem_info(mob.name, mob.hp, mob.lvl, mob.file_m,
                                                                             mob.id)
                                                        gen_link = upload_photo(mob.id + '.jpg')
                                                        send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                        send_messageklava(event.chat_id, 'Выберите действие:',
                                                                          "keyboards/action"
                                                                          ".json")

                                else:
                                    send_message(event.chat_id, 'Слева прохода нету.')
                            else:
                                send_message(event.chat_id, f'Вы не можете ходить ещё {chel.time_calld} секунд')

                if message == '🦶покинуть охоту🦶':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state != 1:
                                INFO_STATUS.refactor_member('pointnow', '0', chel.id)
                                send_message(event.chat_id, 'Вы успешно покинули землю.')

                if message == '🗡атака🗡':
                    maimes = INFO_STATUS.getter_members()
                    vrag = INFO_STATUS.getter_enem()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state == 1:
                                for mob in vrag:
                                    if chel.id_enem == mob.id:
                                        attack = int(easy_logic.rand_attack(chel.attack, chel.lvl, chel.energy))
                                        if mob.hp - attack <= 0:
                                            INFO_STATUS.refactor_member('state', 0, chel.id)
                                            INFO_STATUS.refactor_member('id_enem', 0, chel.id)
                                            send_message(event.chat_id, 'Моб убит')
                                            xp = random.randint((mob.lvl + 1) * 80, (mob.lvl + 2) * 300)
                                            res = random.randint((mob.lvl + 0) * 15, (mob.lvl + 1) * 30)
                                            coins = random.randint((mob.lvl + 1) * 60, (mob.lvl + 2) * 100)
                                            send_message(event.chat_id,
                                                         f'Вы получаете 🔰{xp}🔰 опыта, ♻{res}♻ ресурсов,💰 {coins}💰 монет')
                                            INFO_STATUS.refactor_member('res_count', chel.r_c + res, chel.id)
                                            INFO_STATUS.refactor_member('xp', chel.xp + xp, chel.id)
                                            INFO_STATUS.refactor_member('coins', chel.coins + coins, chel.id)
                                            rands = random.randint(0, 20)
                                            if 10 > rands >= 0:
                                                send_message(event.chat_id,
                                                             f'❤Ура, вы получаете зелье восстановления здоровья❤')
                                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                            if 20 > rands >= 11:
                                                send_message(event.chat_id,
                                                             f'💚Ура, вы получаете зелье восстановления энергии💚')
                                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                            if rands == 20:
                                                send_message(event.chat_id,
                                                             f'🍺Ура, вы получаете пиво🍺')
                                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)

                                            up_lvl(event.chat_id, chel.xp, xp, chel.lvl, chel.id)
                                            INFO_STATUS.delete_enem(mob.id)
                                            os.remove(f'{mob.id}.jpg')
                                            vrag = INFO_STATUS.getter_enem()
                                            if len(vrag) <= 3:
                                                INFO_STATUS.gen_enemies()
                                            map_gg.map_gen_for_now()
                                            gen_link = upload_photo('temp_of_map_demon_gen.png')
                                            send_messagept(event.chat_id, '🪐Пивная застава демонов🪐', gen_link)
                                        else:
                                            energy = easy_logic.rand_energy(chel.lvl)
                                            if chel.energy - energy >= 0:
                                                send_message(event.chat_id,
                                                             f'🗡@id{chel.id}({chel.name}) наносит {attack} урона🗡')
                                                send_message(event.chat_id,
                                                             f'💚У вас осталось {chel.energy - energy}/{easy_logic.max_energy(chel.lvl)} энергии💚')
                                                INFO_STATUS.refactor_member('energy', chel.energy - energy, chel.id)
                                                INFO_STATUS.refactor_enem('hp', mob.hp - attack, mob.id)
                                                enemy.draw_enem_info(mob.name, mob.hp - attack, mob.lvl, mob.file_m,
                                                                     mob.id)
                                                a = otvetka(event.chat_id, chel.id, mob.id, 0)
                                                if a == 1:
                                                    gen_link = upload_photo(mob.id + '.jpg')
                                                    send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                    send_messageklava(event.chat_id, 'Выберите действие:',
                                                                      "keyboards/action"
                                                                      ".json")
                                            else:
                                                send_message(event.chat_id, '💚У вас не хватает энергии на этот удар! Вы '
                                                                            'пропустили ход!💚')
                                                a = otvetka(event.chat_id, chel.id, mob.id, 0)
                                                if a == 1:
                                                    gen_link = upload_photo(mob.id + '.jpg')
                                                    send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                    send_messageklava(event.chat_id, 'Выберите действие:',
                                                                      "keyboards/action"
                                                                      ".json")
                if message == '🦶сбежать🦶':
                    maimes = INFO_STATUS.getter_members()
                    vrag = INFO_STATUS.getter_enem()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state == 1:
                                for mob in vrag:
                                    if chel.id_enem == mob.id:
                                        chance = random.randint(0, 1)
                                        if chance == 1:
                                            send_message(event.chat_id,
                                                         f'Вы успешно сбежали.')
                                            coins = random.randint(int(chel.coins * 0.01), int(chel.coins * 0.05))
                                            send_message(event.chat_id, f'Вы получате дебаф. Монеты: -{coins}')
                                            INFO_STATUS.refactor_member('coins', chel.coins - coins, chel.id)
                                            INFO_STATUS.refactor_member('state', 0, chel.id)
                                            INFO_STATUS.refactor_member('pointnow', '0', chel.id)
                                            INFO_STATUS.refactor_member('id_enem', '0', chel.id)
                                            INFO_STATUS.refactor_enem('hp', easy_logic.max_hp(mob.lvl), mob.id)
                                            INFO_STATUS.refactor_enem('state', 0, mob.id)
                                            INFO_STATUS.refactor_member('time_calld', 150, chel.id)

                                        else:
                                            send_message(event.chat_id, 'У вас не вышло сбежать! Вы '
                                                                        'пропустили ход!')
                                            a = otvetka(event.chat_id, chel.id, mob.id, 0)
                                            if a == 1:
                                                gen_link = upload_photo(mob.id + '.jpg')
                                                send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                                send_messageklava(event.chat_id, 'Выберите действие:',
                                                                  "keyboards/action"
                                                                  ".json")
                if message == '🛡блок🛡':
                    maimes = INFO_STATUS.getter_members()
                    vrag = INFO_STATUS.getter_enem()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.state == 1:
                                for mob in vrag:
                                    if chel.id_enem == mob.id:
                                        send_message(event.chat_id, f'Вы принимаете часть урона на себя, стараясь '
                                                                    f'восстановить силы')
                                        if chel.lvl < mob.lvl:
                                            print('ssds')
                                            defen = int(easy_logic.rand_defffe(chel.defence, chel.lvl, chel.energy))
                                        else:
                                            defen = int(easy_logic.rand_defffe(chel.defence, mob.lvl,
                                                                               easy_logic.max_energy(mob.lvl)))
                                        energy = easy_logic.rand_energy(chel.lvl)
                                        send_message(event.chat_id,
                                                     f'🛡@id{chel.id}({chel.name}) способен принять {defen} урона.🛡')
                                        if chel.energy + energy > easy_logic.max_energy(chel.lvl):
                                            energy = easy_logic.max_energy(chel.lvl)
                                        else:
                                            energy = chel.energy + energy
                                        send_message(event.chat_id,
                                                     f'💚Внезапно вы смогли восстановить {energy}/{easy_logic.max_energy(chel.lvl)} энергии💚')
                                        INFO_STATUS.refactor_member('energy', energy, chel.id)
                                        enemy.draw_enem_info(mob.name, mob.hp, mob.lvl, mob.file_m,
                                                             mob.id)
                                        a = otvetka(event.chat_id, chel.id, mob.id, defen)
                                        if a == 1:
                                            gen_link = upload_photo(mob.id + '.jpg')
                                            send_messagept(event.chat_id, f'{mob.name}', gen_link)
                                            send_messageklava(event.chat_id, 'Выберите действие:',
                                                              "keyboards/action"
                                                              ".json")
                if message == '💼инвентарь💼':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            inventory.draw_inventory(chel.h_c, chel.en_c, chel.b_c, chel.r_c, chel.ex_c, chel.id)
                            upload = upload_photo(f'{chel.id}_i.png')
                            send_messagept(event.chat_id, 'Ваш инвентарь', upload)
                            send_messageklava(event.chat_id, 'Выберите действие:',
                                              "keyboards/inventory"
                                              ".json")

                if message == '❤использовать зелье❤':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.h_c > 0:
                                send_message(event.chat_id, 'Вы использовали зелье восстановления здоровья!')
                                INFO_STATUS.refactor_member('hill_count', chel.h_c - 1, chel.id)
                                send_message(event.chat_id, 'Здоровье польностью восстановлено!')
                                INFO_STATUS.refactor_member('hp', easy_logic.max_hp(chel.lvl), chel.id)
                            else:
                                send_message(event.chat_id, 'У вас нету этого зелья')

                if message == '💚использовать зелье💚':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.en_c > 0:
                                send_message(event.chat_id, 'Вы использовали зелье восстановления здоровья!')
                                INFO_STATUS.refactor_member('ener_count', chel.en_c - 1, chel.id)
                                send_message(event.chat_id, 'Энергия польностью восстановлено!')
                                INFO_STATUS.refactor_member('energy', easy_logic.max_energy(chel.lvl), chel.id)
                            else:
                                send_message(event.chat_id, 'У вас нету этого зелья')

                if message == '🍺использовать пиво🍺':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.b_c > 0 and chel.piv_calld == 0:
                                send_message(event.chat_id, 'Вы использовали благославление бога пива!')
                                INFO_STATUS.refactor_member('beer_count', chel.b_c - 1, chel.id)
                                send_message(event.chat_id, 'На 2 минуты удвоены урон и защита')
                                INFO_STATUS.refactor_member('attack', chel.attack * 2, chel.id)
                                INFO_STATUS.refactor_member('defence', chel.defence * 2, chel.id)
                                INFO_STATUS.refactor_member('piv_calld', 120, chel.id)
                            else:
                                send_message(event.chat_id, 'У вас нету пива или вы уже его использовали')

                if message == '✨использовать зелье✨':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.ex_c > 0:
                                send_message(event.chat_id, 'Вы использовали зелье опыта!')
                                INFO_STATUS.refactor_member('exp_count', chel.ex_c - 1, chel.id)
                                send_message(event.chat_id, 'Уровень увеличен на 1')
                                INFO_STATUS.refactor_member('lvl', chel.lvl + 1, chel.id)
                                INFO_STATUS.refactor_member('xp', easy_logic.lvl_formula(chel.lvl), chel.id)
                            else:
                                send_message(event.chat_id, 'У вас нету этого зелья')

                if message == '💚купить зелье💚':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.coins >= 400:
                                send_message(event.chat_id, '💚Вы купили зелье восстановления энергии!💚')
                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                INFO_STATUS.refactor_member('coins', chel.coins - 400, chel.id)
                            else:
                                send_message(event.chat_id, 'У вас недостаточно монет')

                if message == '✨купить зелье✨':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.coins >= 50000:
                                send_message(event.chat_id, '✨Вы купили зелье опыта!✨')
                                INFO_STATUS.refactor_member('exp_count', chel.en_c + 1, chel.id)
                                INFO_STATUS.refactor_member('coins', chel.coins - 50000, chel.id)
                            else:
                                send_message(event.chat_id, 'У вас недостаточно монет')

                if message == '🍺купить пиво🍺':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.coins >= 1000:
                                send_message(event.chat_id, '🍺Вы купили пиво!🍺')
                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                INFO_STATUS.refactor_member('coins', chel.coins - 1000, chel.id)
                            else:
                                send_message(event.chat_id, 'У вас недостаточно монет')

                if message == '❤купить зелье❤':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.coins >= 500:
                                send_message(event.chat_id, '❤Вы купили зелье восстановления здоровья!❤')
                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                INFO_STATUS.refactor_member('coins', chel.coins - 500, chel.id)
                            else:
                                send_message(event.chat_id, 'У вас недостаточно монет')

                if message == '💜кто гей?💜':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 100:
                                INFO_STATUS.refactor_member('coins', chel.coins - 100, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 100 падших '
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
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 700:
                                INFO_STATUS.refactor_member('coins', chel.coins - 700, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 700 падших '
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
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            owner = chel
                            print(owner.name)
                            if chel.coins >= 1500:
                                INFO_STATUS.refactor_member('coins', chel.coins - 1500, event.obj['from_id'])
                                send_message(event.chat_id, f'@id{owner.id}({owner.name}) потратился аж на 1500 падших '
                                                            f'монет ради '
                                                            f'Пивного удовольствия')
                                members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)[
                                    'items']
                                members_ids = [member['member_id'] for member in members if member['member_id'] > 0]
                                send_message(event.chat_id, 'Вас понял, господин...')
                                idm = random.randint(0, len(members_ids) - 1)
                                idm1 = random.randint(0, len(members_ids) - 1)
                                send_message(event.chat_id,
                                             f'Товарищ @id{members_ids[idm]}(Отдающий) пролетел аж на 300 рублей')
                                send_message(event.chat_id,
                                             f'Товарищ @id{members_ids[idm1]}(Принимающий) выиграл аж 300 рублей')
                                for sex in maimes:
                                    if sex.id == members_ids[idm]:
                                        INFO_STATUS.refactor_member('coins', sex.coins - 300, sex.id)
                                        send_message(event.chat_id,
                                                     'Договор заключен. Теперь на следующем празднике культурного '
                                                     'пития @id' + str(
                                                         members_ids[
                                                             idm]) + '(этот сильный духом муж)' + ' покупает сидр @id' + str(
                                                         members_ids[idm1]) + '(нуждающимуся) .')
                                    if sex.id == members_ids[idm1]:
                                        INFO_STATUS.refactor_member('coins', sex.coins + 300, sex.id)
                            else:
                                send_message(event.chat_id, 'Денег нету, пиво отменяется')

                elif message == '🔮узнать судьбу🔮':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
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
                    state = 'Топ чаров:(Имя|Уровень|Падших Рублей|Уровень)\n'
                    state = state + '-----------------------------------------------------------\n'
                    i = 1
                    for member in members:
                        state = state + f'{i}. 🔸{member.name}🔸    | 🧙{member.lvl}🧙  |💰{member.coins}💰    |🔮{member.lvl}🔮\n'
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
                            Здоровье ❤{chel.hp}/{easy_logic.max_hp(chel.lvl)}❤ ({3 * (chel.lvl + 1)} в минуту)
                            🗡Атака: {chel.attack * (chel.lvl + 1)}-{chel.attack * (chel.lvl + 2)}🗡, 🛡Защита: {chel.defence * (chel.lvl + 0)}-{chel.defence * (chel.lvl + 1)}🛡


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
                                    info_map += f'🗺{pk.point}🗺, Хозяин: {chel.name}, Уровень: {pk.lvl}, Доход с точки: {(pk.cost / 100) * (pk.lvl + 1)}\n'
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
                            if chel.lvl < (chel.count_events + 1) * 10:
                                send_message(event.chat_id, f'Необходим уровень: {(chel.count_events + 1) * 10}')
                                continue
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
                                                                        (chel.improve + (pk.cost / 100)),
                                                                        chel.id)

                                            send_message(event.chat_id,
                                                         f'Теперь ваш доход составляет:{(chel.improve + (pk.cost / 100))} (рубли/минута)')

                                            INFO_STATUS.refactor_map('Owner_id', chel.id, point)
                                            map_gg.map_gen()
                                            photo = upload_photo('temp_of_map_gen.png')
                                            send_messagept(event.chat_id, 'Карта изменена', photo)
                                        else:
                                            send_message(event.chat_id, 'Этот участок занят! Выберите другой.')
                            else:
                                send_message(event.chat_id, 'Недостаточно денег для покупки!')

                elif re.search(r'\bулучшить участок\b', message):
                    maimes = INFO_STATUS.getter_members()
                    pointsd = INFO_STATUS.getter_map_all()
                    point = message.replace('улучшить участок ', '').title()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            for ia in pointsd:
                                if ia.point == point:
                                    if chel.id == ia.owner_id:
                                        send_message(event.chat_id,
                                                     f'Стоимость улучшения: {easy_logic.cost_con(ia.lvl)} рубасецов и {easy_logic.cost_res(ia.lvl)} ресурсов')
                                        if chel.coins >= easy_logic.cost_con(
                                                ia.lvl) and chel.r_c >= easy_logic.cost_res(ia.lvl):
                                            send_message(event.chat_id,
                                                         'Вы успешно улучшили участок. Доход с участка увеличен.')
                                            INFO_STATUS.refactor_member('coins',
                                                                        chel.coins - easy_logic.cost_con(ia.lvl),
                                                                        chel.id)
                                            INFO_STATUS.refactor_member('res_count',
                                                                        chel.r_c - easy_logic.cost_res(ia.lvl),
                                                                        chel.id)
                                            INFO_STATUS.refactor_map('lvl',
                                                                     ia.lvl + 1,
                                                                     ia.point)

                                            INFO_STATUS.refactor_member('improve_money',
                                                                        chel.improve - (ia.lvl * (ia.cost / 100)) + (
                                                                                (ia.lvl + 1) * (ia.cost / 100)),
                                                                        chel.id)

                elif message == '⚒сменить профессию⚒':
                    send_messageklava(event.chat_id, 'Выбирайте', "keyboards/jobs.json")

                elif message == '💰торговец💰':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.classs == 'Безработный':
                                INFO_STATUS.refactor_member('class', 'Торговец', chel.id)
                                send_message(event.chat_id, 'Поздравляем, теперь вы Торговец!')

                elif message == '⚗алхимик⚗':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.classs == 'Безработный':
                                INFO_STATUS.refactor_member('class', 'Алхимик', chel.id)
                                send_message(event.chat_id, 'Поздравляем, теперь вы Алхимик!')

                elif message == '📙учитель немецкого📙':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.classs == 'Безработный':
                                INFO_STATUS.refactor_member('class', 'Учитель Немецкого', chel.id)
                                send_message(event.chat_id, 'Поздравляем, теперь вы Учитель Немецкого!')

                elif message == '⚒работать⚒':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.classs == 'Алхимик':
                                if chel.energy - (chel.lvl + 1) * 30 > 0:
                                    energy = chel.energy - (chel.lvl + 1) * 30
                                    INFO_STATUS.refactor_member('energy', energy, chel.id)
                                    xp = random.randint((chel.lvl + 1) * 25, (chel.lvl + 1) * 100)
                                    INFO_STATUS.refactor_member('xp', chel.xp + xp, chel.id)
                                    info = f"""
                                    🎯Работа🎯 Алхимика очень тяжела, порой она заставляет взглянуть на мир по-другому. 
                                    Постоянно смешивая склянки, он что-то открыл для себя. 
                                    @id{chel.id}({chel.name}) работал сегодня очень усрендно и получил {xp} опыта.
                                    При этом он потратил 💚{(chel.lvl + 1) * 30}💚 энергии. У него осталось только 💚{energy}💚 энерии .
                                                                                            """
                                    money = random.randint((chel.lvl + 1) * 3, (chel.lvl + 1) * 25)
                                    INFO_STATUS.refactor_member('coins', chel.coins + money, chel.id)
                                    if money < ((chel.lvl + 1) * 3 + (chel.lvl + 1) * 25) // 2:
                                        info_2 = f'Однако начальник его не взлюбил, поэтому дал всего лишь 💰{money}💰 падших рублей.'
                                    else:
                                        info_2 = f'И ему повезло, ведь начальник дал ему целых 💰{money}💰 падших рублей.'
                                    info = info + info_2
                                    send_message(event.chat_id, info)
                                    send_message(event.chat_id,
                                                 f'Уровень @id{chel.id}({chel.name}): {chel.lvl}||| Опыт: 🔰{chel.xp + xp}/{easy_logic.lvl_formula(chel.lvl)}🔰')
                                    up_lvl(event.chat_id, chel.xp, xp, chel.lvl, chel.id)
                                    chandgd = random.randint(chel.lvl, (chel.lvl + 1))
                                    if chandgd == 1 or chandgd == 2:
                                        chance2 = (random.randint(1, 16))
                                        if chance2 == 16:
                                            chance3 = (random.randint(1, 3))
                                            if chance3 == 1:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления эенергии!')
                                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                            if chance3 == 2:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления здоровья!')
                                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                            if chance3 == 3:
                                                send_message(event.chat_id, 'Вы получили пиво!')
                                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                    elif chandgd == 3 or chandgd == 5:
                                        chance2 = (random.randint(1, 8))
                                        if chance2 == 4:
                                            chance3 = (random.randint(1, 3))
                                            if chance3 == 1:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления эенергии!')
                                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                            if chance3 == 2:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления здоровья!')
                                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                            if chance3 == 3:
                                                send_message(event.chat_id, 'Вы получили пиво!')
                                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                    elif chandgd == 6 or chandgd == 8:
                                        chance2 = (random.randint(1, 4))
                                        if chance2 == 3:
                                            chance3 = (random.randint(1, 3))
                                            if chance3 == 1:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления эенергии!')
                                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                            if chance3 == 2:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления здоровья!')
                                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                            if chance3 == 3:
                                                send_message(event.chat_id, 'Вы получили пиво!')
                                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                    elif chandgd == 9 or chandgd == 10:
                                        chance2 = (random.randint(1, 2))
                                        if chance2 == 2:
                                            chance3 = (random.randint(1, 3))
                                            if chance3 == 1:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления эенергии!')
                                                INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                            if chance3 == 2:
                                                send_message(event.chat_id,
                                                             'Вы получили зелье восстановления здоровья!')
                                                INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                            if chance3 == 3:
                                                send_message(event.chat_id, 'Вы получили пиво!')
                                                INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                    else:
                                        chance3 = (random.randint(1, 3))
                                        if chance3 == 1:
                                            send_message(event.chat_id, 'Вы получили зелье восстановления эенергии!')
                                            INFO_STATUS.refactor_member('ener_count', chel.en_c + 1, chel.id)
                                        if chance3 == 2:
                                            send_message(event.chat_id, 'Вы получили зелье восстановления здоровья!')
                                            INFO_STATUS.refactor_member('hill_count', chel.h_c + 1, chel.id)
                                        if chance3 == 3:
                                            send_message(event.chat_id, 'Вы получили пиво!')
                                            INFO_STATUS.refactor_member('beer_count', chel.b_c + 1, chel.id)
                                else:
                                    send_message(event.chat_id, f'💚Недостаточно энергии💚')
                            elif chel.classs == 'Учитель Немецкого':
                                if chel.energy - (chel.lvl + 1) * 30 > 0:
                                    energy = chel.energy - (chel.lvl + 1) * 30
                                    INFO_STATUS.refactor_member('energy', energy, chel.id)
                                    xp = random.randint((chel.lvl + 1) * 100, (chel.lvl + 1) * 300)
                                    INFO_STATUS.refactor_member('xp', chel.xp + xp, chel.id)
                                    info = f"""
                                    🎯Работа🎯 Учителя Немецкого очень тяжела, порой она заставляет взглянуть на мир по-другому. 
                                    Постоянно обучая несмышлёнышей, он что-то открыл для себя. 
                                    @id{chel.id}({chel.name}) работал сегодня очень усрендно и получил {xp} опыта.
                                    При этом он потратил 💚{(chel.lvl + 1) * 30}💚 энергии. У него осталось только 💚{energy}💚 энерии .
                                                                                            """
                                    money = random.randint((chel.lvl + 1) * 3, (chel.lvl + 1) * 25)
                                    INFO_STATUS.refactor_member('coins', chel.coins + money, chel.id)
                                    if money < ((chel.lvl + 1) * 3 + (chel.lvl + 1) * 25) // 2:
                                        info_2 = f'Однако начальник его не взлюбил, поэтому дал всего лишь 💰{money}💰 падших рублей.'
                                    else:
                                        info_2 = f'И ему повезло, ведь начальник дал ему целых 💰{money}💰 падших рублей.'
                                    info = info + info_2
                                    send_message(event.chat_id, info)
                                    send_message(event.chat_id,
                                                 f'Уровень @id{chel.id}({chel.name}): {chel.lvl}||| Опыт: 🔰{chel.xp + xp}/{easy_logic.lvl_formula(chel.lvl)}🔰')
                                    up_lvl(event.chat_id, chel.xp, xp, chel.lvl, chel.id)
                                else:
                                    send_message(event.chat_id, f'💚Недостаточно энергии💚')

                            elif chel.classs == 'Торговец':
                                if chel.energy - (chel.lvl + 1) * 30 > 0:
                                    energy = chel.energy - (chel.lvl + 1) * 30
                                    INFO_STATUS.refactor_member('energy', energy, chel.id)
                                    xp = random.randint((chel.lvl + 1) * 25, (chel.lvl + 1) * 100)
                                    INFO_STATUS.refactor_member('xp', chel.xp + xp, chel.id)
                                    info = f"""
                                    🎯Работа🎯 Торговца очень тяжела, порой она заставляет взглянуть на мир по-другому. 
                                    Постоянно продавая товары, он что-то открыл для себя. 
                                    @id{chel.id}({chel.name}) работал сегодня очень усрендно и получил {xp} опыта.
                                    При этом он потратил 💚{(chel.lvl + 1) * 30}💚 энергии. У него осталось только 💚{energy}💚 энерии .
                                                                                            """
                                    money = random.randint((chel.lvl + 1) * 60, (chel.lvl + 1) * 250)
                                    INFO_STATUS.refactor_member('coins', chel.coins + money, chel.id)
                                    if money < ((chel.lvl + 1) * 3 + (chel.lvl + 1) * 25) // 2:
                                        info_2 = f'Однако начальник его не взлюбил, поэтому дал всего лишь 💰{money}💰 падших рублей.'
                                    else:
                                        info_2 = f'И ему повезло, ведь начальник дал ему целых 💰{money}💰 падших рублей.'
                                    info = info + info_2
                                    send_message(event.chat_id, info)
                                    send_message(event.chat_id,
                                                 f'Уровень @id{chel.id}({chel.name}): {chel.lvl}||| Опыт: 🔰{chel.xp + xp}/{easy_logic.lvl_formula(chel.lvl)}🔰')
                                    up_lvl(event.chat_id, chel.xp, xp, chel.lvl, chel.id)
                                else:
                                    send_message(event.chat_id, f'💚Недостаточно энергии💚')
                            else:
                                send_message(event.chat_id, 'Сначала выберите себе профессию!!!!!')


                elif message == 'аоа':
                    send_messageklava(event.chat_id, 'На', r"keyboards/aoa.json")

                elif message == '🏔мир🏔':
                    upload = upload_photo('media/locations/town.png')
                    send_messagept(event.chat_id, 'Вы в городе! Следует знать свой путь.', upload)
                    send_messageklava(event.chat_id, 'Куда идём?', "keyboards/big_world.json")
                elif message == '🍻таверна🍻':
                    upload = upload_photo('media/locations/Tavern.png')
                    send_messagept(event.chat_id, 'Вы в таверне! Будьте осторожны! Кто знает, что здесь твориться.',
                                   upload)
                    send_messageklava(event.chat_id, 'Что делаем?', "keyboards/tavern.json")

                elif message == '🎵заказать песню🎵':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.coins - 30 <= 0:
                                send_message(event.chat_id, 'Недостаточно денег.')
                                continue
                            INFO_STATUS.refactor_member('coins', chel.coins - 30, chel.id)
                            send_message(event.chat_id,
                                         'Вы пытаетесь дёрнуть барда, чтобы он вам наваял что-нибудь душевное! '
                                         'Он предлагает свой репертуар')
                            audio = ['audio246767805_456239265', 'audio246767805_456239380', 'audio246767805_456239379',
                                     'audio246767805_456239378']
                            for i in range(4):
                                send_messagemusic(event.chat_id, f'Песня №{i + 1}', audio[i])

                elif message == '💬поговорить с трактирщиком💬':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.pointnow != '0':
                                send_message(event.chat_id, 'Вы не в городе!')
                                continue
                            if chel.coins - 50 <= 0:
                                send_message(event.chat_id, 'Недостаточно денег.')
                                continue
                            INFO_STATUS.refactor_member('coins', chel.coins - 50, chel.id)
                            send_message(event.chat_id,
                                         'Трактирщик кажется вам самым осведомлённым существом в мире.'
                                         'Он показывает вам новости.')
                            news = pars_it_news()
                            for i in range(len(news[0])):
                                send_message(event.chat_id, '⚜' + news[0][i] + news[1][i] + '⚜')



                elif message == '🏪лавка🏪':
                    upload = upload_photo('media/locations/shop.png')
                    send_messagept(event.chat_id, 'Вы в магазине! Покупайте товары по демократичным ценам!', upload)
                    send_messageklava(event.chat_id, 'Что делаем?', "keyboards/shop.json")

                elif message == '🏠дом🏠':
                    send_messageklava(event.chat_id, 'С возвращением!', "keyboards/world_and_you.json")
                elif message == '📜управление землёй📜':
                    send_messageklava(event.chat_id, 'Вперёд', "keyboards/my_earth.json")

                elif message == '❔глоссарий по боту❔':
                    send_messageklava(event.chat_id, 'На', "keyboards/bot_info.json")

                elif message == '⚒профессии⚒':
                    send_message(event.chat_id, """Итак, искатель приключений и божественного пива, ты решил узнать, 
                    какие существуют профессии. Что ж, я отвеечу на твой вопрос. Всего их три: Алхимик (не советую 
                    натыкаться на них в безлюдном переулке, они обязательно предложат Вам выпить зелье; но если вы 
                    бвли неосторожны, то лучше бегите, потому что у них всегда есть крупные знакомые), 
                    Торговец (обязательно продаст то, что давно пылится на дальней полке склада) и Учитель Немецкого 
                    (для самых нестандартных личностей). Профессию можно выбрать только однажды, поэтому выбирайте с умом! 
                    
                    """)

                elif message == '🏞земли🏞':
                    maimes = INFO_STATUS.getter_members()
                    for chel in maimes:
                        if chel.id == event.obj['from_id']:
                            if chel.lvl < 10:
                                send_message(event.chat_id, """Ты чё припёрся?..Про земли выведать? Ты чё, самый 
                                богатый тут? А? У тебя даже титула нет. Пшёл! До 10 уровня ничего не скажу. ) 
                                """)
                            else:
                                send_message(event.chat_id, """Ты чё припёрся?..Про земли выведать? Ты чё, самый 
                                богатый тут? А? А, так Вы не обычный простолюдин... Прошу меня простить. Итак, 
                                есть две основные команды: 'купить участок [координаты участка, например, 'A1']', 
                                'улучшить участок [координаты участка]'.  Первый участок Вы можете купить, 
                                начиная с 10 уровня. Каждый последующий будет доступен через каждые 10 уровней. Самые 
                                дешёвые участки находятся на окраинах карты, самые дорогие и прибыльные - в центре. 
                                На улучшение участка тратятся деньги и ресурсы. На прибыльность участка влияет 
                                исключительно его уровень и местоположение. ) 
                                """)

                elif message == '🔰уровень/ресурсы🔰':
                    send_message(event.chat_id, """Не говори, что ты не знаешь, что такое уровень...Погоди, так это 
                    не шутка. Нет, нет, не проси, это слишком очевидно. Мда...давненько я не встречал таких 
                    настырных. Ладно, рассказываю только один раз, слушай внимательно. Повышать уровень есть 
                    несколько путей: работа, путешествия по землям охоты и участвуя там в битвах. Спрашивается: 
                    "Зачем?" Так вот, уровень отвечает за такие основополагающие показатели как здоровоье и энергия и 
                    их скорость восполнения. Также уровень отвечает за силу атаки и за количество получаемых денег. 
                    Быть может, я упустил некоторые детали, но, думаю, ты разберёшься. Ресурсы возможно получить 
                    только на охоте. Их тратят на улучшение земель. 

                                        """)


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


opa = threading.Thread(target=upp_money)
opa.start()
opa1 = threading.Thread(target=decris_calld)
opa1.start()
bot_session = vk_api.VkApi(
    token="448a161c4370d920f09782b8ea67453e58f64ebe60444d3a6e3c99de30c1f6214ff9e838e3f713e7ee246")
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 198702757)
main_conept()
