import cv2
# import cv as cv2
import os
import sys
import numpy as np

DEBUG_DIR = "results/debug"

def create_dir_if_missing(path):
	if not os.path.exists(path):
		os.makedirs(path)


def do_segmentation(file_path):
	create_dir_if_missing(DEBUG_DIR)
	img = cv2.imread(file_path, 0)
	img2 = img

	ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

	kernel = np.ones((15, 15), np.uint8)

	img = cv2.fastNlMeansDenoising(img, None, 40, 40, 15)

	# img_erosion = cv2.erode(img, kernel, iterations=1)
	img = cv2.dilate(img, kernel, iterations=1)

	ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	im2, contours, hierarchy = cv2.findContours(img, 1, 2)

	for contour in contours:
		if cv2.contourArea(contour) < 1000:
			continue
		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(img2, [box], 0, (0, 0, 255), 2)

	cv2.imwrite(("%s/a1 gray.png" % DEBUG_DIR), img2)
	cv2.imwrite(("%s/a2 gray.png" % DEBUG_DIR), img)

if __name__ == "__main__":
	# source file path
	if len(sys.argv) > 1:
		source_file_path = sys.argv[1]
		do_segmentation(source_file_path)
	else:
		print ("Invalid argument: <source file>")
