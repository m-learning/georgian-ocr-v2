#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
import os, os.path
import json
import codecs
import cgi
import cv2

def create_char_element(meta_obj):
    # Read template
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 
          'export_templates/character.fragment.svg'), 'r') as content_file:
        fragment_template = content_file.read()
    
    fragment_template = fragment_template.replace('{char}', cgi.escape(meta_obj['char']).encode('ascii', 'xmlcharrefreplace'))
    fragment_template = fragment_template.replace('{x}', str(meta_obj['x']))
    fragment_template = fragment_template.replace('{y}', str(meta_obj['y']+20))
    # TODO Calculate dynamic size correctly
    fragment_template = fragment_template.replace('{font-size}', '40px') #str(meta_obj['y'])+'px')

    return fragment_template

def export_svg(original_image, meta_dir, output_svg, background=False):
    # Read template
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'export_templates/page.svg'), 'r') as content_file:
        page_template = content_file.read()

    image_height, image_width, _ = cv2.imread(original_image).shape
    # Replace values
    page_template = page_template.replace('{width}', str(image_width))
    page_template = page_template.replace('{height}', str(image_height))

    if background:
        page_template = page_template.replace('{background-image}', original_image)
        page_template = page_template.replace('{background-image-width}', str(image_width))
        page_template = page_template.replace('{background-image-height}', str(image_height))

    # Loop in characters
    for root, _, files in os.walk(meta_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            
            # Put new one
            with open(fullpath) as json_data:
                meta_obj = json.load(json_data)
#                if meta_obj['accuracy'] == 0: continue

                page_template = page_template.replace('{content}',
                    create_char_element(meta_obj)+'{content}')

    # Write output
    with codecs.open(output_svg, 'w') as output_file:
        output_file.write(page_template)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        original_image = sys.argv[1]
        meta_dir = sys.argv[2]
        output_svg = sys.argv[3]
        output_svg_no_bg = sys.argv[4]

        export_svg(original_image, meta_dir, output_svg_no_bg)
        export_svg(original_image, meta_dir, output_svg, background=True)
    else:
        print ("Invalid argument: <original image>, <meta dir>, <output svg> <output svg without background>")

