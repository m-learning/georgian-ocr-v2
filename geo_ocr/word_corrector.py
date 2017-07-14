# -*- coding: utf-8 -*-
import re
import urllib2
import json

def parse_word_list_file(path):
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')


def find_matching_word(word, correct_words):
    url = "http://localhost:9200/_search"
    data = {'query': {'fuzzy' : { 'word' :{'value':word,'fuzziness': 2}}}}
    req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    json_data = json.loads(response)
    chosen_word = json_data['hits']['hits'][0]['_source']['word']
#    print 'Chosen word '+ chosen_word['word'] + ' ' + str(chosen_word['distance']), str(len(word.decode('utf-8'))/2)
    # If distance is enough close we alter the word
    if chosen_word != word:
      print 'Word was corrected ' + word + ' with ' + chosen_word
      return chosen_word
    else: return word


def correct_words(text, correct_words):

    def replace_callback(match):
        if not match.group(2).strip(): return match.group(0)
        replaced_word = find_matching_word(match.group(2), correct_words)
        return match.group(1) + replaced_word

    replaced_text = re.compile(r'(^|\s)(.*?)(?=\s|$)',
        flags=re.M).sub(replace_callback, text)

    return replaced_text
