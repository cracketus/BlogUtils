import os
from PIL import Image, ImageDraw, ImageFont

__author__ = 'cracketus'

watermark_text = 'Timur Shevlyakov | cracketus'
font_size = 35
# source_dir = 'C:\Users\cricetus\Documents\Blogs\Hohenrausch'
# watermarked_dir = 'C:\Users\cricetus\Documents\Blogs\Hohenrausch\Watermarked'
source_dir = '.\TestImages'
watermarked_dir = '.\TestImages\Watermarked'
image_extension = ['.jpg', '.jpeg', '.png']


def calculate_pos(width, height, text_width, text_height, align='bottom-right'):
    assert width > text_width
    assert height > text_height

    if align == 'top-right':
        return width - text_width - 10, 10
    elif align == 'top-left':
        return 10, 10
    elif align == 'bottom-right':
        return width - text_width - 10, height - text_height - 10
    elif align == 'bottom-left':
        return 10, height - text_height - 10
    elif align == 'center':
        return (width - text_width) / 2 - 5, (height - text_height) / 2 - 5

    return 10, 10


def add_watermark(file, align, fontSize):
    print 'Processing: ' + file
    try:
        full_path = os.path.join(source_dir, file)
        im = Image.open(full_path)

        im_w, im_h = im.size
        watermark = Image.new('RGBA', (im_w, im_h))
        waterdraw = ImageDraw.ImageDraw(watermark, 'RGBA')

        font = ImageFont.truetype("comic.ttf", fontSize)
        w, h = waterdraw.textsize(watermark_text, font)

        x, y = calculate_pos(im_w, im_h, w, h, align)
        waterdraw.text((x, y), watermark_text, font=font)

        watermask = watermark.convert("L").point(lambda x: x !=0 and 150)
        watermark.putalpha(watermask)

        im.paste(watermark, None, watermark)

        wm_file = os.path.join(watermarked_dir, 'wm_' + file)

        im.save(wm_file, 'PNG')

        print 'Saved watermarked image: ' + wm_file
    except IOError as err:
        print('IO error: {0}'.format(err))


def main():
    if not os.path.exists(watermarked_dir):
        os.makedirs(watermarked_dir)

    for f in os.listdir(source_dir):
        extension = os.path.splitext(f)[1].lower()
        if extension in image_extension:
            add_watermark(f, 'bottom-right', font_size)


if __name__ == '__main__':
    main()
