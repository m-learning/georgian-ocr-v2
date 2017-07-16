# -*- coding: utf-8 -*-
import re
import urllib2
import json
import Levenshtein as lev

permited_chars = u"აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

# Obsolete
def remove_symbols(word):
    return "".join(c for c in word if c in permited_chars)

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


def find_matching_words(word):
    url = "http://ocr.mlearning.ge:9200/_search"
    data = {'query': {'fuzzy' : { 'word' :{'value':word,'fuzziness': 2}}}}
    req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    json_data = json.loads(response)

    results = []
    for hit in json_data['hits']['hits']:
        results.append({
          'word': hit['_source']['word'],
          'score': hit['_score']
        })

    return results
     

def correct_words(text):
    text = unicode(text, 'utf-8')
    def replace_callback(match):
        if not match.group(2).strip(): return match.group(0)
        replaced_word = find_matching_word(match.group(2))
        return match.group(1) + replaced_word

    replaced_text = re.compile(r'(^|\s)(.*?)(?=\s|$)',
        flags=re.M).sub(replace_callback, text)

    return replaced_text


def take_word_from_line(line, position):
    word_metas=[]
    for index in range(position, len(line)):
        meta = line[index]
        if meta['char'] == u' ': return [word_metas, index+1]
        word_metas.append(meta)

    return [word_metas, len(line)]


def group_meta_as_words(lines):
    word_lines = []
    position = 0
    for l in lines:
        words = []
        while position < len(l):
            [word_metas, position] = take_word_from_line(l, position)
            words.append(word_metas)

        position = 0
        word_lines.append(words)

    return word_lines


def word_from_meta_array(word_meta):
    word = u''
    for meta in word_meta:
        word += meta['char']

    return word


def choose_best_match(word_meta, word_alternatives):
    read_word = word_from_meta_array(word_meta)
    chosen_word = read_word

    for word_alt in word_alternatives:
        print 'Word alternative', word_alt['word']

        is_wrong_word = False
        editops = lev.editops(read_word, word_alt['word'])
        for editop in editops:
            (op, source_index, _) = editop
            print op, source_index, word_meta[source_index]
            if word_meta[source_index]['score'] > 0.9:
                is_wrong_word = True
                break

        if not is_wrong_word:
            chosen_word = word_alt['word']
            break

    return chosen_word


def correct_words_with_scores(lines):
    word_lines = group_meta_as_words(lines)
    
    text = ''
    for l in word_lines:
      for w in l:
        word = word_from_meta_array(w)

#        matching_word_objs = find_matching_words(word)
#        matching_words = [f(x) for w in matching_word_objs]
        
        best_match = choose_best_match(w, find_matching_words(word))
        text+=' '+best_match

      text+='\n'

    return text

    
