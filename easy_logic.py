import random

import INFO_STATUS


def lvl_formula(lvl):
    lvl_next = lvl + 1
    xp = 1000
    for lvl_n in range(lvl_next):
        xp = xp + 1000 * lvl_n * lvl_n
    return xp


def max_energy(lvl):
    energy = (lvl + 1) * 100
    return energy


def max_hp(lvl):
    hp = (lvl + 1) * 100
    return hp


def enem_mhp(lvl):
    hp = (lvl + 1) * 150
    return hp


def gen_pos():
    first_point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    second_point = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    cheli = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    pos = '0'
    flag = 0
    for i in range(10):
        for j in range(10):
            for chel in cheli:
                print(chel.pointnow, first_point[i] + second_point[j])
                if chel.pointnow == first_point[i] + second_point[j]:
                    print('dsd')
                    continue
                else:
                    print('pibo')
                    flag = 1
            for mob in mobs:
                if mob.pointnow == first_point[i] + second_point[j]:
                    print('dsd')
                    continue
                else:
                    print('pibo')
                    flag = 1
            if flag == 1:
                pos = first_point[i] + second_point[j]
                break
        if flag == 1:
            break
    return pos


def up(pos):
    pos_y = pos.replace(pos[0], '')
    second_point = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    flag = 0
    now = 0
    for i in range(10):
        if second_point[i] == pos_y:
            now = i
    chels = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    for chel in chels:
        if chel.pointnow == second_point[now - 1]:
            flag = 1
    for mob in mobs:
        if mob.pointnow == second_point[now - 1]:
            flag = 1
    if second_point[now] != '1' and flag == 0:
        pos_y = second_point[now - 1]

    pos_y = pos[0] + pos_y
    return pos_y


def down(pos):
    pos_y = pos.replace(pos[0], '')
    second_point = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    flag = 0
    now = 0
    for i in range(10):
        if second_point[i] == pos_y:
            now = i
    chels = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    for chel in chels:
        if chel.pointnow == second_point[now - 1]:
            flag = 1
    for mob in mobs:
        if mob.pointnow == second_point[now - 1]:
            flag = 1
    if second_point[now] != '10' and flag == 0:
        pos_y = second_point[now + 1]

    pos_y = pos[0] + pos_y
    return pos_y


def left(pos):
    if len(pos) > 2:
        pos_side = pos[1] + pos[2]
    else:
        pos_side = pos[1]
    pos_x = pos[0]
    first_point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    now = 0
    flag = 0
    for i in range(10):
        if first_point[i] == pos_x:
            now = i
    chels = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    for chel in chels:
        if chel.pointnow == first_point[now - 1]:
            flag = 1
    for mob in mobs:
        if mob.pointnow == first_point[now - 1]:
            flag = 1
    if first_point[now] != 'A' and flag == 0:
        pos_x = first_point[now - 1]
    pos_x = pos_x + pos_side
    return pos_x


def right(pos):
    if len(pos) > 2:
        pos_side = pos[1] + pos[2]
    else:
        pos_side = pos[1]
    pos_x = pos[0]
    first_point = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    now = 0
    flag = 0
    for i in range(10):
        if first_point[i] == pos_x:
            now = i
    chels = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    for chel in chels:
        if chel.pointnow == first_point[now - 1]:
            flag = 1
    for mob in mobs:
        if mob.pointnow == first_point[now - 1]:
            flag = 1
    if first_point[now] != 'J' and flag == 0:
        pos_x = first_point[now + 1]
    pos_x = pos_x + pos_side
    return pos_x


def get_chek():
    mens = INFO_STATUS.getter_members()
    mobs = INFO_STATUS.getter_enem()
    first_point = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', '0']
    second_point = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '0']
    for enemy in mobs:
        pos = enemy.pointnow
        if len(pos) > 2:
            pos_side = pos[1] + pos[2]
        else:
            pos_side = pos[1]
        now_x = 0
        now_y = 0
        for i in range(10):
            if first_point[i] == pos[0]:
                now_x = i
        for i in range(10):
            if second_point[i] == pos_side:
                now_y = i
        pos_to_check = [first_point[now_x] + second_point[now_y - 1], first_point[now_x] + second_point[now_y + 1],
                        first_point[now_x - 1] + second_point[now_y], first_point[now_x + 1] + second_point[now_y],
                        first_point[now_x + 1] + second_point[now_y - 1],
                        first_point[now_x - 1] + second_point[now_y + 1],
                        first_point[now_x - 1] + second_point[now_y - 1],
                        first_point[now_x + 1] + second_point[now_y + 1]]

        for pos in pos_to_check:
            for men in mens:
                if men.pointnow == pos and men.state != 1:
                    INFO_STATUS.refactor_member('state', 1, men.id)
                    INFO_STATUS.refactor_member('id_enem', enemy.id, men.id)
                    INFO_STATUS.refactor_enem('state', 1, enemy.id)
                    break


def rand_energy(lvl):
    energy = random.randint((lvl + 1), (lvl + 2) * 2)
    return energy


def rand_attack(attack, lvl, energy):
    energy_coaff = energy / max_energy(lvl)
    damage = random.randint(attack * (lvl + 1), attack * (lvl + 2))
    damage = energy_coaff * damage
    return damage


def rand_defffe(defence, lvl, energy):
    energy_coaff = energy / max_energy(lvl)
    damage = random.randint(defence * lvl, defence * (lvl + 1))
    damage = energy_coaff * damage
    return damage


def cost_res(lvl):
    lvl_next = lvl + 1
    res = 100
    for lvl_n in range(lvl_next):
        res = res + 20 * lvl_n * lvl_n
    return res


def cost_con(lvl):
    lvl_next = lvl + 1
    con = 10
    for lvl_n in range(lvl_next):
        con = con + 1000 * lvl_n * lvl_n * lvl_n
    return con
