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
symbols = u'!*()-+=.,?;:"'

def paint_text(text, w, h, rotate=False, ud=False, multi_fonts=False, multi_sizes=False, save=False, spackle=False, blur=False):
  surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
  with cairo.Context(surface) as context:
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()
    fonts = [
             {'name':'AcadNusx',                  'type':'latin'},
             {'name':'AcadMtavr',                 'type':'latin'},
             {'name':'Acad Nusx Geo',             'type':'latin'},
             {'name':'LitNusx',                   'type':'latin'},
             {'name':'Chveulebrivi TT',           'type':'latin'},
             {'name':'DumbaNusx',                 'type':'latin'},
             {'name':'Avaza',                     'type':'latin'},
             {'name':'BPG ParaGraph Chveulebrivi','type':'unicode'}, 
             {'name':'BPG Venuri 2010',           'type':'unicode'}, 
             {'name':'BPG Glakho',                'type':'unicode'}, 
             {'name':'BPG Nino Elite',            'type':'unicode'},
             {'name':'BPG Arial',                 'type':'unicode'},
    ]
    if multi_fonts:
      font = np.random.choice(fonts)
      context.select_font_face(font['name'], cairo.FONT_SLANT_NORMAL,
                               np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))
    else:
      font = fonts[0]
      context.select_font_face(font['name'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    if (multi_sizes):
      context.set_font_size(random.randint(20, 52))
    else:
      context.set_font_size(44)
    
    if font['type'] == 'latin' and text in georgian:
      text = latingeo[georgian.index(text)]
    
    box = context.text_extents(text)
    border_w_h = (4, 4)
    #if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
    #  raise IOError('Could not fit string into image. Max char count is too large for given image width.')

    # teach the RNN translational invariance by
    # fitting text box randomly on canvas, with some room to rotate
    max_shift_x = w - box[2] - border_w_h[0]
    max_shift_y = h - box[3] - border_w_h[1]
    top_left_x = np.random.randint(0, int(max_shift_x))
    if ud:
      top_left_y = np.random.randint(0, int(max_shift_y))
    else:
      top_left_y = h // 2
    context.move_to(top_left_x - int(box[0]), top_left_y - int(box[1]))
    context.set_source_rgb(0, 0, 0)
    context.show_text(text)
  if save:
    global img_counter
    img_counter += 1
    surface.write_to_png(create_dir_if_missing('results/gen_imgs/') + 'img_%04d.png' % img_counter)
  buf = surface.get_data()
  a = np.frombuffer(buf, np.uint8)
  a.shape = (h, w, 4)
  a = a[:, :, 0]  # grab single channel
  a = a.astype(np.float32) / 255
  a = np.expand_dims(a, 0)
  if rotate:
    a = image.random_rotation(a, 3 * (w - top_left_x) / w + 1)
  if spackle:
    a = speckle(a)
  if blur:
    ndimage.gaussian_filter(a, 1, output=a)
  return a

chars = georgian + numbers + symbols
LABEL_SIZE = len(chars)

img_w = 64
img_h = 64

y = list_eye(LABEL_SIZE)


def next_batch(size, rotate=False, ud=False, multi_fonts=False, multi_sizes=False, blur=False, save=False):
  print "Generating {0:d} images...".format(size)
  x_train = np.zeros((size, img_w, img_h))
  y_train = [None] * size
  for i in range(size):
    char = chars[random.randint(0, LABEL_SIZE - 1)]
    img = paint_text(char, img_w, img_h, rotate=rotate, ud=ud, multi_fonts=multi_fonts, multi_sizes=multi_sizes, blur=blur, save=save)
    x_train[i] = 1 - img
    y_train[i] = y[chars.index(char)]
  x_train = np.expand_dims(x_train, 3)
  return x_train, y_train


def init_arguments():
  parser = argparse.ArgumentParser(description='random image generator')
  parser.add_argument('text', metavar='text', type=str, nargs='+',
            help='text to generate.')
  parser.add_argument('-w', '--width', metavar='image_width', type=int,
            help='image width (64 is default)', default=64)
  parser.add_argument('--height', metavar='image_height', type=int,
            help='image width (64 is default)', default=64)
  parser.add_argument('-s', '--save_path', metavar='save_path', type=str, default='results/gen_img/test/',
            help='path to save generated images')
  return parser.parse_args()


if __name__ == '__main__':
  args = init_arguments()
  for word in args.text:
    img = paint_text(word.decode('utf-8'), args.width, args.height, rotate=True, ud=True, multi_fonts=True, multi_sizes=True, blur=False, save=False)
    mpimg.imsave(os.path.join(create_dir_if_missing(args.save_path), 'img-%s.png' % word.decode('utf-8')), img[0], cmap="Greys_r")


