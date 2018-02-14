import random
import cv2
import math
import sys
import json
import numpy as np
import traceback
import file_operations as file_ops

from scipy import ndimage
#from transform import deskew_image

from skimage import color
from skimage import filters
from skimage import img_as_ubyte
from skimage import util

import numpy as np
import segmenter
import vanish 



def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    os.makedirs(path)



def do_fragmentation(src_img, debug = True):


    # Find the contours
    _, contours, hierarchy = cv2.findContours(src_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    chars = []
    print ('Number of contures', len(contours))
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        try:
            x, y, w, h = cv2.boundingRect(cnt)

            # Create meta file
            char = {'x': x, 'y': y, 'w': w, 'h': h, 'id': count, 'contours': cnt}

            chars.append(char)
            count += 1
        except ValueError as ve:
            if debug:
                traceback.print_exc(file=sys.stdout)
                print ("skip fragment:", ve)
    
    full_h, full_w = src_img.shape
    
    return chars, full_w, full_h


if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print ("Invalid argument: <source file>")
