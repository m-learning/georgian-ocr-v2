import argparse
from PIL import Image
import numpy as np
import image_generator as ig
import network
import learning

model = None


def init_arguments():
	parser = argparse.ArgumentParser(description='Georgian OCR')
	parser.add_argument('-i', '--image', metavar='image_path', type=str,
	                    help='Path to the image to recognize.')
	return parser.parse_args()


def recognize_image(image_path):
	img = Image.open(image_path)
	img = img.convert("L")
	array = np.asarray(img.getdata(), dtype=np.float32)
	array /= 255.0
	array = array.reshape(learning.input_shape)

	array = np.expand_dims(array, 0)
	return recognize(array)


def recognize(array):
	array = 1 - array
	global model

	if model is None:
		model = network.init_model(ig.LABEL_SIZE, learning.input_shape)
		model.load_weights('results/data/model.h5')

	print model.predict(array, batch_size=1, verbose=0)

	pred = model.predict_classes(array, batch_size=1, verbose=0)
	ch = ig.chars[pred[0]]
	return ch


if __name__ == '__main__':
	args = init_arguments()
	char = recognize_image(args.image)
	print(char)
