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
    else:

        font = ImageFont.truetype('media/fonts/20170.ttf', 50)
        draw.text((first_coord - 190, second_coord - 190),str(color),
                           fill= ImageColor.getrgb('black'),font = font)

    return draw


def map_gen():
    points = INFO_STATUS.getter_map_for_draw()
    temp = Image.open('media/temp_of_map.png', 'r')
    colori = Image.new('RGBA', temp.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(colori)
    for point in points:
        coloring(point.point, point.color, draw, 0)

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


