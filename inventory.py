from PIL import Image, ImageDraw, ImageColor, ImageFont
import INFO_STATUS
import easy_logic


def draw_inventory(count1, count2, count3, count4, count5, id_chel):
    temp = Image.open(f'media/temp_of_i.png', 'r')
    draw = ImageDraw.Draw(temp)
    font = ImageFont.truetype('media/fonts/19718.ttf', 70)
    draw.text((300, 320), str(count1), fill=ImageColor.getrgb('black'), font=font)
    draw.text((700, 320), str(count2), fill=ImageColor.getrgb('black'), font=font)
    draw.text((1100, 320), str(count3), fill=ImageColor.getrgb('black'), font=font)
    draw.text((1500, 320), str(count4), fill=ImageColor.getrgb('black'), font=font)
    draw.text((1900, 320), str(count5), fill=ImageColor.getrgb('black'), font=font)

    temp.save(f'{id_chel}_i.png')

