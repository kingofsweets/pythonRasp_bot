import sqlite3


def getter():
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
        members.append(a)
    return members


def refactor(property, value, id):
    db = sqlite3.connect('info_pan.db')
    cursor = db.cursor()
    cursor.execute(f"""Update info_char set {property} = '{value}' where id = '{id}' """)
    db.commit()
    db.close()


class Infochar():
    name = ''
    id = ''
    coins = 0
    gay_lvl = 0
    lvl = 0

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

