import random
import cv2
import math
import sys
import json
import numpy as np
import traceback
from multiprocessing import Process
from multiprocessing import Manager
import file_operations as file_ops

from scipy import ndimage
from transform import deskew_image

from skimage import color
from skimage import filters
from skimage import img_as_ubyte
from skimage import util


DEBUG_DIR = "results/debug"


def create_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    os.makedirs(path)


def vanish_image(img,local_area,offset,ret,size,invert=False):
    gray_scale_image = color.rgb2gray(img)
    if invert:
        gray_scale_image = util.invert(gray_scale_image)
    val = filters.threshold_local(gray_scale_image,local_area,mode="wrap",offset=offset)
    ret[size] = (gray_scale_image>val)
    #return (gray_scale_image > val)




def do_fragmentation(file_path, debug = True):
    file_ops.create_clean_dir(DEBUG_DIR)

    # load source image
    src_img = cv2.imread(file_path);
    src_img = deskew_image(src_img)

    #src_img = cv2.resize(src_img, (0, 0), fx = 4, fy = 4)
    cv2.imwrite(("%s/a0 scaled.png" % DEBUG_DIR), src_img)
  
    manager=Manager()
    imgs=manager.dict()
    p1=Process(target=vanish_image,args=(src_img,201,0.2,imgs,"clean"))
    p2=Process(target=vanish_image,args=(src_img,101,0.04,imgs,"noisy"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    clean_img=img_as_ubyte(imgs["clean"])
    src_img=img_as_ubyte(imgs["noisy"])
    #clean_img = img_as_ubyte(vanish_image(src_img,201,0.2))
    #src_img = img_as_ubyte(vanish_image(src_img,101,0.04))
    
    cv2.imwrite(("%s/a1 vainshed.png" % DEBUG_DIR), src_img)
    cv2.imwrite(("%s/a1 clean.png" % DEBUG_DIR), clean_img)

    # Find the contours
    _, contours, hierarchy = cv2.findContours(src_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    count = 0
    chars = []
    print 'Number of contures', len(contours)
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        try:
            x, y, w, h = cv2.boundingRect(cnt)

            # Create meta file
            char = {'x': x, 'y': y, 'w': w, 'h': h, 'id': count}

            chars.append(char)
            count += 1
        except ValueError, ve:
            if debug:
                traceback.print_exc(file=sys.stdout)
                print "skip fragment:", ve
    
    full_h, full_w = src_img.shape
    
    return chars, full_w, full_h, clean_img, src_img


if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print ("Invalid argument: <source file>")
