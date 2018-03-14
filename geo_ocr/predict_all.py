import argparse
import numpy as np
import image_generator as ig
import network
import train
import fragmenter
import os
import image_operations as image_ops

import export_words

model = None


def init_arguments():
    parser = argparse.ArgumentParser(description='Georgian OCR')
    parser.add_argument('-i', '--image', metavar='image_path', type=str,
                        help='Path to the image to recognize.')
    parser.add_argument('-w', '--correct-words', 
                        help='To use elasticsearch for correcting words.',
                        action='store_true')
    parser.add_argument('-d', '--debug',
                        help='Debug mode. Show logs and dump images.',
                        action='store_true')
    parser.add_argument('-p', '--pdf',
                        help='export as pdf file.',
                        action='store_true')
    return parser.parse_args()


def choose_char(scores, chars):
    pairs = []
    for i in range(0, len(scores)):
        pairs.append({'char': chars[i], 'score': scores[i]})
    pairs = sorted(pairs, key=lambda pair: pair['score'], reverse=True)

    return [pairs[0], pairs[1], pairs[2], pairs[3]]


def recognize(array):
    path = os.getcwd()
    array = 1 - array
    global model

    if model is None:
        model = network.init_model(ig.LABEL_SIZE, train.input_shape)
        model.load_weights(os.path.join(path, 'results/data/model.h5'))

    pred = model.predict(array, batch_size=5, verbose=0)
    return choose_char(pred[0], ig.chars)


def recognize_image(img_arr):
    img_arr /= 255.0
    array = img_arr.reshape(train.input_shape)

    array = np.expand_dims(array, 0)
    return recognize(array)

def recognize_chars(chars, image):
    char_images = image_ops.crop_all_char_images(chars, image)
    #print(char_images)

    global model
    path = os.getcwd()

    if model is None:
        model = network.init_model(ig.LABEL_SIZE, train.input_shape)
        model.load_weights(os.path.join(path, 'results/data/model.h5'))

    pred = model.predict(char_images, batch_size=len(chars), verbose=0)

    #print choose_char(pred[0], ig.chars)[0]['char']
    #print choose_char(pred[1], ig.chars)[0]['char']

    chars = []
    for p in pred:
        chars.append(choose_char(p, ig.chars))

    return chars


if __name__ == '__main__':
    args = init_arguments()
    image_arrays = fragmenter.do_fragmentation(args.image, debug=args.debug)

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
        if args.debug:
            print (meta_data, char.encode('utf8'), score)
        meta_data['char'] = char
        meta_data['score'] = score
    if args.debug:
        print ('Avg score: %d' % (full_score * 100 / full_count))

    # ----- for testing --------
    # use export_word as a module
    export_words.test([n["meta"] for n in image_arrays])
