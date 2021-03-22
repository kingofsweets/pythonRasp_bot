import random
import sqlite3


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


def refactor_map(property, value, point):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""Update map set {property} = '{value}' where coord = '{point}' """)
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

    def saver(self):
        db = sqlite3.connect('info_pan.db')
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO info_char(name, id, coins, gay_lvl,lvl)
                        VALUES('{self.name}','{self.id}','{self.coins}','{self.gay_lvl}','{self.lvl}')
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

j1 = 0
j2 = 0
for i in range(0, 100):
     a = MAP()
     a.point = a.first_point[j2] + str(j1 + 1)
     j1 += 1
     if j1 % 10 == 0:
         j2 += 1
     if j1 > 9:
         j1 = 0
     a.status = 'none'
     a.owner_id = '0'
     a.color = 'none'
     a.cost = random.randint(250,4000000)

     a.saver()
