# -*- coding: utf-8 -*-
import os
import cv2
from .predict_all import *
from . import word_corrector as wc
from . import filter
from . import segmenter
from . import vanish
import sys
#import matplotlib.pyplot as plt
import timeit
from . import image_operations as image_ops
from . import file_operations as file_ops
from . import merge_symbols as ms
from . import char_operations as char_ops
import json
from . import convert

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


def line_debugger(lines, vanished_img):
    file_ops.create_clean_dir('results/lines')
    counter = 1
    for i in lines:
        chars = []
        for each in i:
            chars.append(each)
        image = restore_image(chars, vanished_img)
        cv2.imwrite(('results/lines/%s.jpg' % counter), image)
        counter += 1


def print_symbols(lines, vanished_img):
    for i in lines:
        for each in i:
            new_each = image_ops.crop_char_image(ms.converter(each), vanished_img)
            cv2.imwrite(("%s/%s.png" % (LETTERS_DIR, each['id'])), new_each)


def read(image_path, correct_words=False, debug=True, to_pdf=False):
    overall_time = timeit.default_timer()
    file_ops.create_clean_dir(LETTERS_DIR)

    # load source image
    src_img = cv2.imread(image_path)
    
    if not os.path.isfile(image_path):
        print("Files does not exists")
        return
    
    
    vanished_img,clean_img,clean_small_img=vanish.vanish_img(src_img)

    segments=segmenter.do_segmentation(clean_small_img)
    
    print (segments)    

    cv2.imwrite('results/debug/clean_small.png', clean_small_img)
    
    #chars, full_w, full_h, clean_img, vanished_img = fragmenter.do_fragmentation(src_img, debug=debug)
    chars, full_w, full_h =  fragmenter.do_fragmentation(vanished_img, debug=debug)
    # TODO: Line detector

    print (len(chars), 'chars exist')

    chars = filter.filter_background(chars, full_w, full_h)
    # chars = filter.filter_overlaps(chars)
    other_chars = filter.filter_compare(chars, clean_img)
    chars = filter.filter_unproportional(chars)

    # TODO: Fix for images without noise
    chars = filter.filter_by_size_distribution(chars, full_w, full_h)

    # merge filters
    chars = filter.filter_merge(chars, other_chars)
    chars = filter.filter_overlaps(chars)
    chars = filter.filter_too_small(chars)

    # detect % ? ! : symbols
    # chars = sorted(chars, key=lambda k: k['x'])

    print (len(chars), 'chars left after filtering')


    #crops = image_ops.crop_all_char_images(chars, vanished_img)
    #print('crops ----------------------------------------', crops)

    # if you want to see filtered image uncomment next 4 lines
    # restored_image = restore_image(chars, full_h, full_w)
    # plt.imshow(restored_image)
    # cv2.imwrite('/home/shota/image.png', restored_image)
    # plt.show()
    full_score = 0
    full_count = 0

    recognize_time = timeit.default_timer()
    recognized_chars = []

    pairs = recognize_chars(chars, vanished_img)

    only_recognize_time = 0
    for i in range(0, len(pairs)):
        pair = pairs[i]
        char = chars[i]
        #try:
        #    char_img = image_ops.crop_char_image(char, vanished_img)
        #except Exception, e:
        #    print "Could not crop image:", e
        #    continue

        #flattened = char_img.flatten()

        #only_recognize_time_frag = timeit.default_timer()
        #pairs = recognize_image(flattened)
        #only_recognize_time += timeit.default_timer()-only_recognize_time_frag

        char['char'] = pair[0]['char']
        char['score'] = pair[0]['score'].item()
        char["alternatives"] = [pair[1], pair[2], pair[3]]

        full_score += char['score']
        full_count += 1

        recognized_chars.append(char)

        if debug:
            print (char['id'], char['char'], char['score'], pairs[1]['char'], pairs[1]['score'], pairs[2]['char'], pairs[2]['score'], str(char['w'])+'x'+str(char['h']))

        # if debug:
        #     cv2.imwrite(("%s/%s.png" % (LETTERS_DIR, char['id'])), char_img)

    if debug:
        print ('Avg score: %d' % (full_score * 100 / full_count))

    recognize_time = timeit.default_timer()-recognize_time
    
    print('Recognize time: '+str(recognize_time))
    print('Only Recognize time: '+str(only_recognize_time))
    start_time = timeit.default_timer()
    
    chars = recognized_chars
    
    # chars = filter.filter_by_weights(chars)
    chars = filter.filter_by_possible_alternatives(chars)
    chars = filter.filter_out_of_average(chars)
    
    lines, avg_width, avg_height = export_words.export_lines(chars)
    read_text = u''
    # detect ? ! : ; % symbols
    ms.merge(lines, vanished_img)

    lines = export_words.addspaces(lines, avg_width)
    print ('xazebis raodenoba: ', len(lines))
   
    changed=True
    while(changed):
        lines,changed=filter.filter_out_of_line(lines)
    # lines=filter.filter_out_of_line(lines)

    if debug:
        line_debugger(lines, vanished_img)
        print_symbols(lines, vanished_img)

    word_lines = char_ops.group_meta_as_words(lines)

    #word_lines = char_ops.merge_split_words(word_lines)
    
    
    if correct_words:
        read_text = wc.correct_words_with_scores(word_lines)
    else: read_text = char_ops.word_lines_to_text(word_lines)
    
    print (read_text)
    
    restored_image = restore_image(chars, vanished_img)
    cv2.imwrite('results/debug/filtered.png', restored_image)
    
    print ("overall time: "+str(timeit.default_timer()-overall_time))

    if to_pdf:
        rewrited = []
        for line in word_lines:
            reline = []
            for word in line:
                reword = []
                for char in word:
                    #print ('x-w:', char['w'])
                    #print ('x-h:', char['h'])
                    #print ('x-x:', char['x'])
                    #print ('x-y:', char['y'])
                    #print ('x-char:', char['char'])
                    reword.append(
                        {
                            'w': char['w'],
                            'h': char['h'],
                            'x': char['x'],
                            'y': char['y'],
                            'lh': char['lh'],
                            'char': char['char']
                        }
                    )
                reline.append(reword)
            rewrited.append(reline)
            
        convert.topdf(image_path, rewrited)
        with open('/tmp/data.json', 'w') as f:
            json.dump(rewrited, f, sort_keys=True, indent=4, ensure_ascii=True)

    return read_text 
    
    

