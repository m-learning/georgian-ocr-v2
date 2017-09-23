import numpy as np
import math
import cv2
from scipy import ndimage

def create_blank_image(width=64, height=64, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


def create_image_for_recognize(image, width=64, height=64):
    generated_image = np.ones((height, width), np.float32) * 255
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

    crop_img = cv2.resize(image, (0, 0), fx = downscale_ratio, fy = downscale_ratio)
    return crop_img


def crop_char_image(char, img):
    x = char['x']
    y = char['y']
    w = char['w']
    h = char['h']

    #TODO: test me !!!
    # copy_img = img.copy()
    #
    # mask1 = np.zeros(img.shape, np.uint8)
    # mask1.fill(255)
    #
    # mask2 = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
    #
    # a = cv2.drawContours(mask1, char['contours'], -1, (0, 255, 0), 1)
    # cv2.imwrite('contour.png', a)
    # cv2.floodFill(mask1, mask2, (0, 0), 0)
    # cv2.imwrite('invert.png', mask1)
    # im_inv = cv2.bitwise_not(copy_img)
    # final = cv2.bitwise_not(cv2.bitwise_and(a, im_inv))
    # cv2.imwrite('final.png', final)

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

    ndimage.gaussian_filter(crop_img, 0.8, output=crop_img)

    # Convert image to 64x64
    image_to_recognize = create_image_for_recognize(crop_img)

    return image_to_recognize




def crop_seg_image(seg, img):
    x = seg['x']
    y = seg['y']
    w = seg['w']
    h = seg['h']


    crop_img = img[y:y + h, x:x + w]

    # define small height and width
    #s_height, s_width = crop_img.shape[:2]

    # Shrink if cropped image is oversized
    #if s_height > 64 or s_width > 64 or s_height < 20 or s_width < 20:
    #    crop_img = downscale_proportionally(crop_img, 45, 45)

    # define background image as large image
    #result_img = create_blank_image()

    # define large height and width
    #l_height, l_width = result_img.shape[:2]

    #ndimage.gaussian_filter(crop_img, 0.8, output=crop_img)

    # Convert image to 64x64
    #image_to_recognize = create_image_for_recognize(crop_img)

    return crop_img

