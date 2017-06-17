import predict
import image_generator3 as ig
import argparse
import numpy as np

def init_arguments():
	parser = argparse.ArgumentParser(description='random image generator')
	parser.add_argument('text', metavar='text', type=str, nargs='+',
						help='text to generate.')
	parser.add_argument('-w', '--width', metavar='image_width', type=int,
						help='image width (64 is default)', default=64)
	parser.add_argument('--height', metavar='image_height', type=int,
						help='image width (64 is default)', default=64)
	parser.add_argument('-s', '--save_path', metavar='save_path', type=str, default='results/gen_img/test/',
						help='path to save generated images')
	return parser.parse_args()


if __name__ == '__main__':
	args = init_arguments()
	for word in args.text:
		img = ig.paint_text(word.decode('utf-8'), args.width, args.height, rotate=True, ud=True, multi_fonts=True, multi_sizes=True, save=False)
		img = np.expand_dims(img, 3)
		pred_char = predict.recognize(img)
		print (word.decode('utf-8') + ' : ' + pred_char)
