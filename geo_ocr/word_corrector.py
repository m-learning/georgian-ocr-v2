# -*- coding: utf-8 -*-
import Levenshtein as lev
import re

def parse_word_list_file(path):
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')


def find_matching_word(word, correct_words):
    distances = []
    for w in correct_words:
      distance = lev.distance(word, w)
      if distance == 0:
        return w

      else: distances.append({'word': w, 'distance': distance})

    distance_sorted = sorted(distances, key=lambda d: d['distance'])

    chosen_word = distance_sorted[0]
#    print 'Chosen word '+ chosen_word['word'] + ' ' + str(chosen_word['distance']), str(len(word.decode('utf-8'))/2)
    # If distance is enough close we alter the word
    if chosen_word['distance'] < len(word.decode('utf-8'))/3:
      print 'Word was corrected ' + word + ' with ' + chosen_word['word']
      return chosen_word['word']
    else: return word


def correct_words(text, correct_words):

    def replace_callback(match):
        if not match.group(2).strip(): return match.group(0)
        replaced_word = find_matching_word(match.group(2), correct_words)
        return match.group(1) + replaced_word

    replaced_text = re.compile(r'(^|\s)(.*?)(?=\s|$)', 
        flags=re.M).sub(replace_callback, text)

    return replaced_text
    

