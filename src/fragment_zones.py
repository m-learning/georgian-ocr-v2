import random
import cv2
# import cv as cv2
import math
import os
import sys
import json
import numpy as np
from scipy import ndimage

from skimage import color
from skimage import filters
from skimage import img_as_ubyte

# destination directory
FRAGMENTS_DIR = "results/words"
RAW_FRAGMENTS_DIR = "results/raw-fragments"
META_DIR = "results/meta"
DEBUG_DIR = "results/debug"


def create_dir_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)


def vanish_image(img):
    gray_scale_image = color.rgb2gray(img)
    val = filters.threshold_li(gray_scale_image)
    return img_as_ubyte((gray_scale_image > val))

def find_enclosing_meta(allMeta, meta):
    for m in allMeta:
       print m

def delete_subcrops(allMeta):
    for m1 in allMeta:
       for m2 in allMeta:
           if (m1['x'] > m2['x'] and
                  m1['y'] > m2['y'] and
                  m1['x']+m1['w'] < m2['x']+m2['w'] and
                  m1['y']+m1['h'] < m2['y']+m2['h']):
              imageFilename = "%s/%04d.png" % (FRAGMENTS_DIR, m1['id'])
              metaFilename = "%s/%04d.json" % (META_DIR, m1['id'])

              print 'Deleting enclosed fragment', imageFilename
              try:
                  os.remove(imageFilename)
                  os.remove(metaFilename)
              except Exception, e:
                  print e

def do_fragmentation(file_path):
    create_dir_if_missing(FRAGMENTS_DIR)
    create_dir_if_missing(META_DIR)
    create_dir_if_missing(DEBUG_DIR)

    # load source image
    src_img = cv2.imread(file_path)

    src_img = vanish_image(src_img)
    cv2.imwrite(("%s/a1 gray.png" % DEBUG_DIR), src_img * 255)

    # convert to grayscale
    #src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    #gray = cv2.medianBlur(src_img, 5)
    #cv2.imwrite(("%s/a2 medianBlur.png" % DEBUG_DIR), src_img)

    # Apply adaptive threshold
    #src_img = cv2.adaptiveThreshold(src_img, 255, 1, 1, 11, 2)
    #cv2.imwrite(("%s/a3 treshColor.png" % DEBUG_DIR), src_img)

    # apply some dilation and erosion to join the gaps
    #deliated = cv2.dilate(src_img, None, iterations=3)
    #cv2.imwrite(("%s/a4 deliate.png" % DEBUG_DIR), deliated)

    src_img = cv2.erode(src_img, None, iterations=4)
    cv2.imwrite(("%s/a5 erode.png" % DEBUG_DIR), src_img)

    #ndimage.gaussian_filter(src_img, 6, output=src_img)
    #cv2.imwrite(("%s/a5 gausian filtered.png" % DEBUG_DIR), src_img)

    # Find the contours
    _, contours, hierarchy = cv2.findContours(src_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#    allMeta = []
    count = 0
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        count += 1
        try:
            # Create image file
            imageFilename = "%s/%04d.png" % (FRAGMENTS_DIR, count)
            rawImageFilename = "%s/%04d.png" % (RAW_FRAGMENTS_DIR, count)
            x, y, w, h = crop_rectangle(src_img, cnt, imageFilename, rawImageFilename)

            # Create meta file
#            meta = {'x': x, 'y': y, 'w': w, 'h': h, 'id': count}
#            metaFilename = "%s/%04d.json" % (META_DIR, count)
#            f = open(metaFilename, 'w')
#            json.dump(meta, f)
#            f.close()

#            allMeta.append(meta)

        except ValueError, ve:
            print "skip fragment", ve

#    delete_subcrops(allMeta)


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


def crop_rectangle(img, contour, file_name, raw_file_name):
    x, y, w, h = cv2.boundingRect(contour)

    if w * h < 100:
			raise ValueError('Cropping rectangle is too small')

    crop_img = img[y:y + h, x:x + w]

    cv2.imwrite(raw_file_name, crop_img)

    # define background image as large image 
    result_img = create_blank_image()

    # define small height and width
    s_height, s_width = crop_img.shape[:2]

    # define large height and width
    l_height, l_width = result_img.shape[:2]

    y_offset = int(math.floor((l_height - s_height) / 2))
    x_offset = int(math.floor((l_width - s_width) / 2))

    # result_img[y_offset:y_offset + s_height, x_offset:x_offset + s_width] = crop_img
		
    ndimage.gaussian_filter(crop_img, 1, output=crop_img)

    # Convert image to 64x64
    #image_to_recognize = create_image_for_recognize(crop_img)


    cv2.imwrite(file_name, crop_img)

    return x, y, w, h


if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print ("Invalid argument: <source file>")
