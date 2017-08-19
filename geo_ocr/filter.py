import os
import sys
import numpy as np

LETTERS_PATH = "results/letters"

def filter_unproportional(chars):
    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        ratio = float(ch['w'])/ch['h']
        if ratio < 0.2 or ratio > 3.0:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename) 
        else:
            resulting_chars.append(ch)

    print 'Number of unproportional parts removed', num_of_noise
    return resulting_chars


def filter_too_small(chars):
    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        if ch['w'] < 10 or ch['h'] < 10:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename)
        else:
            resulting_chars.append(ch)

    print 'Number of too small parts removed', num_of_noise
    return resulting_chars


def filter_out_of_average(chars):
    sum_w = 0
    sum_h = 0

    for ch in chars:
        sum_w += ch['w']
        sum_h += ch['h']

    len_chars = len(chars)
    avg_w = sum_w / len_chars
    avg_h = sum_h / len_chars

    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        if ch['w'] > avg_w * 15 or ch['h'] > avg_h * 15 or ch['w'] < avg_w / 15 or ch['h'] < avg_h / 15:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename)
        else:
            resulting_chars.append(ch)

    print 'Number of out of average parts removed', num_of_noise
    return resulting_chars


def filter_by_size_distribution_step(chars):
    # To remove chars with lowest width and heigth distribution
    min_w = sys.maxint
    min_h = sys.maxint
    max_w = 0
    max_h = 0

    for ch in chars:
        if ch['w'] < min_w:
            min_w = ch['w']
        if ch['h'] < min_h:
            min_h = ch['h']

        if ch['w'] > max_w:
            max_w = ch['w']
        if ch['h'] > max_h:
            max_h = ch['h']

    hist_size = 5
    width_hist = [0] * hist_size
    height_hist = [0] * hist_size
    width_delta = max_w - min_w
    height_delta = max_h - min_h

    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        w = ch['w']
        width_index = int(float(w - min_w)/width_delta*(hist_size-1))
        width_hist[width_index] += 1

        h = ch['h']
        height_index = int(float(h - min_h)/height_delta*(hist_size-1))
        height_hist[height_index] += 1

        if width_index < 1 or height_index < 1:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename)
        else:
            resulting_chars.append(ch)

    print 'Number of low occurence size parts removed', num_of_noise
    #print '---'
    print 'Width distribution histogram', width_hist
    print 'Height distribution histogram', height_hist
    #print '---'

    return resulting_chars


def filter_by_size_distribution(chars, full_w, full_h):
    num_of_too_small = 0
    for ch in chars:
        if ch['w'] < 10 or ch['h'] < 10:
            num_of_too_small += 1

    if not num_of_too_small:
        print 'Number of low occurence size parts removed', 0, 'There is no noise'
        return chars

    chars = filter_by_size_distribution_step(chars)

    return chars


def filter_by_edge_smoothness(chars):
    # TODO: Work on original image, not blurred
    return chars


def filter_by_weights(chars):
    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        if ch['score'] < 0.2:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename)
        else:
            resulting_chars.append(ch)

    print 'Number of parts removed because of low wight', num_of_noise
    return resulting_chars


def filter_by_possible_alternatives(chars):
    # TODO
    return chars


def filter_overlaps(chars):
    num_of_noise = 0
    resulting_chars = []
    for m1 in chars:
        removed = False
        for m2 in chars:
            if (m1['x'] > m2['x'] and
                  m1['y'] > m2['y'] and
                  m1['x']+m1['w'] < m2['x']+m2['w'] and
                  m1['y']+m1['h'] < m2['y']+m2['h']):

                num_of_noise += 1
                # TODO: Copy to debug dir with filter name
                imageFilename = "%s/%d.png" % (LETTERS_PATH, m1['id'])
                if os.path.isfile(imageFilename): os.remove(imageFilename)
                removed = True
                break
        if not removed:
            resulting_chars.append(m1)
                

    print 'Number of overlapped parts removed', num_of_noise
    return resulting_chars


def filter_background(chars, full_w, full_h):
    num_of_noise = 0
    resulting_chars = []
    for ch in chars:
        if (float(ch['w']) * ch['h']) / (full_w * full_h) > 0.9:
            num_of_noise += 1
            # TODO: Copy to debug dir with filter name
            imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
            if os.path.isfile(imageFilename): os.remove(imageFilename)
        else:
            resulting_chars.append(ch)

    print 'Number of backgrounds removed', num_of_noise
    return resulting_chars


#def filter_low_score

def filter_outsized(line_metas, avg_width, avg_height):
    num_of_noise = 0
    resulting_lines = []
    for line in line_metas:
        resulting_chars = []
        for ch in line:
#            print ch['id'], ch['h'], avg_height, avg_height*0.2
            if ch['w'] < avg_width*0.2 or ch['h'] < avg_height*0.2 or ch['h'] > avg_height*1.5:
                num_of_noise += 1
                # TODO: Copy to debug dir with filter name
                imageFilename = "%s/%d.png" % (LETTERS_PATH, ch['id'])
                if os.path.isfile(imageFilename): os.remove(imageFilename)
            else:
                resulting_chars.append(ch)

        resulting_lines.append(resulting_chars)
                
    print 'Number of outsized parts removed', num_of_noise
    return resulting_lines

def filter_compare(chars,clean_img):
    new_chars=[]
    count=0
    for char in chars:
        clean_letter=np.invert(np.array(clean_img[char["y"]:(char["y"]+char["h"]),
                 char["x"]:(char["x"]+char["w"])],dtype=bool))
        #print np.sum(clean_letter)/float(char["w"]*char["h"]),char["id"], np.sum(clean_letter)
        #print np.sum(clean_letter)/float((char["w"]*char["h"]))
        if (np.sum(clean_letter)/float(char["w"]*char["h"])>0.05):
            new_chars.append(char)
        else:
            count+=1
    print "Clean image compare filter: "+str(count)
    return new_chars

def filter_merge(chars_1,chars_2):
    for char_2 in chars_2:
        in_list=False
        for char_1 in chars_1:
            if char_2["id"]==char_1["id"]:
                in_list=True
        if not in_list:
            chars_1.append(char_2)
    return chars_1

