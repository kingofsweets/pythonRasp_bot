from PIL import Image, ImageDraw, ImageColor, ImageFont
import INFO_STATUS
import easy_logic


def draw_enem_info(name, hp, lvl, file, id_e):
    coaff = hp / easy_logic.enem_mhp(lvl)
    print(lvl)
    print(easy_logic.enem_mhp(lvl))
    temp = Image.open(f'media/enemies/{file}', 'r')
    draw = ImageDraw.Draw(temp)
    print(name)
    if file[0] == '2' or file[0] == '3' or file[0] == '5':
        font = ImageFont.truetype('media/fonts/19718.ttf', 50)
    else:
        font = ImageFont.truetype('media/fonts/19718.ttf', 100)
    draw.text((30, 10), name,
              fill=ImageColor.getrgb('black'), font=font)
    if file[0] == '2' or file[0] == '3' or file[0] == '5':
        draw.rectangle((15, 650, 515, 675), fill=ImageColor.getcolor("#4a0600", "RGB"))
        draw.rectangle((15, 650, 515 * coaff + 15, 675), fill=ImageColor.getrgb('red'))
        font = ImageFont.truetype('media/fonts/19718.ttf', 25)
        draw.text((250, 650), str(hp) + f'/{easy_logic.enem_mhp(lvl)}', fill=ImageColor.getrgb('white'), font=font)
    else:
        draw.rectangle((50, 1500, 1050, 1550), fill=ImageColor.getcolor("#4a0600", "RGB"))
        draw.rectangle((50, 1500, 1050 * coaff + 50, 1550), fill=ImageColor.getrgb('red'))
        font = ImageFont.truetype('media/fonts/19718.ttf', 40)
        draw.text((500, 1505), str(hp) + f'/{easy_logic.enem_mhp(lvl)}', fill=ImageColor.getrgb('white'), font=font)

    temp.save(f'{id_e}.jpg')
