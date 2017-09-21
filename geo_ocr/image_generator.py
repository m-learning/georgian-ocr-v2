#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from scipy import ndimage
import cairocffi as cairo
import numpy as np
import random
from keras.preprocessing import image
import os
import argparse
import matplotlib.image as mpimg
from PIL import ImageFont
import cv2
import random

random.seed(55)
np.random.seed(55)


def list_eye(n):
    return np.eye(n).tolist()


def create_dir_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def speckle(img):
    severity = np.random.uniform(0, 0.6)
    blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
    img_speck = (img + blur)
    img_speck[img_speck > 1] = 1
    img_speck[img_speck <= 0] = 0
    return img_speck


# paints the string in a random location the bounding box
# also uses a random font, a slight random rotation,
# and a random amount of speckle noise
img_counter = 0

latingeo = u'abgdevzTiklmnopJrstufqRySCcZwWxjh'
georgian = u'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
numbers = u'1234567890'
symbols = u'!*()-+=.,?;:%/\[]{}<>'

bad_fonts = ['GLKupiura-Bold.ttf', 'GLKupiura-Light.ttf', 'GLKupiura-Medium.ttf', 'GLKupiura-Regular.ttf', 'GLKupiura-UltraLight.ttf',
             'GLMkafio-Book.ttf', 'GLMkafio-Thin.ttf', 'GLMkafio-Light.ttf', 'GLMkafio-Regular.ttf', 'GLMkafio-ExtraLight.ttf', 'GLMkafio-UltraLight.ttf',
			 'GLParizuli-Bold.ttf', 'GLParizuli-Medium.ttf', 'GLParizuli-Regular.ttf']

bad_font_7 = ['GLChonchkhi-Book.ttf', 'GLChonchkhi-Light.ttf', 'GLChonchkhi-Regular.ttf']


GENERATED_IMAGES_DIR = "results/gen_imgs/"

def parse_fonts_directory(fonts_path):
    font_files = os.listdir(fonts_path)

    in_font_names = []
    for f in font_files:
        parsed_font = ImageFont.truetype(os.path.join(fonts_path, f))
        in_font_names.append(parsed_font.font.family)

    return in_font_names


def create_font_record(name, font_type):
    return { 'name': name, 'type': font_type }

font_names = []
def list_available_fonts():
    global font_names

    if font_names: return font_names

    # TODO: Make directory paths configurable
    font_names += [create_font_record(name, 'latin') 
        for name in parse_fonts_directory('bulk_fonts/latin')]

    font_names += [create_font_record(name, 'unicode') 
        for name in parse_fonts_directory('bulk_fonts/utf-8')]

    return font_names


def find_max_font_size(context, text, max_w, max_h):
    font_size = 1000

    context.set_font_size(font_size)
    box = context.text_extents(text)
    w = box[2]
    h = box[3]

    while w > max_w:
        ratio_w = max_w / w
        font_size = font_size * ratio_w
        context.set_font_size(font_size)
        box = context.text_extents(text)
        w = box[2]

    h = box[3]

    while h > max_h:
        ratio_h = max_h / h
        font_size = font_size * ratio_h
        context.set_font_size(font_size)
        box = context.text_extents(text)
        h = box[2]

    return int(font_size)
    

