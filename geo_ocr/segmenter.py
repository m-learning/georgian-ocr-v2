import cv2
import os
import sys
import numpy as np

DEBUG_DIR = "results/debug"

DILATE_ITERATIONS =20 


def calculate_image_roughness(img):
	# todo calculate text roughness in image
	return 1


def get_dilate_iterations(roughness):
	# todo calculate iteration number based on roughness
	return DILATE_ITERATIONS


def create_dir_if_missing(path):
	if not os.path.exists(path):
		os.makedirs(path)


def vanish_image(img):
	img = cv2.bilateralFilter(img, 50, 40, 40)
	# val = filters.threshold_li(gray)
	kernel = np.ones((2, 2), np.float32) / 10
	img = cv2.filter2D(img, -1, kernel)
	img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
	return img


def dilate_image(img):
	kernel = np.ones((4, 4), np.uint8)
	img = cv2.fastNlMeansDenoising(img, None, 40, 40, 15)
	roughness = calculate_image_roughness(img)
	img = cv2.dilate(img, kernel, iterations=get_dilate_iterations(roughness))
	ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
	return img


def find_contours(img, original_img):
	im2, contours, hierarchy = cv2.findContours(img, 1, 2)
	cont = []
	for contour in contours:
		if cv2.contourArea(contour) < 1000:
			continue
		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(original_img, [box], 0, (0, 0, 255), 2)
		cont.append(contour)
	return cont, original_img


def do_segmentation(img):
	create_dir_if_missing(DEBUG_DIR)
	#img = cv2.imread(file_path, 0)
	original_img = img

	img = vanish_image(img)

	img = dilate_image(img)

	contours, original_img = find_contours(img, original_img)

	cv2.imwrite(("%s/a1 segment.png" % DEBUG_DIR), original_img)
	cv2.imwrite(("%s/a2 segment.png" % DEBUG_DIR), img)


if __name__ == "__main__":
	# source file path
	if len(sys.argv) > 1:
		source_file_path = sys.argv[1]
		do_segmentation(source_file_path)
	else:
		print ("Invalid argument: <source file>")
