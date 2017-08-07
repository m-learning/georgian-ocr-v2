#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
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
pmarks = u',.!\'":;'

def char_classify(all_meta):
    # ------------------------ 1 --------------------------
    #center = 32 - all_meta[0]
    
    new_meta = []
    for ch in all_meta:
        fv = {}
        
        if ch['char'] in u''.join(classes):
            for i in range(len(classes)):
                if ch['char'] in classes[i]:
                    ch['class'] = i
                    if i == 2 or i == 3:
                        ch['lh'] = ch['h'] / 2.
                    else:
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
        if meta['char'] in classes[0] and meta['score'] > 0.5:
            char1 = meta
        elif meta['char'] in classes[3] and meta['score'] > 0.5:
            char2 = meta

    if char1 == None or char2 == None:
        return None
    
    char_bit = char2['h'] / 8  
    if ((char1['h'] - char2['h'])**2) ** 0.5 < char_bit:
        return 'Mtavruli'
    else:
        return 'Mxedruli'


def detect_avg_wh(all_meta, samp_chars=20):
    
    # character counting
    chars = {}
    for meta in all_meta:
        #print meta['char']
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
    
    avg_width = sum([n[1][1]['w'] for n in avr_chars])  / len(avr_chars)
    avg_width *= 0.4

    middle_chars = [n[1][1]['h'] for n in avr_chars
                      if n[1][1]['char'] in classes[1]+classes[3]]
    
    if len(middle_chars) == 0:
        avg_height = avg_width
    else:
        avg_height = (sum(middle_chars) / (1.1*len(middle_chars))) 
        
    return avg_width, avg_height


def export(all_meta):
    
    all_meta = char_classify(all_meta)
    all_meta = all_meta[::-1]
    
    font_type = find_font_type(all_meta)
    
    # pass empty if error is high 
    if font_type == None:
        print "> Error rate for text is to high, can't detect font type"
        # TODO: Construct flat text (word_from_meta_array)
        # return '--', [all_meta], 0, 0
    else:
        print 'Font Type: ', font_type
        
    
    avg_char_width, avg_line_height =  detect_avg_wh(all_meta[0:100])
    #avg_char_width = 30
    #avg_line_height = 40
    
    print 'Char avr width: ', avg_char_width
    print 'Char avr height: ', avg_line_height
    
    lines = []
    line = []
    tline = []
    text = ''
    
    all_meta = sorted(all_meta, key=lambda x: x['y'])
    #for n in all_meta:
        #print n
    #    print n['x'], n['y'], n['id'], n['char'], '===='
    
    # Sort and find lines
    m_len = len(all_meta)
    for i in xrange(m_len):
        line.append(all_meta[i])
        line.sort(key=lambda x: x['x'])
        dy = 0
        if i != m_len-1 and i > 1: 
            if font_type == 'Mxedruli':
                y1 = sum([n['y'] + n['lh'] for n in line]) / len(line)
                y2 = all_meta[i+1]['y'] + all_meta[i+1]['lh']
                dy = y2 - y1
                v = all_meta[i]
                #print 'char:', v['char'], 'lh:', v['lh'], 'h:', v['h'], 'class:', v['class'], 'w:', v['w'], 'y:', v['y'], 'x:', v['x'], 'id:', v['id'], '\n'
            else: #elif font_type == 'Mtavruli':
                y1 = sum([n['y'] for n in line]) / len(line)
                dy = all_meta[i+1]['y'] - y1
                
        if i == m_len-1 or dy >= avg_line_height:
            #space_cnt = 0
            for j in xrange(len(line)):
                if line[j]['x'] - line[j-1]['x'] - line[j-1]['w'] > avg_char_width:
                    text += u' '
                    
                    # add space
                    space = line[j].copy()
                    space['char'] = u' '
                    space['x'] += 1
                    tline.append(space)
                    
                    
                text += line[j]['char']
                tline.append(line[j])

            text += u'\n'
            #print text
            lines.append(tline)
            line = []
            tline = []
            
            
    return text, lines, avg_char_width, avg_line_height
    
