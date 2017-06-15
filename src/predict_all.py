import argparse
from PIL import Image
import numpy as np
from v2 import image_generator as ig
from v2 import network
from v2 import learning
import fragmenter as f
import os
import json

model = None


def init_arguments():
  parser = argparse.ArgumentParser(description='Georgian OCR')
  parser.add_argument('-i', '--image', metavar='image_path', type=str,
    help='Path to the image to recognize.')
  return parser.parse_args()

def choose_char(scores, chars):
  pairs = []
  for i in range(0, len(scores)):
    pairs.append({ 'char': chars[i], 'score': scores[i] })

  pairs = sorted(pairs, key=lambda pair: pair['score'], reverse=True)

  return pairs[0]['char'], pairs[0]['score'].item()
    

def recognize(array):
	array = 1 - array
	global model

	if model is None:
		model = network.init_model(ig.LABEL_SIZE, learning.input_shape)
		model.load_weights('results/data/model.h5')

	pred = model.predict(array, batch_size=1, verbose=0)
	return choose_char(pred[0], ig.chars)

def recognize_image(image_path):
	img = Image.open(image_path)
	img = img.convert("L")
	array = np.asarray(img.getdata(), dtype=np.float32)
	array /= 255.0
	array = array.reshape(learning.input_shape)

	array = np.expand_dims(array, 0)
	return recognize(array)


def write_meta_char(fragment_filename, char, score):
	meta_filename = os.path.join(f.META_DIR, fragment_filename)
	with open(meta_filename) as json_data:
		meta_obj = json.load(json_data)
		meta_obj['char'] = char
		meta_obj['score'] = score

		with open(meta_filename, 'w') as output_file:
			output_file.write(json.dumps(meta_obj))

if __name__ == '__main__':
	args = init_arguments()

	f.do_fragmentation(args.image)
	result = ''
	full_score = 0
	full_count = 0
	
	for (dir_path, dir_names, file_names) in os.walk(f.FRAGMENTS_DIR):
		file_names = sorted(file_names)
		for file_name in file_names:
			[char, score] = recognize_image(os.path.join(dir_path, file_name))
			full_score += score
			full_count += 1

			print file_name, char.encode('utf8'), score
			write_meta_char(file_name[:-4]+'.json', char, score)
	print 'Avg score: %d' % (full_score * 100 /full_count)

