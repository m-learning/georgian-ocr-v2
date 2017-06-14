import argparse
from PIL import Image
import numpy as np
from v2 import image_generator as ig
from v2 import network
from v2 import learning
import fragmenter
import os
import json

import export_words

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
    #print type(img)
    #img = img.convert("L")
    #test_array = np.asarray(img.getdata(), dtype=np.float32)
    #test_array /= 255.0
    # -------------------------
    #img_arr[img_arr > ]=255.
    img_arr /= 255.0 #array /= 255.0
    array = img_arr.reshape(learning.input_shape)
    
    array = np.expand_dims(array, 0)
    return recognize(array)

if __name__ == '__main__':
    args = init_arguments()
    image_arrays = fragmenter.do_fragmentation(args.image)

    result = ''
    full_score = 0
    full_count = 0
    
    for n in image_arrays:
        img_arr = n["arr"]
        meta_data = n["meta"]
        img_arr = img_arr.flatten()
	[char, score] = recognize_image(img_arr)
        full_score += score
	full_count += 1
        print meta_data, char, score
        meta_data['char'] = char
	meta_data['score'] = score
            
    print 'Avg score: %d' % (full_score * 100 /full_count)
    

    # ----- for testing --------
    # use export_word as a module
    export_words.test([n["meta"] for n in image_arrays])
