#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import codecs

def read_meta(meta_dir):
  all_meta = []
  # Loop in characters
  for root, _, files in os.walk(meta_dir):
    for f in files:
      fullpath = os.path.join(root, f)


      # Put new one
      with open(fullpath) as json_data:
        meta_obj = json.load(json_data)
        all_meta.append(meta_obj)

  return all_meta
                
def get_average_line_height():
  pass

def get_average_char_width():
  pass

def get_next_line(all_meta, char_meta):
  pass



def get_line_first_chars(all_meta):
  first = all_meta[83]
#  for meta in all_meta:
#    if meta['x'] < first['x']: #and meta['y'] < first['y']:
#      first = meta

  return [all_meta[83]]

def get_char_lines(all_meta):
  lines = []
  for meta in all_meta:
    pass

def get_all_chars_from_line(all_meta, char_meta, avg_line_height):
  char_x = char_meta['x']
  char_y = char_meta['y']
  char_x_border = char_x + char_meta['w']
  char_y_border = char_y + char_meta['h']

  line_chars = []
  for meta in all_meta:
    # Don't add current char
    #if meta['x'] == char_meta['x'] and meta['y'] == char_meta['y']: continue

    meta_x_border = meta['x'] + meta['w']
    meta_y_border = meta['y'] + meta['h']

    # Filter chars from down lines
    if meta['y'] > char_y_border: continue

    # Filter chars from upper lines
    if meta_y_border < char_y : continue

    line_chars.append(meta)

  sorted_line_chars =  sorted(line_chars, key=lambda ch: ch['x'])
  return sorted_line_chars

def split_line_with_words(line_chars, avg_char_width):
  words = ['']
  for i in range(0, len(line_chars)-1):
    char = line_chars[i]
    next_char = line_chars[i+1]

    words[-1]+=char['char']

    if next_char['x'] - (char['x']+char['w']) > avg_char_width / 2:
      # New word is starting here
      words.append('')

  words[-1]+=next_char['char']
  return words


if __name__ == "__main__":
  all_meta = read_meta('results/meta/')

  line_first_chars = get_line_first_chars(all_meta)

  for first_char in line_first_chars:
    all_line_chars = get_all_chars_from_line(all_meta, line_first_chars[0], 40)

    for ch in all_line_chars:
      print ch['char'], ch['x'], ch['y']

    words = split_line_with_words(all_line_chars, 24)
    for w in words:
      print w

