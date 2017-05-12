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

ge2en = {
	u'ა': 'a',
	u'ბ': 'b',
	u'გ': 'g',
	u'დ': 'd',
	u'ე': 'e',
	u'ვ': 'v',
	u'ზ': 'z',
	u'თ': 'T',
	u'ი': 'i',
	u'კ': 'k',
	u'ლ': 'l',
	u'მ': 'm',
	u'ნ': 'n',
	u'ო': 'o',
	u'პ': 'p',
	u'ჟ': 'J',
	u'რ': 'r',
	u'ს': 's',
	u'ტ': 't',
	u'უ': 'u',
	u'ფ': 'f',
	u'ქ': 'q',
	u'ღ': 'R',
	u'ყ': 'y',
	u'შ': 'S',
	u'ჩ': 'C',
	u'ც': 'c',
	u'ძ': 'Z',
	u'წ': 'w',
	u'ჭ': 'W',
	u'ხ': 'x',
	u'ჯ': 'j',
	u'ჰ': 'h',
	u' ': ' ',
}


def translate(text):
	result = ''
	for char in text:
		result += ge2en[char] if char in ge2en else char
	return result


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


def paint_text(text, w, h, rotate=False, ud=False, multi_fonts=False, multi_sizes=False, save=False):
	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
	with cairo.Context(surface) as context:
		context.set_source_rgb(1, 1, 1)  # White
		context.paint()
		# this font list works in Centos 7
		if multi_fonts:
			# fonts = ['FreeMono', 'Serif', 'FreeSerif', 'FreeSans', 'BPG Glakho', 'Monospace']
			fonts = ['AcadNusx', 'AcadMtavr', 'Acad Nusx Geo', 'LitNusx', 'Chveulebrivi TT', 'DumbaNusx']
			context.select_font_face(np.random.choice(fonts), cairo.FONT_SLANT_NORMAL,
			                         np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))
		else:
			context.select_font_face('AcadNusx', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
		if (multi_sizes):
			context.set_font_size(random.randint(14, 32))
		else:
			context.set_font_size(25)
		box = context.text_extents(translate(text))
		border_w_h = (4, 4)
		if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
			raise IOError('Could not fit string into image. Max char count is too large for given image width.')

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
		context.show_text(translate(text))
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
	a = speckle(a)
	return a


#latin_upper = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#latin_lower = u'abcdefghijklmnopqrstuvwxyz'
georgian = u'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ' #ჱჲჳჴჵ'
numbers = u'1234567890'
symbols = u'!@#$%^&*()-+=/\\.,<>?;:"|}{[]'

chars = georgian  # numbers + symbols
LABEL_SIZE = len(chars)

img_w = 64
img_h = 64

y = list_eye(LABEL_SIZE)


def next_batch(size):
	print("generating images...")
	x_train = np.zeros((size, img_w, img_h))
	y_train = [None] * size
	for i in range(size):
		char = chars[random.randint(0, LABEL_SIZE - 1)]
		save = i % 100 == 0
		img = paint_text(char, img_w, img_h, save=save, rotate=True, ud=True, multi_fonts=True, multi_sizes=True)
		x_train[i] = 1 - img
		y_train[i] = y[chars.index(char)]
	x_train = np.expand_dims(x_train, 3)
	return x_train, y_train


def get_test_set(size):
	return next_batch(size)


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
		img = paint_text(word.decode('utf-8'), args.width, args.height, rotate=True, ud=True, multi_fonts=True, multi_sizes=True, save=False)

		img = img[0]

		img *= 255.0

		mpimg.imsave(os.path.join(create_dir_if_missing(args.save_path), 'img-%s.jpg' % word.decode('utf-8')), img, cmap="Greys_r")





