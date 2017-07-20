import random
import cv2
import math
import os
import sys
import json
import shutil
import numpy as np
import traceback

from scipy import ndimage


from skimage import color
from skimage import filters
from skimage import img_as_ubyte
from skimage import util
from skimage import img_as_float

# destination directory
FRAGMENTS_DIR = "results/letters"
RAW_FRAGMENTS_DIR = "results/raw-fragments"
META_DIR = "results/meta"
DEBUG_DIR = "results/debug"


def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    os.makedirs(path)


def vanish_image(img,invert=False):
    gray_scale_image = color.rgb2gray(img)
    if invert:
        gray_scale_image = util.invert(gray_scale_image)
    val = filters.threshold_local(gray_scale_image,101,mode="wrap",offset=0.02)
    return (gray_scale_image > val)


def delete_subcrops(img_arrays, debug = True):

    num_of_deleted = 0
    for m1 in img_arrays:
       for m2 in img_arrays:
           if (m1['x'] > m2['x'] and
                  m1['y'] > m2['y'] and
                  m1['x']+m1['w'] < m2['x']+m2['w'] and
                  m1['y']+m1['h'] < m2['y']+m2['h']):

              img_arrays = [s for s in img_arrays if not s['id'] == m1['id']]

              num_of_deleted += 1
              if debug:
                
                imageFilename = "%s/%d.png" % (FRAGMENTS_DIR, m1['id'])
                if os.path.isfile(imageFilename): os.remove(imageFilename)

    print 'Number of deleted sub crops', num_of_deleted
    return img_arrays


def do_fragmentation(file_path, debug = True):
    create_clean_dir(FRAGMENTS_DIR)
    create_clean_dir(META_DIR)
    create_clean_dir(DEBUG_DIR)
    
    # load source image
    src_img = cv2.imread(file_path)


    src_img = cv2.resize(src_img, (0, 0), fx = 4, fy = 4)
    cv2.imwrite(("%s/a0 scaled.png" % DEBUG_DIR), src_img)

    src_img = img_as_ubyte(vanish_image(src_img))
    cv2.imwrite(("%s/a1 vainshed.png" % DEBUG_DIR), src_img)

    #src_img = cv2.bitwise_not(src_img)
    #cv2.imwrite(("%s/a2 inverted.png" % DEBUG_DIR), src_img * 255)

    #src_img = cv2.erode(src_img, None, iterations=1)
    #cv2.imwrite(("%s/a3 eroded.png" % DEBUG_DIR), src_img)

    #src_img = cv2.bitwise_not(src_img)
    #cv2.imwrite(("%s/a4 uninvert.png" % DEBUG_DIR), src_img)
    
    # Find the contours
    _, contours, hierarchy = cv2.findContours(src_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    count = 0
    chars = []

    print 'Number of contures', len(contours)
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        try:
            # Create image file
            x, y, w, h, img_arr = crop_rectangle(src_img, cnt, debug)

            if debug:
                cv2.imwrite(("%s/%s.png" % (FRAGMENTS_DIR, count)), img_arr)

            # Create meta file
            char = {'x': x, 'y': y, 'w': w, 'h': h, 'id': count, 'image': img_arr}
            
            chars.append(char)
            count += 1
        except ValueError, ve:
            if debug:
                traceback.print_exc(file=sys.stdout)
                print "skip fragment:", ve

    # TODO: Last contour is the whole image. It has to be deleted nicely
    #chars = chars[:-1]
    #chars = delete_subcrops(chars, debug)

    full_h, full_w = src_img.shape
    return chars, full_w, full_h
    
    
def create_blank_image(width=64, height=64, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)
    
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color
    
    return image


def create_image_for_recognize(image, width=64, height=64):
    generated_image = np.ones((height, width)) * 255
    (image_h, image_w) = image.shape
    index_w = (width - image_w) / 2
    index_h = (height - image_h) / 2

    generated_image[index_h : image_h + index_h, index_w : image_w + index_w] = image
    return generated_image


def downscale_proportionally(image, max_w, max_h):
    h, w = image.shape[:2]

    downscale_ratio = 1
    if w > h:
       downscale_ratio = float(max_w) / w
    else:
       downscale_ratio = float(max_h) / h

    try:
      crop_img = cv2.resize(image, (0, 0), fx = downscale_ratio, fy = downscale_ratio)
    except:
      print "Could not downscale image"
      crop_img = image
    return crop_img


def crop_rectangle(img, contour, debug):
    x, y, w, h = cv2.boundingRect(contour)
    # TODO: Store original pixels too
    
    crop_img = img[y:y + h, x:x + w]
    
    # define small height and width
    s_height, s_width = crop_img.shape[:2]

    # Shrink if cropped image is oversized
    if s_height > 64 or s_width > 64 or s_height < 20 or s_width < 20:
        crop_img = downscale_proportionally(crop_img, 45, 45)

    # define background image as large image 
    result_img = create_blank_image()

    # define large height and width
    l_height, l_width = result_img.shape[:2]
    
    y_offset = int(math.floor((l_height - s_height) / 2))
    x_offset = int(math.floor((l_width - s_width) / 2))

    ndimage.gaussian_filter(crop_img, 0.8, output=crop_img)
    
    # Convert image to 64x64
    image_to_recognize = create_image_for_recognize(crop_img)
    
    return x, y, w, h, image_to_recognize


if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print ("Invalid argument: <source file>")
