#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
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


def is_same_line(char1, char2):
    char1_y_border = char1['y'] + char1['h']
    char2_y_border = char2['y'] + char2['h']

    # Char1 is down
    if char1['y'] > char2_y_border:
        return False

    # Char1 is up
    if char1_y_border < char2['y']:
        return False

    return True


def get_line_first_chars(all_meta, avg_line_height):
    first_chars = []
    for meta in all_meta:
        sorted_chars = get_all_chars_from_line(all_meta, meta, avg_line_height)
        if sorted_chars[0] not in first_chars:
            first_chars.append(sorted_chars[0])
    sorted_first_chars = sorted(first_chars, key=lambda ch: ch['y'])
    return sorted_first_chars


def get_all_chars_from_line(all_meta, char_meta, avg_line_height):
    line_chars = []
    for meta in all_meta:
        if is_same_line(meta, char_meta):
            line_chars.append(meta)

    sorted_line_chars = sorted(line_chars, key=lambda ch: ch['x'])
    return sorted_line_chars


def split_line_with_words(line_chars, avg_char_width):
    next_char = None
    words = ['']
    for i in range(0, len(line_chars)-1):
        char = line_chars[i]
        next_char = line_chars[i+1]

        words[-1] += char['char']

        if next_char['x'] - (char['x']+char['w']) > avg_char_width / 2:
            # New word is starting here
            words.append('')

    if next_char is not None:
        words[-1] += next_char['char']
    return words


def export(all_meta):
    avg_line_height = 40
    avg_char_width = 24
    line_first_chars = get_line_first_chars(all_meta, avg_line_height)

    final_text = ''
    for first_char in line_first_chars:
        all_line_chars = get_all_chars_from_line(all_meta,
                                                 first_char, avg_line_height)

        words = split_line_with_words(all_line_chars, avg_char_width)
        for w in words:
            final_text += w + ' '

        final_text += '\n'

    return final_text.encode('utf-8')


if __name__ == "__main__":
    all_meta = read_meta(os.path.join(os.getcwd(), 'results/meta/'))

    avg_line_height = 40
    avg_char_width = 24
    line_first_chars = get_line_first_chars(all_meta, avg_line_height)

    final_text = ''
    for first_char in line_first_chars:
        all_line_chars = get_all_chars_from_line(all_meta,
                                                 first_char, avg_line_height)

        words = split_line_with_words(all_line_chars, avg_char_width)
        for w in words:
            final_text += w + ' '

        final_text += '\n'
    print final_text.encode('utf-8')