def read_for_tdc(image_path, debug=False):
    overall_time = timeit.default_timer()
    file_ops.create_clean_dir(LETTERS_DIR)

    if not os.path.isfile(image_path):
        print("Files does not exists")
        return

    chars, full_w, full_h, clean_img, vanished_img = fragmenter.do_fragmentation(image_path, debug=debug)

    print (len(chars), 'chars exist')

    chars = filter.filter_background(chars, full_w, full_h)
    other_chars = filter.filter_compare(chars, clean_img)
    chars = filter.filter_unproportional(chars)

    chars = filter.filter_by_size_distribution(chars, full_w, full_h)

    # merge filters
    chars = filter.filter_merge(chars, other_chars)
    chars = filter.filter_overlaps(chars)
    chars = filter.filter_too_small(chars)

    print (len(chars), 'chars left after filtering')    

    full_score = 0
    full_count = 0

    recognize_time = timeit.default_timer()
    recognized_chars = []
    for char in chars:
        try:
            char_img = image_ops.crop_char_image(char, vanished_img)
        except Exception as e:
            print ("Could not crop image:", e)
            continue

        pairs = recognize_image(char_img.flatten())
        char['char'] = pairs[0]['char']
        char['score'] = pairs[0]['score'].item()
        char["alternatives"] = [pairs[1], pairs[2], pairs[3]]

        full_score += char['score']
        full_count += 1

        recognized_chars.append(char)

        if debug:
            print (char['id'], char['char'], char['score'], pairs[1]['char'], pairs[1]['score'], pairs[2]['char'], pairs[2]['score'], str(char['w'])+'x'+str(char['h']))

    if debug:
        print ('Avg score: %d' % (full_score * 100 / full_count))
    recognize_time = timeit.default_timer()-recognize_time
    start_time = timeit.default_timer()
    
    chars = recognized_chars
    
    chars = filter.filter_by_possible_alternatives(chars)
    
    lines, avg_width, avg_height = export_words.export_lines(chars)
    ms.merge(lines, vanished_img)

    lines = export_words.addspaces(lines, avg_width)
    print ('xazebis raodenoba: ', len(lines))
   
    changed=True
    while(changed):
        lines,changed=filter.filter_out_of_line(lines)
    
    result = []
    
    for chars in lines:
        for char in chars:
            try:
                if char['char'] == u' ':
                    result.append({
                        'char': 'space',
                        'char_img': None 
                    })
                    continue
                char_img = image_ops.crop_char_image(char, vanished_img)
                result.append({
                    'char': char['char'],
                    'char_img': char_img
                })
            except Exception as e:
                print ("Could not crop image:", e)
                continue
        result.append({
            'char': 'newline',
            'char_img': None
        })

    if debug:
        line_debugger(lines, vanished_img)
        print_symbols(lines, vanished_img)

    restored_image = restore_image(chars, vanished_img)
    cv2.imwrite('results/debug/filtered.png', restored_image)
    
    print ("overall time: "+str(timeit.default_timer()-overall_time))
    return result

if __name__ == '__main__':
    args = init_arguments()
    read(args.image, args.correct_words, args.debug, args.pdf)
