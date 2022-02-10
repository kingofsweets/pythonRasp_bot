from PIL import Image, ImageDraw, ImageColor, ImageFont
import INFO_STATUS


def coloring(point, color, draw, value):
    points_f = {
        "A": 200,
        "B": 400,
        "C": 600,
        "D": 800,
        "E": 1000,
        "F": 1200,
        "G": 1400,
        "H": 1600,
        "I": 1800,
        "J": 2000,
    }
    points_s = {
        "1": 200,
        "2": 400,
        "3": 600,
        "4": 800,
        "5": 1000,
        "6": 1200,
        "7": 1400,
        "8": 1600,
        "9": 1800,
        "10": 2000,
    }
    if len(point) > 2:
        first_coord = points_f[point[0]]
        second_coord = points_s[point[1] + point[2]]
    else:
        first_coord = points_f[point[0]]
        second_coord = points_s[point[1]]
    if value == 0:
        colors = color.split(',')
        finec = []
        for colore in colors:
            finec.append(int(colore))

        draw.rectangle((first_coord - 200, second_coord - 200, first_coord, second_coord),
                       fill=(finec[0], finec[1], finec[2], 110))
    elif value == 1:

        font = ImageFont.truetype('media/fonts/20170.ttf', 50)
        draw.text((first_coord - 190, second_coord - 190), str(color),
                  fill=ImageColor.getrgb('black'), font=font)
    elif value == 2:

        font = ImageFont.truetype('media/fonts/19718.ttf', 170)
        draw.text((first_coord - 190, second_coord - 190), str(color),
                  fill=ImageColor.getrgb('black'), font=font)

    return draw


def coloring_enem(point, temp, element):
    points_f = {
        "A": 100,
        "B": 200,
        "C": 300,
        "D": 400,
        "E": 500,
        "F": 600,
        "G": 700,
        "H": 800,
        "I": 900,
        "J": 1000,
    }
    points_s = {
        "1": 100,
        "2": 200,
        "3": 300,
        "4": 400,
        "5": 500,
        "6": 600,
        "7": 700,
        "8": 800,
        "9": 900,
        "10": 1000,
    }
    if len(point) > 2:
        first_coord = points_f[point[0]]
        second_coord = points_s[point[1] + point[2]]
    else:
        first_coord = points_f[point[0]]
        second_coord = points_s[point[1]]

    temp.paste(element, (first_coord - 100, second_coord - 100), element)

    return temp


def map_gen():
    points = INFO_STATUS.getter_map_for_draw()
    temp = Image.open('media/temp_of_map.png', 'r')
    colori = Image.new('RGBA', temp.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(colori)
    for point in points:
        coloring(point.point, point.color, draw, 0)
        coloring(point.point, point.lvl, draw, 2)

    out = Image.alpha_composite(temp, colori)

    out.save('temp_of_map_gen.png')


def map_gen_forbuy():
    map_gen()
    points = INFO_STATUS.getter_map_for_buy()
    print(len(points))
    temp = Image.open('temp_of_map_gen.png', 'r')
    draw = ImageDraw.Draw(temp)
    for point in points:
        coloring(point.point, point.cost, draw, 1)


    temp.save('temp_of_map_gen_forbuy.png')


def genering_dynamics_map():
    pass


def draw_player_ic(idc, name):
    print(name)
    sac = Image.new('RGB', (100, 100))
    wo = name[0] + name[1]
    draw = ImageDraw.Draw(sac)

    font = ImageFont.truetype('media/fonts/19718.ttf', 75)
    draw.text((5,5),wo , font=font)

    sac.save(f'{idc}.png')


def map_gen_for_now():
    players = INFO_STATUS.getter_members_for_gen()
    mobs = INFO_STATUS.getter_enem()
    temp = Image.open('media/temp_of_map_demon.png', 'r')

    for player in players:
        draw_player_ic(player.id, player.name)
        temp_playeer = Image.open(f'{player.id}.png', 'r').convert('RGBA')
        coloring_enem(player.pointnow, temp, temp_playeer)
    for mob in mobs:
        file = 'media/enemies/mini/' + mob.file_i
        temp_enem = Image.open(file, 'r').convert('RGBA')
        coloring_enem(mob.pointnow, temp, temp_enem)

    temp.save('temp_of_map_demon_gen.png')
