import random
import secrets
import sqlite3
import easy_logic


# def getter_members_for_calldown():
#     db = sqlite3.connect('info_pan.db')
#     cursor = db.cursor()
#     cursor.execute("SELECT id,time_calld FROM info_char")
#     members = []
#     for member in cursor.fetchall():
#             a = Infochar()
#             a.id = member[0]
#             a.time_calld = [1]
#
#             members.append(a)
#     return members


def getter_members_for_gen():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM info_char ORDER BY coins DESC")
    members = []
    for member in cursor.fetchall():
        if member[12] != '0':
            a = Infochar()
            a.name = member[0]
            a.id = member[1]
            a.time_calld = member[16]
            a.pointnow = member[12]

            members.append(a)
    return members


def getter_enem():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM enemy")
    enemies = []
    for enem in cursor.fetchall():
        a = Enemy()
        a.name = enem[0]
        a.pointnow = enem[1]
        a.step = enem[2]
        a.attack = enem[3]
        a.defence = enem[4]
        a.hp = enem[5]
        a.file_m = enem[6]
        a.file_i = enem[7]
        a.id = enem[8]

        enemies.append(a)
    return enemies


def getter_enem_for_gen():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM enemy")
    enemies = []
    for enem in cursor.fetchall():
        if enem[9] != 1:
            a = Enemy()
            a.name = enem[0]
            a.pointnow = enem[1]
            a.step = enem[2]
            a.attack = enem[3]
            a.defence = enem[4]
            a.hp = enem[5]
            a.file_m = enem[6]
            a.file_i = enem[7]
            a.id = enem[8]

        enemies.append(a)
    return enemies


def getter_members():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM info_char ORDER BY coins DESC")
    members = []
    for member in cursor.fetchall():
        a = Infochar()
        a.name = member[0]
        a.id = member[1]
        a.coins = member[2]
        a.gay_lvl = member[3]
        a.lvl = member[4]
        a.count_events = member[5]
        a.improve = member[6]
        a.titul = member[7]
        a.classs = member[8]
        a.energy = member[9]
        a.xp = member[10]
        a.step = member[11]
        a.pointnow = member[12]
        a.attack = member[13]
        a.defence = member[14]
        a.hp = member[15]
        a.time_calld = member[16]
        a.state = member[17]
        a.id_enem = member[18]

        members.append(a)
    return members


def getter_map_for_draw():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM map")
    points = []
    for point in cursor.fetchall():
        if point[1] == '1':
            a = MAP()
            a.point = point[0]
            a.status = point[1]
            a.owner_id = point[2]
            a.color = point[3]
            a.cost = point[4]
            points.append(a)
    return points


def getter_map_for_buy():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM map")
    points = []
    for point in cursor.fetchall():
        if point[1] != '1':
            a = MAP()
            a.point = point[0]
            a.status = point[1]
            a.owner_id = point[2]
            a.color = point[3]
            a.cost = point[4]
            points.append(a)
    return points


def getter_map_all():
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM map")
    points = []
    for point in cursor.fetchall():
        a = MAP()
        a.point = point[0]
        a.status = point[1]
        a.owner_id = point[2]
        a.color = point[3]
        a.cost = point[4]
        points.append(a)
    return points


def refactor_member(property, value, id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""Update info_char set {property} = '{value}' where id = '{id}' """)
    db.commit()
    db.close()


def delete_member(id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE from info_char where id = '{id}'""")
    db.commit()
    db.close()


def delete_point(id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE from map where id = '{id}'""")
    db.commit()
    db.close()


def delete_enem(id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE from enemy where id = '{id}'""")
    db.commit()
    db.close()


def refactor_map(property, value, point):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""Update map set {property} = '{value}' where coord = '{point}' """)
    db.commit()
    db.close()


def refactor_enem(property, value, id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""Update enemy set {property} = '{value}' where id = '{id}' """)
    db.commit()
    db.close()


class Infochar():
    name = ''
    id = ''
    coins = 0
    gay_lvl = 0
    lvl = 0
    count_events = 0
    improve = 0
    titul = ''
    classs = ''
    energy = 0
    xp = 0
    pointnow = 0
    step = 1
    attack = 10
    defence = 15
    hp = 100
    time_calld = 0
    state = 0
    id_enem = 0

    def saver(self):
        db = sqlite3.connect('info_pan.db')
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO info_char(name, id, coins, gay_lvl, lvl, energy)
                        VALUES('Безработный','{self.id}','0','0','0', '100')
        """)
        db.commit()
        db.close()

    def delete(self):
        pass


class MAP:
    first_point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    color = ''
    point = ''
    status = 'none'
    owner_id = 0
    cost = 450

    def saver(self):
        db = sqlite3.connect('info_pan.db')
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO map(coord, status, owner_id, cost)
                        VALUES('{self.point}','{self.status}','{self.owner_id}','{self.cost}')
        """)
        db.commit()
        db.close()


# j1 = 0
# j2 = 0
# for i in range(0, 100):
#      a = MAP()
#      a.point = a.first_point[j2] + str(j1 + 1)
#      j1 += 1
#      if j1 % 10 == 0:
#          j2 += 1
#      if j1 > 9:
#          j1 = 0
#      a.status = 'none'
#      a.owner_id = '0'
#      a.color = 'none'
#      a.cost = random.randint(250,4000000)
#
#      a.saver()

class Enemy:
    name = ''
    id = ''
    pointnow = 0
    step = 1
    attack = 10
    defence = 15
    hp = 100
    file_m = ''
    file_i = ''
    visibility = 1

    def saver(self):
        db = sqlite3.connect('info_pan.db')
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO enemy(name, id, point_now, file_m, file_i)
                        VALUES('{self.name}','{self.id}','{self.pointnow}','{self.file_m}','{self.file_i}')
        """)
        db.commit()
        db.close()

    def random_go(self):
        pos = self.pointnow
        vector = random.randint(1, 4)
        if vector == 1:
            next_pos = easy_logic.up(pos)
        if vector == 2:
            next_pos = easy_logic.down(pos)
        if vector == 3:
            next_pos = easy_logic.left(pos)
        if vector == 4:
            next_pos = easy_logic.right(pos)
        refactor_enem('point_now', next_pos, self.id)


def gen_rand_pos():
    first_point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    second_point = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    flag = 0
    f_pos = first_point[random.randint(0, 9)]
    s_pos = second_point[random.randint(0, 9)]
    chels = getter_members_for_gen()
    mobs = getter_enem()
    for chel in chels:
        if chel.pointnow == f_pos + s_pos:
            flag = 1
    for mob in mobs:
        if mob.pointnow == f_pos + s_pos:
            flag = 1

    if flag == 0:
        return f_pos + s_pos
    else:
        gen_rand_pos()


def gen_enemies():
    enemys = getter_enem()
    ids = []
    name_s = ['Горный путешественник', 'Вор диких земель', 'Каменщик', 'Призываетльница демонов', 'Падший палач']
    for i in range(3):
        name = random.randint(0, 4)
        f_i = f'{name + 1}var_m.png'
        f_m = f'{name + 1}var.jpg'
        name = name_s[name]
        pos = gen_rand_pos()
        a = Enemy()
        a.name = name
        rans = list(range(0, 200))
        for mob in enemys:
            idem = mob.id.replace('a', '')
            rans.remove(int(idem))
        a.id = 'a' + str(secrets.choice(rans))
        a.pointnow = pos
        a.file_m = f_m
        a.file_i = f_i

        a.saver()
