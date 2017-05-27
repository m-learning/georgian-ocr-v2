#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import cgi

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

def get_next_char(all_meta, char_meta, avg_char_width):
  char_x = char_meta['x']
  char_y = char_meta['y']
  char_x_border = char_x + char_meta['w']
  char_y_border = char_y + char_meta['y']

  for meta in all_meta:
    if meta['x'] == char_meta['x'] and meta['y'] == char_meta['y']: continue

    meta_x_border = meta['x'] + meta['w']
    meta_y_border = meta['y'] + meta['h']

    # Filter chars from other lines
    if meta['y'] > char_y_border: continue

    # Filter chars from other words
    if meta_x_border - char_x_border > avg_char_width / 2: continue
    
    # Filter chars before
    if meta['x'] < char_x: continue

    return meta


def get_first_char(all_meta):
  first = all_meta[0]
  for meta in all_meta:
    print meta['id'], meta['x'], meta['y'], ' ', first['id'], first['x'], first['y']
    if meta['x'] < first['x']: #and meta['y'] < first['y']:
      first = meta

  return first

def get_chars_by_lines(all_meta):
  pass

if __name__ == "__main__":
  all_meta = read_meta('results/meta/')
  print all_meta

  char = get_first_char(all_meta)
  while char is not None:
    print char['char']
    char = get_next_char(all_meta, char, 40)
    


