import random
import cv2
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
ZONES_DIR = "results/zones"
DEBUG_DIR = "results/debug"


def create_dir_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)


def vanish_image(img):
    gray_scale_image = color.rgb2gray(img)
    val = filters.threshold_li(gray_scale_image)
    return img_as_ubyte(gray_scale_image > val)


def do_fragmentation(file_path):
    create_dir_if_missing(ZONES_DIR)
    create_dir_if_missing(DEBUG_DIR)

    # load source image
    src_img = cv2.imread(file_path)

    src_img = vanish_image(src_img)
    # convert to grayscale
    # gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(("%s/a1 gray.png" % DEBUG_DIR), src_img)

    # smooth the image to avoid noises
    # gray = cv2.medianBlur(gray, 5)
    # cv2.imwrite(("%s/a2 medianBlur.png" % DEBUG_DIR), gray)

    # Apply adaptive threshold
    # thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    # thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # cv2.imwrite(("%s/a3 treshColor.png" % DEBUG_DIR), thresh_color)

    # apply some dilation and erosion to join the gaps
    # thresh = cv2.dilate(thresh, None, iterations=3)
    # cv2.imwrite(("%s/a4 deliate.png" % DEBUG_DIR), thresh)

    src_img = cv2.erode(src_img, None, iterations=10)
    cv2.imwrite(("%s/a5 erode.png" % DEBUG_DIR), src_img)

    # Find the contours
    _, contours, hierarchy = cv2.findContours(src_img,
                                              cv2.RETR_LIST,
                                              cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        count += 1
        try:
            # Create image file
            imageFilename = "%s/%04d.png" % (ZONES_DIR, count)
            x, y, w, h = crop_rectangle(src_img, cnt, imageFilename)

        except ValueError as ve:
            print "skip fragment", ve


def create_blank_image(width=64, height=64, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


def crop_rectangle(img, contour, file_name):
    x, y, w, h = cv2.boundingRect(contour)

    if w * h < 2000:
        raise ValueError('Cropping rectangle is too small')

    crop_img = img[y:y + h, x:x + w]

    cv2.imwrite(file_name, crop_img)

    return x, y, w, h


if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print("Invalid argument: <source file>")
