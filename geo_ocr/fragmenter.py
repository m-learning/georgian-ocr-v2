import random
import cv2
# import cv as cv2
import math
import os
import sys
import json
import shutil
import numpy as np
from scipy import ndimage


from skimage import color
from skimage import filters
from skimage import img_as_ubyte


# destination directory
FRAGMENTS_DIR = "results/letters"
RAW_FRAGMENTS_DIR = "results/raw-fragments"
META_DIR = "results/meta"
DEBUG_DIR = "results/debug"


def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    os.makedirs(path)

def vanish_image(img):
    gray_scale_image = color.rgb2gray(img)
    val = filters.threshold_li(gray_scale_image)
    return (gray_scale_image > val)
              
def find_noise(data):
    width = data["meta"]["w"]
    if width < 13:
        return True
    return False

def do_fragmentation(file_path, debug = True):
    create_clean_dir(FRAGMENTS_DIR)
    create_clean_dir(META_DIR)
    create_clean_dir(DEBUG_DIR)
    
    # load source image
    src_img = cv2.imread(file_path)

    gray = vanish_image(src_img)
    # convert to grayscale
    # gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(("%s/a1 gray.png" % DEBUG_DIR), gray * 255)

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
    
    # thresh = cv2.erode(thresh, None, iterations=2)
    # cv2.imwrite(("%s/a5 erode.png" % DEBUG_DIR), thresh)
    
    # Find the contours
    cv_image = img_as_ubyte(gray)
    _, contours, hierarchy = cv2.findContours(cv_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    allMeta = []
    count = 0

    img_arrays = []
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        try:
            # Create image file
            x, y, w, h, img_arr = crop_rectangle(cv_image, cnt)

            if debug:
                cv2.imwrite(("%s/%s.png" % (FRAGMENTS_DIR, count)), img_arr)

            # Create meta file
            meta = {'x': x, 'y': y, 'w': w, 'h': h, 'id': count}
            
            image_data = {'arr':img_arr, "meta": meta}
            if not find_noise(image_data):
                img_arrays.append(image_data)
                count += 1
        except ValueError, ve:
            if debug:
                print "skip fragment", ve
    return img_arrays
    
    
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


def crop_rectangle(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    
    crop_img = img[y:y + h, x:x + w]
    
    # define background image as large image 
    result_img = create_blank_image()

    # define small height and width
    s_height, s_width = crop_img.shape[:2]
    
    # define large height and width
    l_height, l_width = result_img.shape[:2]
    
    y_offset = int(math.floor((l_height - s_height) / 2))
    x_offset = int(math.floor((l_width - s_width) / 2))
    	
    ndimage.gaussian_filter(crop_img, 1, output=crop_img)
    
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
