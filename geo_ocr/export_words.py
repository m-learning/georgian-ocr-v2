#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import codecs

def read_meta(meta_dir):
    all_meta = []
    # Loop in characters
    for root, _, files in os.walk(meta_dir):
        for f in files:
          fullpath = os.path.join(root, f)

          # Put new one
          with open(fullpath) as json_data:
            meta_obj = json.load(json_data)
            all_meta.append(meta_obj)

    return all_meta


classes = [u"ათიო", u"ბზმნპრსძშჩწხჰ", u"ჭქ", u"გდევკლჟტუფღყცჯ"]

def char_classify(all_meta):
    # ------------------------ 1 --------------------------
    #center = 32 - all_meta[0]
    
    new_meta = []
    for ch in all_meta:
        fv = {}
        for i in range(len(classes)):
            if ch['char'] in classes[i]:
                ch['class'] = i 
                if i == 2 or i == 3:
                    ch['lh'] = ch['h']/2.
                elif i == 0 or i == 1:
                    ch['lh'] = ch['h']
            else:
                ch['class'] = -1
                ch['lh'] = ch['h']
        new_meta.append(ch)
    
    return new_meta


def find_font_type(all_meta):
    # todo -- check on average values
    char1 = None
    char2 = None
    
    print '-------------------------'
    for meta in all_meta[:]:
        if meta['char'] in classes[0] and meta['score'] > 0.50:
            char1 = meta
        elif meta['char'] in classes[3] and meta['score'] > 0.50:
            char2 = meta

    if char1 == None or char2 == None:
        return None
    char_bit = char2['h']/8  
    if ((char1['h'] - char2['h'])**2)**0.5 < char_bit:
        return 'Mtavruli'
    else:
        #print char1['id'], char2['id']
        #print char1['h'], char1['h'] - char2['h'], char2['h']
        #print 'Mxedruli'
        return 'Mxedruli'


def detect_avg_wh(all_meta, font_type, samp_chars=20):
    
    # character counting
    chars = {}
    for meta in all_meta:
        #print meta['char']
        #if meta['char'] in ''.join(classes):
        #print meta['char'], meta['w'] 
        if meta['char'] not in chars:
            chars[meta['char']] = [1, meta]
        else: 
            chars[meta['char']][0]+=1
        
        #print chars[meta['char']][0]
    
    avr_chars = sorted(chars.items(), key = lambda x: x[1][0])
    
    # limit number of charactes by 20
    sample = len(all_meta)
    if sample > samp_chars:
        avr_chars = avr_chars[-samp_chars:]
    
    avg_width = sum([n[1][1]['w'] for n in avr_chars]) / samp_chars
    avg_width *= 0.5
    
    if font_type ==  'Mxedruli':
        avg_height = avg_width * 3
    elif font_type == 'Mtavruli':
        avg_height = avg_width 
    
    return avg_width, avg_height


def export(all_meta):
    
    all_meta = char_classify(all_meta)
    all_meta = all_meta[::-1]

    font_type = find_font_type(all_meta)
    
    # pass empty if error is high 
    if font_type == None:
        print "> Error rate for text if to high, can't detect font type"
        return '', [[]]
    
    print 'Font Type: ', font_type
    
    avg_char_width, avg_line_height =  detect_avg_wh(all_meta[0:100], font_type)
    #avg_char_width = 10
    #avg_line_height = 40
    
    print 'Char avr width: ', avg_char_width
    print 'Char avr height: ', avg_line_height
    
    lines = []
    line = []
    tline = []
    text = ''
    
    # Sort and find lines
    m_len = len(all_meta)
    for i in xrange(m_len):
        line.append(all_meta[i])
        line.sort(key = lambda x: x['x'])
        
        dy = 0
        if i != m_len-1:
        
            if font_type ==  'Mxedruli':
                y2 = all_meta[i+1]['y'] + all_meta[i+1]['lh']
                y1 = all_meta[i]['y'] + all_meta[i]['lh']
                dy = y2 - y1 #
            elif font_type == 'Mtavruli':
                dy = all_meta[i+1]['y'] - all_meta[i]['y']
            
        if i == m_len-1 or dy >= avg_line_height:
            #space_cnt = 0
            for j in xrange(len(line)):
                if line[j]['x'] - line[j-1]['x'] - line[j-1]['w'] > avg_char_width:
                    text += u' '
                    #text += line[j]['char']

                    # add space
                    space = line[j].copy()
                    space['char'] = u' '
                    space['x'] += 1
                    tline.append(space)
                    
                    
                text += line[j]['char']
                tline.append(line[j])
                
            text += u'\n'
            lines.append(tline)
            line = []
            tline = []
            
            
    return text, lines, avg_char_width, avg_line_height
    

if __name__ == "__main__":
  all_meta = read_meta(os.path.join(os.getcwd(),'results/meta/'))
  
  avg_line_height = 40
  avg_char_width = 24
  line_first_chars = get_line_first_chars(all_meta, avg_line_height)

  final_text = ''
  for first_char in line_first_chars:
    all_line_chars = get_all_chars_from_line(all_meta, first_char, avg_line_height)
  
    words = split_line_with_words(all_line_chars, avg_char_width)
    for w in words:
      final_text += w + ' '

    final_text+= '\n'

  print final_text.encode('utf-8')


