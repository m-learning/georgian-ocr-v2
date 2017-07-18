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

        pairs = recognize_image(img_arr)
        char = pairs[0]['char']
        score = pairs[0]['score'].item()

        meta_data["alternatives"]=[
          pairs[1], pairs[2]]

        full_score += score
        full_count += 1
        if debug:
            print meta_data['id'], char.encode('utf8'), score, pairs[1]['char'].encode('utf8'), pairs[1]['score'], pairs[2]['char'].encode('utf8'), pairs[2]['score']

        meta_data['char'] = char
        meta_data['score'] = score
    if debug:
        print 'Avg score: %d' % (full_score * 100 / full_count)

    read_text = export_words.export([n["meta"] for n in image_arrays])

    print read_text

    if correct_words:
        read_text = wr.correct_words(read_text)

    
    document = [[
     {'char':u'კ', 'score':0.91, 'alternatives':[{'char':u'ვ', 'score':0.35}, {'char':u'ზ', 'score':0.4}]},
     {'char':u'ა', 'score':0.91, 'alternatives':[{'char':u'ვ', 'score':0.35}, {'char':u'ზ', 'score':0.4}]},
     {'char':u'ც', 'score':0.91, 'alternatives':[{'char':u'ვ', 'score':0.35}, {'char':u'ზ', 'score':0.4}]},
     {'char':u'ზ', 'score':0.6, 'alternatives':[{'char':u'ი', 'score':0.35}, {'char':u'ზ', 'score':0.4}]}
    ]]

    document = [[
     {'char':u'კ', 'score':0.5, 'alternatives':[{'char':u'ძ', 'score':0.34}, {'char':u'ქ', 'score':0.04}]},
     {'char':u'თ', 'score':0.46, 'alternatives':[{'char':u'ო', 'score':0.38}, {'char':u'ი', 'score':0.07}]},
     {'char':u'შ', 'score':0.77, 'alternatives':[{'char':u'უ', 'score':0.12}, {'char':u'ფ', 'score':0.02}]},
     {'char':u'მ', 'score':0.86, 'alternatives':[{'char':u'შ', 'score':0.06}, {'char':u'ძ', 'score':0.04}]},
     {'char':u'ა', 'score':0.90, 'alternatives':[{'char':u'ბ', 'score':0.01}, {'char':u'ყ', 'score':0.01}]},
     {'char':u'რ', 'score':0.78, 'alternatives':[{'char':u'ი', 'score':0.07}, {'char':u'ჩ', 'score':0.06}]},
     {'char':u'ი', 'score':0.56, 'alternatives':[{'char':u'0', 'score':0.27}, {'char':u'ჩ', 'score':0.1}]},
     {'char':u'ძ', 'score':0.58, 'alternatives':[{'char':u'"', 'score':0.06}, {'char':u'*', 'score':0.05}]}
    ]]
    print wr.correct_words_with_scores(document)

    print read_text
    return read_text


if __name__ == '__main__':
    args = init_arguments()
    read(args.image, args.correct_words, args.debug)
