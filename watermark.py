import os

import math
from PIL import Image, ImageDraw, ImageFont

__author__ = 'cracketus'

# This script adds watermark text to the image by the given position and text size
# Changes will be applied to all images in the given directory
# Watermarked images will be stored in the given directory as copies

# The main idea of script is to create a new image with the same size. New image has black background and
# gray watermark text. Then we apply this image to original image as for alpha channel.
# RGB of black color is 0x000000. 0x00 corresponds to 100% transparent in alpha-mask and 0xFF is nontransparent.
# Help function calculates gray color according to given transparency.
# So, the watermarked image will look like original picture with the partially transparent text in the given position.
#
# You can change RGB of watermarked text to get more appropriate effect for your images. In the "TestImages" directory
# you find samples pictures to test watermark text (e.g. black-white gradient or some popular textures)

WATERMARK_TEXT = 'Timur Shevlyakov | cracketus'
WATERMARK_TRANSPARENCY = 25  # in percents
WATERMARK_MARGIN = 10
FONT_FILE = 'comic.ttf'
FONT_SIZE = 35
SOURCE_DIR = '.\TestImages'
WATERMARKED_DIR = '.\TestImages\Watermarked'
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def calculate_watermark_color(transparency):
    """
    Help function. Calculate internal color corresponds to given transparency
    :param transparency: transparency in percents
    :return: color
    """
    assert 100 >= transparency >= 0

    color = 255 - (255 / 100 * transparency)
    color = math.floor(color)
    return "#{0:02x}{1:02x}{2:02x}".format(color, color, color)


def calculate_pos(width, height, text_width, text_height, align='top-left'):
    """
    calculate (x, y) coordinates of watermark by given relative position
    :param width: image's width
    :param height: image's height
    :param text_width: text's width
    :param text_height: text's height
    :param align: position of watermark text
    :return: (x, y) coordinates
    """
    assert width > text_width
    assert height > text_height

    if align == 'top-right':
        return width - text_width - WATERMARK_MARGIN, WATERMARK_MARGIN
    elif align == 'top-left':
        return WATERMARK_MARGIN, WATERMARK_MARGIN
    elif align == 'bottom-right':
        return width - text_width - WATERMARK_MARGIN, height - text_height - WATERMARK_MARGIN
    elif align == 'bottom-left':
        return WATERMARK_MARGIN, height - text_height - WATERMARK_MARGIN
    elif align == 'center':
        return (width - text_width - WATERMARK_MARGIN) / 2, (height - text_height - WATERMARK_MARGIN) / 2

    return WATERMARK_MARGIN, WATERMARK_MARGIN


def add_watermark(file_name, align, font_size):
    """
    Add watermark text to given image
    :param file_name: image file
    :param align: relative position in the image
    :param font_size: size of watermark text
    """
    print('Processing: ' + file_name)
    try:
        # open an original image
        full_path = os.path.join(SOURCE_DIR, file_name)
        im = Image.open(full_path)

        # create a watermark image with the same size
        im_w, im_h = im.size
        watermark = Image.new('RGBA', (im_w, im_h))
        # create watermark draw-object to draw text
        draw = ImageDraw.ImageDraw(watermark, 'RGBA')

        # specify font parameters
        font = ImageFont.truetype(FONT_FILE, int(font_size))
        w, h = draw.textsize(WATERMARK_TEXT, font)

        # calculate (x, y)-coordinates for text
        x, y = calculate_pos(im_w, im_h, w, h, align)
        # draw text
        watermark_color = calculate_watermark_color(WATERMARK_TRANSPARENCY)
        draw.text((x, y), WATERMARK_TEXT, watermark_color, font)

        # convert draw object to 8-bit gray-scale and put it as alpha
        watermark.putalpha(watermark.convert("L"))

        # paste watermark to the original image
        im.paste(watermark, None, watermark)

        wm_file = os.path.join(WATERMARKED_DIR, 'wm_' + file_name)

        im.save(wm_file)

        print('Saved watermarked image: ' + wm_file)
    except IOError as err:
        print('IO error: {0}'.format(err))


def main():
    # create a new directory for watermarked images, if not exist
    if not os.path.exists(WATERMARKED_DIR):
        os.makedirs(WATERMARKED_DIR)

    # go through the directory
    for f in os.listdir(SOURCE_DIR):
        extension = os.path.splitext(f)[1].lower()
        # and apply watermark to all images
        if extension in IMAGE_EXTENSIONS:
            add_watermark(f, 'bottom-right', int(FONT_SIZE))


if __name__ == '__main__':
    main()
