#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import cairocffi as cairo
import os
import cv2
import numpy as np
from PIL import ImageFont
import scipy.misc as misc

latingeo = u'abgdevzTiklmnopJrstufqRySCcZwWxjh'
georgian = u'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
numbers = u'1234567890'
symbols = u'!*()-+=.,?;:%/\[]{}<>'

font_names = []

GENERATED_IMAGES_FILE = "results/fonts.png"

img_counter = 0


def paint():
	fonts = list_available_fonts()
	global img_counter

	title_length = 15

	all_symbols = georgian + numbers + symbols

	images_count = len(all_symbols)
	font_count = len(fonts)

	context, surface = get_empty_image(images_count, font_count, title_length)

	for (j, font) in enumerate(fonts):
		generate_image(create_font_record("Ubuntu", "Ubuntu", "Ubuntu"), font['file'], context, 0, j)
		for (i, text) in enumerate(all_symbols):
			generate_image(font, text, context, i + title_length, j)

	surface.write_to_png(
		GENERATED_IMAGES_FILE
	)


def parse_fonts_directory(fonts_path):
	font_files = os.listdir(fonts_path)

	in_font_names = []
	for f in font_files:
		parsed_font = ImageFont.truetype(os.path.join(fonts_path, f))
		in_font_names.append((parsed_font.font.family, f))

	return in_font_names


def list_available_fonts():
	global font_names

	if font_names:
		return font_names

	font_names += [create_font_record(name, 'latin', file_name)
	               for (name, file_name) in parse_fonts_directory('bulk_fonts/latin')]

	font_names += [create_font_record(name, 'unicode', file_name)
	               for (name, file_name) in parse_fonts_directory('bulk_fonts/utf-8')]

	font_names = sorted(font_names, key=lambda c: c['file'])

	return font_names


def create_font_record(name, font_type, file_name):
	return {'name': name, 'type': font_type, 'file': file_name}


def create_dir_if_missing(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def get_empty_image(images_count, fonts_count, title_length):
	imagesize = (64 * (images_count + title_length), 64 * fonts_count)

	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *imagesize)

	with cairo.Context(surface) as context:
		context.set_source_rgb(255, 255, 255)
		context.rectangle(0, 0, *imagesize)
		context.fill()

		context.set_source_rgb(0, 0, 0)
		for i in range(fonts_count):
			context.move_to(0, i * 64)
			context.line_to(64 * (images_count + title_length), i * 64)
			context.stroke()

		context.move_to(title_length * 64, 0)
		context.line_to(title_length * 64, fonts_count * 64)
		context.stroke()
		return context, surface


def generate_image(font, text, context, index, font_index):
	if font is not None:
		context.select_font_face(font['name'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	font_size = 48
	context.set_font_size(font_size)
	context.set_source_rgb(0, 0, 0)

	if font is not None and font['type'] == 'latin' and text in georgian:
		text = latingeo[georgian.index(text)]

	context.move_to(index * 64 + 16, font_index * 64 + 48)
	# context.set_source_rgb(1, 1, 1)
	context.show_text(text)


if __name__ == '__main__':
	paint()
# generate_image(None, "a")