def paint_text(text, w, h,
               rotate=False, ud=False, lr=False, multi_fonts=False,
               multi_sizes=False, save=False, spackle=False, blur=False):

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    with cairo.Context(surface) as context:
        context.set_source_rgb(1, 1, 1)  # White
        context.paint()

    fonts = list_available_fonts()

    if multi_fonts:
        font = np.random.choice(fonts)
        context.select_font_face(font['name'],
                                 cairo.FONT_SLANT_NORMAL,
                                 np.random.choice([cairo.FONT_WEIGHT_BOLD,
                                                   cairo.FONT_WEIGHT_NORMAL]))
    else:
        font = fonts[0]
        context.select_font_face(font['name'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)


    if (multi_sizes):
        max_font_size = find_max_font_size(context, text, img_w, img_h) - 4
        if not max_font_size:
            print 'Damaged font', font['name'], 'for text', text
            raise ValueError('Damaged font')

        context.set_font_size(random.randint(25, max_font_size))
    else:
        context.set_font_size(44)

    if font['type'] == 'latin' and text in georgian:
        text = latingeo[georgian.index(text)]
    if font is not None and (text == '/' or text == '\\') and font['file'] in bad_fonts:
        context.select_font_face(font_names[0]['name'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    if font is not None and text == '7' and font['file'] in bad_font_7:
        context.select_font_face(font_names[0]['name'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        
    box = context.text_extents(text)
    text_w = box[2]
    text_h = box[3]
    border_w_h = (4, 4)
    # if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
    #     raise IOError('Could not fit string into image. \
    #                   Max char count is too large for given image width.')

    # teach the RNN translational invariance by
    # fitting text box randomly on canvas, with some room to rotate
    max_shift_x = w - text_w - border_w_h[0]
    max_shift_y = h - text_h - border_w_h[1]

    if int(max_shift_x) <= 0:
      max_shift_x = 1
      
    if int(max_shift_y) <= 0:
      max_shift_y = 1
    
    
    if lr:
        top_left_x = np.random.randint(0, int(max_shift_x))
    else:
        top_left_x = w // 2 - text_w // 2

    if ud:
        top_left_y = np.random.randint(0, int(max_shift_y))
    else:
        top_left_y = h // 2 - text_h // 2


    context.move_to(top_left_x - int(box[0]), top_left_y - int(box[1]))
    #context.set_source_rgb(0, 0, 0)
    context.show_text(text)
    if save:
        global img_counter
        img_counter += 1
        surface.write_to_png(
            create_dir_if_missing(GENERATED_IMAGES_DIR) + 'img_%04d.png' % img_counter
        )
    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (h, w, 4)
    a = a[:, :, 0]  # grab single channel
    a = np.expand_dims(a, 0)
    if rotate:
        a = image.random_rotation(a, 7 * (w - top_left_x) / w + 1)
    #if spackle:
    #    a = speckle(a)

    a = np.squeeze(a)

    #if blur:
    #    ndimage.gaussian_filter(a, np.random.randint(0, 2), output=a)

    # Randomly reverse colors
    #if bool(random.getrandbits(1)):
    #  a = 255-a

#    global img_counter
#    img_counter += 1
#    print img_counter, text
#    cv2.imwrite((u"%s/%s-%s.png" % (GENERATED_IMAGES_DIR, img_counter, font['name'])), a)

    a = a.astype(np.float32) / 255
    return a


chars = georgian + numbers + symbols
LABEL_SIZE = len(chars)

img_w = 64
img_h = 64

y = list_eye(LABEL_SIZE)


def next_batch(size, rotate=False, ud=False, lr=False,
               multi_fonts=False, multi_sizes=False, blur=False, save=False):

    create_dir_if_missing(GENERATED_IMAGES_DIR)

    print "Generating {0:d} images...".format(size)
    x_train = np.zeros((size, img_w, img_h))
    y_train = [None] * size
    for i in range(size):
        while True:
            try:
                char = chars[random.randint(0, LABEL_SIZE - 1)]
                img = paint_text(char, img_w, img_h,
                                 rotate=rotate, ud=ud, lr=lr, multi_fonts=multi_fonts,
                                 multi_sizes=multi_sizes, blur=blur, save=save)
                break
            except ValueError, e:
                # FIXME: Wrong decision!
                print e

        x_train[i] = 1 - img
        y_train[i] = y[chars.index(char)]
    x_train = np.expand_dims(x_train, 3)
    return x_train, y_train


def init_arguments():
    parser = argparse.ArgumentParser(description='random image generator')
    parser.add_argument('text', metavar='text',
                        type=str, nargs='+', help='text to generate.')
    parser.add_argument('-w', '--width',
                        metavar='image_width', type=int,
                        help='image width (64 is default)', default=64)
    parser.add_argument('--height',
                        metavar='image_height', type=int,
                        help='image width (64 is default)', default=64)
    parser.add_argument('-s', '--save_path',
                        metavar='save_path',
                        type=str, default='results/gen_img/test/',
                        help='path to save generated images')
    return parser.parse_args()


if __name__ == '__main__':
    args = init_arguments()

    for word in args.text:
        img = paint_text(word.decode('utf-8'),
                         args.width, args.height,
                         rotate=True, ud=True, multi_fonts=True,
                         multi_sizes=True, blur=False, save=False)
        mpimg.imsave(
            os.path.join(
                create_dir_if_missing(args.save_path),
                'img-%s.png' % word.decode('utf-8')), img[0], cmap="Greys_r")
