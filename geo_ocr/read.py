# -*- coding: utf-8 -*-
import os
from predict_all import *
import word_corrector as wc
import filter
import sys


def restore_image(chars, w, h):
    image = np.zeros((h, w, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    
    for ch in chars:
        # TODO: Print into image
        pass


def read(image_path, correct_words=False, debug=True):
    if not os.path.isfile(image_path):
        print("Files does not exists")
        return

    chars, full_w, full_h = fragmenter.do_fragmentation(image_path, debug=debug)

    # TODO: Line detector

    print len(chars), 'chars exist'

    chars = filter.filter_background(chars, full_w, full_h)
    chars = filter.filter_overlaps(chars)
#    chars = filter.filter_too_small(chars)
    chars = filter.filter_unproportional(chars)

    # TODO: Fix for images without noise
    chars = filter.filter_by_size_distribution(chars, full_w, full_h)
    #chars = filter.filter_out_of_average(chars)

    print len(chars), 'chars left after filtering'

    full_score = 0
    full_count = 0

    for char in chars:
        pairs = recognize_image(char['image'].flatten())
        char['char'] = pairs[0]['char']
        char['score'] = pairs[0]['score'].item()
        char["alternatives"]=[pairs[1], pairs[2], pairs[3]]

        full_score += char['score']
        full_count += 1
        if debug:
            print char['id'], char['char'], char['score'], pairs[1]['char'], pairs[1]['score'], pairs[2]['char'], pairs[2]['score'], str(char['w'])+'x'+str(char['h'])

    if debug:
        print 'Avg score: %d' % (full_score * 100 / full_count)

    
    chars = filter.filter_by_weights(chars)
    chars = filter.filter_by_possible_alternatives(chars)

    read_text, lines, avg_width, avg_height = export_words.export(chars)

    #lines = filter.filter_outsized(lines, avg_width, avg_height)

    print read_text

    if correct_words:
      read_text = wc.correct_words_with_scores(lines)

    print read_text
    return read_text
    

if __name__ == '__main__':
    args = init_arguments()
    read(args.image, args.correct_words, args.debug)
