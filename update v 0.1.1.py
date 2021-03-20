from PIL import Image, ImageDraw

im = Image.open("уау.jpg", 'r')
draw_text = ImageDraw.Draw(im)
draw_text.text((100,100),'Test Text', fill='#1C0606')
im.show()