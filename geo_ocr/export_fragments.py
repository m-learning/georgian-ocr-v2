#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import codecs
import cgi
import cv2

# FIXME This is a relative path depended on output parameter
RAW_FRAGMENTS_DIR=os.path.join(os.getcwd(),'results/raw-fragments/')


def create_char_element(meta_obj, fragment_name):
    # Read template
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 
          'export_templates/character-image.fragment.svg'), 'r') as content_file:
        fragment_template = content_file.read()
    
    fragment_template = fragment_template.replace('{image}', fragment_name)
    fragment_template = fragment_template.replace('{x}', str(meta_obj['x']))
    fragment_template = fragment_template.replace('{y}', str(meta_obj['y']))
    fragment_template = fragment_template.replace('{width}', str(meta_obj['w']))
    fragment_template = fragment_template.replace('{height}', str(meta_obj['h']))

    return fragment_template

def export_svg(original_image, meta_dir, fragment_dir, output_svg):
    # Read template
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'export_templates/page.svg'), 'r') as content_file:
        page_template = content_file.read()

    image_height, image_width, _ = cv2.imread(original_image).shape
    # Replace values
    page_template = page_template.replace('{width}', str(image_width))
    page_template = page_template.replace('{height}', str(image_height))
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
                page_template = page_template.replace('{content}', 
                    create_char_element(meta_obj, RAW_FRAGMENTS_DIR+f[:-5]+'.png')+'{content}')

    # Write output
    with codecs.open(output_svg, 'w') as output_file:
        output_file.write(page_template)


if __name__ == "__main__":
    if len(sys.argv) > 4:
        original_image = sys.argv[1]
        meta_dir = sys.argv[2]
        fragment_dir = sys.argv[3]
        output_html = sys.argv[4]

        export_svg(original_image, meta_dir, fragment_dir, output_html)
    else:
        print ("Invalid argument: <original image>, <meta dir>, <fragment dir>, <output svg>")

