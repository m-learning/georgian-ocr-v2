import argparse
from PIL import Image
import numpy as np
from v2 import image_generator as ig
from v2 import network
from v2 import learning
import fragmenter
import os
import json

#-------------------------
import sys
import export_words
#-------------------------

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

def recognize_image(img_arr): #image_path):
    #img = Image.open(image_path)
    #print('IMAGE TYPE IS:', img)
    #img = img.convert("L")
    #array = np.asarray(img.getdata(), dtype=np.float32)
    img_arr /= 255.0 #array /= 255.0
    array = img_arr.reshape(learning.input_shape) #array.reshape(learning.input_shape)
    
    array = np.expand_dims(array, 0)#(array, 0)
    return recognize(array)


def write_meta_char(fragment_filename, char, score):
	meta_filename = os.path.join(fragmenter.META_DIR, fragment_filename)
	with open(meta_filename) as json_data:
		meta_obj = json.load(json_data)
		meta_obj['char'] = char
		meta_obj['score'] = score

		with open(meta_filename, 'w') as output_file:
			output_file.write(json.dumps(meta_obj))

if __name__ == '__main__':
    args = init_arguments()
    #print('================', args.image)
    image_arrays, meta_data = fragmenter.do_fragmentation(args.image)
    result = ''
    full_score = 0
    full_count = 0
    
    for (dir_path, dir_names, file_names) in os.walk(fragmenter.FRAGMENTS_DIR):
        meta_keys = sorted(meta_data.keys())
	for meta_key in meta_keys:
            #print('~~~~~~~~~~~~~~~~ ', file_name)
            img_arr = image_arrays[meta_key]
	    [char, score] = recognize_image(img_arr)#os.path.join(dir_path, file_name))
	    full_score += score
	    full_count += 1
            
	    print meta_key, char, score
	    #write_meta_char(file_name[:-4]+'.json', char, score)
            meta_data[meta_key]['char'] = char
	    meta_data[meta_key]['score'] = score

    print 'Avg score: %d' % (full_score * 100 /full_count)

    # --------------- text assembly -------------
    '''
    y = -1
    for key in sorted(meta_data.keys()):
      if meta_data[key]['y']+10 < y:
      else:
        end_char = '\n'
        end_char = ''
      y = meta_data[key]['y']
      #print(y)
      char = meta_data[key]['char']
      sys.stdout.write(char+end_char)
      #exp_test = export_words.test(meta_data)
    '''
    export_words.test(meta_data.values())

    
