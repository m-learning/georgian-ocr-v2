# -*- coding: utf-8 -*-
import os
import cv2
from predict_all import *
import word_corrector as wc
import filter
import sys
import matplotlib.pyplot as plt
import timeit
import image_operations as image_ops
import file_operations as file_ops

LETTERS_DIR = "results/letters"


def restore_image(chars, original_image):
    full_h, full_w = original_image.shape

    image = np.zeros((full_h, full_w, 3), np.uint8)
    color = tuple(reversed((255, 255, 255)))
    image[:] = color
    for ch in chars:
        x = ch['x']
        y = ch['y']
        w = ch['w']
        h = ch['h']
        original_crop = original_image[y:y + h, x:x + w]
        new_ch = cv2.cvtColor(original_crop, cv2.COLOR_GRAY2BGR)
        image[ch['y']:ch['y']+new_ch.shape[0], ch['x']:ch['x']+new_ch.shape[1]] = new_ch

    return image


def read(image_path, correct_words=False, debug=True):
    overall_time = timeit.default_timer()
    file_ops.create_clean_dir(LETTERS_DIR)

    if not os.path.isfile(image_path):
        print("Files does not exists")
        return
    
    chars, full_w, full_h, clean_img, vanished_img = fragmenter.do_fragmentation(image_path, debug=debug)
    # TODO: Line detector

    print len(chars), 'chars exist'
    
    chars = filter.filter_background(chars, full_w, full_h)
    #chars = filter.filter_overlaps(chars)
    other_chars= filter.filter_too_small(chars)
    other_chars=filter.filter_compare(chars,clean_img)
    chars = filter.filter_unproportional(chars)
    
    # TODO: Fix for images without noise
    chars = filter.filter_by_size_distribution(chars, full_w, full_h)
    #chars = filter.filter_out_of_average(chars)

    #merge filters
    chars=filter.filter_merge(chars,other_chars)
    chars = filter.filter_overlaps(chars)
    
    print len(chars), 'chars left after filtering'
    #if you want to see filtered image uncomment next 4 lines
    #restored_image = restore_image(chars, full_h, full_w)
    #plt.imshow(restored_image)
    #cv2.imwrite('/home/shota/image.png', restored_image)
    #plt.show()
    full_score = 0
    full_count = 0

    recognize_time = timeit.default_timer()
    for char in chars:
        char_img = image_ops.crop_char_image(char, vanished_img)
        pairs = recognize_image(char_img.flatten())
        char['char'] = pairs[0]['char']
        char['score'] = pairs[0]['score'].item()
        char["alternatives"]=[pairs[1], pairs[2], pairs[3]]

        full_score += char['score']
        full_count += 1
        if debug:
            print char['id'], char['char'], char['score'], pairs[1]['char'], pairs[1]['score'], pairs[2]['char'], pairs[2]['score'], str(char['w'])+'x'+str(char['h'])
        
        if debug:
            cv2.imwrite(("%s/%s.png" % (LETTERS_DIR, char['id'])), char_img)

    if debug:
        print 'Avg score: %d' % (full_score * 100 / full_count)
    recognize_time=timeit.default_timer()-recognize_time

    start_time = timeit.default_timer()
    #chars = filter.filter_by_weights(chars)
    chars = filter.filter_by_possible_alternatives(chars)
    
    read_text, lines, avg_width, avg_height = export_words.export(chars)

    #lines = filter.filter_outsized(lines, avg_width, avg_height)

    print read_text

    if correct_words:
      read_text = wc.correct_words_with_scores(lines)

    print read_text
    
    restored_image = restore_image(chars, vanished_img)
    cv2.imwrite('results/debug/filtered.png', restored_image)

    print "overall time: "+str(timeit.default_timer()-overall_time)
    return read_text


if __name__ == '__main__':
    args = init_arguments()
    read(args.image, args.correct_words, args.debug)
