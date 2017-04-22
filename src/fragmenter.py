import random
import cv2
# import cv as cv2
import math
import os
import sys
import numpy as np


# destination directory
FRAGMENTS_DIR = "results/words"


def do_fragmentation(file_path):

    if not os.path.exists(FRAGMENTS_DIR):
        os.makedirs(FRAGMENTS_DIR)
    # load source image
    src_img = cv2.imread(file_path)

    # convert to grayscale
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    gray = cv2.medianBlur(gray, 5)

    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps
    thresh = cv2.dilate(thresh, None, iterations=3)
    thresh = cv2.erode(thresh, None, iterations=2)

    # Find the contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    # For each contour, find the bounding rectangle and crop it.
    # put cropped image on a blank background and write to disk
    for cnt in contours:
        count += 1
        try:
            crop_rectangle(src_img, cnt, FRAGMENTS_DIR + "/" + str(count) + ".png")
        except ValueError:
            print ("skip fragment")

        # text = ''
        # # read images and predict text
        # for index in range(count):
        #     img = cv2.imread(destination_dir + "/" + str(index + 1) + ".png")
        #     text += recognize_image(img) + ' '
        # text_file = open("result.txt", "w")
        # text_file.write(text)
        # text_file.close()


# read existing words
# words = []
# words_file = open('data/words', 'r')
# content = words_file.read()
# lines = content.split('\n')
# for line in lines:
#     if line:
#         words.append(line)

def create_blank_image(width=128, height=64, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)
    
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color
    
    return image


def crop_rectangle(img, contour, file_name):
    x,y,w,h = cv2.boundingRect(contour)
    
    crop_img = img[y:y+h, x:x+w]
    
    # define background image as large image 
    result_img = create_blank_image()

    # define small height and width
    s_height, s_width = crop_img.shape[:2]
    
    # define large height and width
    l_height, l_width = result_img.shape[:2]

    y_offset = int(math.floor((l_height - s_height) / 2))
    x_offset = int(math.floor((l_width - s_width) / 2))

    result_img[y_offset:y_offset + s_height, x_offset:x_offset + s_width] = crop_img

    cv2.imwrite(file_name, result_img)

if __name__ == "__main__":
    # source file path
    if len(sys.argv) > 1:
        source_file_path = sys.argv[1]
        do_fragmentation(source_file_path)
    else:
        print ("Invalid argument: <source file>")
