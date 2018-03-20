import numpy as np
import math
import cv2
from . import train
from scipy import ndimage

DEBUG_DIR = "results/debug"
def create_blank_image(width=64, height=64, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


def create_image_for_recognize(image, width=64, height=64):
    generated_image = np.zeros((height, width))#, np.float32 
    (image_h, image_w) = image.shape
    index_w = (width - image_w) / 2
    index_h = (height - image_h) / 2
    height = int(math.floor(height))
    width = int(math.floor(width))
    index_h = int(math.floor(index_h))
    index_w = int(math.floor(index_w))
    image_h = int(math.floor(image_h))
    image_w = int(math.floor(image_w))
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
        crop_img = np.zeros((64, 64), np.uint8)
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

    # Shrink if cropped image is oversized
    if h > 64 or w > 64 or h < 20 or w < 20:
        crop_img = downscale_proportionally(crop_img, 45, 45)

    # define background image as large image
    result_img = create_blank_image()

    ndimage.gaussian_filter(crop_img, 0.8, output=crop_img)

    # Convert image to 64x64
    image_to_recognize = create_image_for_recognize(crop_img)

    return image_to_recognize

def crop_all_char_images(chars, img_source):
    ndimage.gaussian_filter(img_source, 0.8, output=img_source)
    img_source = img_source / 255.0
    img_source = 1 - img_source
    crops = np.zeros((len(chars),64,64,1)) # FIXME: Static sizing
    for i in range(0, len(chars)):
        char = chars[i]
        x = char['x']
        y = char['y']
        w = char['w']
        h = char['h']

        crop_img = img_source[y:y + h, x:x + w]
        # Shrink if cropped image is oversized
        if h > 64 or w > 64 or h < 20 or w < 20:
            crop_img = downscale_proportionally(crop_img, 45, 45)

        result_img = create_blank_image()
        crop_img = create_image_for_recognize(crop_img)

        # Convert image to 64x64
        crop_img = crop_img.reshape((64, 64, 1))
        crop_img = np.expand_dims(crop_img, 0)

        crops[i] = crop_img

    return crops


