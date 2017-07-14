# -*- coding: utf-8 -*-
import os
from predict_all import *
import word_corrector as wr


def read(image_path, correct_words=False, debug=True):
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
        [char, score] = recognize_image(img_arr)
        full_score += score
        full_count += 1
        if debug:
            print meta_data, char.encode('utf8'), score
        meta_data['char'] = char
        meta_data['score'] = score
    if debug:
        print 'Avg score: %d' % (full_score * 100 / full_count)

    read_text = export_words.export([n["meta"] for n in image_arrays])

    if correct_words:
      read_text = wr.correct_words(read_text)

    print read_text
    return read_text


if __name__ == '__main__':
    args = init_arguments()
    read(args.image, args.correct_words, args.debug)
