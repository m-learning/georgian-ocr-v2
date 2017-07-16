import os
from predict_all import *


def read(image_path, debug=True):
	if not os.path.isfile(image_path):
		print("Files does not exists")
		return

	image_arrays = fragmenter.do_fragmentation(image_path, debug=debug)
	full_score = 0
	full_count = 0

	for n in image_arrays:
		img_arr = n["arr"]
		meta_data = n["meta"]
		img_arr = img_arr.flatten()
		print meta_data['id'], get_nearest(n, image_arrays)
		continue
		[char, score] = recognize_image(img_arr)
		full_score += score
		full_count += 1
		if debug:
			print meta_data, char.encode('utf8'), score
		meta_data['char'] = char
		meta_data['score'] = score
	if debug:
		print 'Avg score: %d' % (full_score * 100 / full_count)

	# ----- for testing --------
	# use export_word as a module
	export_words.test([n["meta"] for n in image_arrays])


def get_nearest(image, image_arrays, n=4):
	distances = []
	for im in image_arrays:
		if im is image:
			continue
		distances.append((calculate_distance(image, im), im['meta']))
	sorted_distances = sorted(distances, key=lambda dist: dist[0])[:n]

	return [get_frame(image['meta'], im) for (d, im) in sorted_distances]


def get_frame(meta1, meta2):
	top = min(meta1['y'], meta2['y'])
	right = min(meta1['x'] + meta1['w'], meta2['x'] + meta2['w'])
	bottom = min(meta1['y'] + meta1['h'], meta2['y'] + meta2['h'])
	left = min(meta1['x'], meta2['x'])
	return [top, right, bottom, left]


def calculate_distance(im1, im2):
	meta1, meta2 = im1["meta"], im2["meta"]
	x1, y1, = meta1['x'] + meta1['w'] / 2, meta1['y'] + meta1['h'] / 2
	x2, y2 = meta2['x'] + meta2['w'] / 2, meta2['y'] + meta2['h'] / 2
	return pow(x1 - x2, 2) + pow(y1 - y2, 2)


if __name__ == '__main__':
	args = init_arguments()
	read(args.image, args.debug)
