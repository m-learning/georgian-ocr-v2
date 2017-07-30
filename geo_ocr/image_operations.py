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

    try:
      crop_img = cv2.resize(image, (0, 0), fx = downscale_ratio, fy = downscale_ratio)
    except Exception, e:
      print "Could not downscale image", e
      crop_img = image
    return crop_img


def crop_char_image(char, img):
    x = char['x']
    y = char['y']
    w = char['w']
    h = char['h']

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
