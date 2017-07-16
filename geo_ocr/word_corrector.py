# -*- coding: utf-8 -*-
import re
import urllib2
import json

def parse_word_list_file(path):
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')


def find_matching_word(word):
    url = "http://ocr.mlearning.ge:9200/_search"
    data = {'query': {'fuzzy' : { 'word' :{'value':word,'fuzziness': 2}}}}
    req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    json_data = json.loads(response)
    if not json_data['hits']['hits']: return word

    chosen_word = json_data['hits']['hits'][0]['_source']['word']
    if chosen_word != word:
      print 'Word was corrected ' + word + ' with ' + chosen_word
      return chosen_word
    else: return word


def correct_words(text):
    text = unicode(text, 'utf-8')
    def replace_callback(match):
        if not match.group(2).strip(): return match.group(0)
        replaced_word = find_matching_word(match.group(2))
        return match.group(1) + replaced_word

    replaced_text = re.compile(r'(^|\s)(.*?)(?=\s|$)',
        flags=re.M).sub(replace_callback, text)

    return replaced_text
