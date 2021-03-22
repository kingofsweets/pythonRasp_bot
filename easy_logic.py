def lvl_formula(lvl):
    lvl_next = lvl + 1
    xp = 1000
    for lvl_n in range(lvl_next):
        xp = xp + 1000 * lvl_n
    return xp


def max_energy(lvl):
    energy = (lvl + 1) * 100
    return energy
