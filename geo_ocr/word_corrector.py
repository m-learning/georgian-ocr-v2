# -*- coding: utf-8 -*-
import re
import urllib2
import json
import Levenshtein as lev
import copy

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
     

def correct_words(text):
    text = unicode(text, 'utf-8')
    def replace_callback(match):
        if not match.group(2).strip(): return match.group(0)
        replaced_word = find_matching_word(match.group(2))
        return match.group(1) + replaced_word

    replaced_text = re.compile(r'(^|\s)(.*?)(?=\s|$)',
        flags=re.M).sub(replace_callback, text)

    return replaced_text


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


def replacing_letter_is_wrong(char_meta, replacing_letter):
    if char_meta['score'] > 0.9: return True
    if char_meta['alternatives'][0]['char'] == replacing_letter: return False
    if char_meta['alternatives'][1]['char'] == replacing_letter: return False
    return True


def deleting_letter_is_wrong(char_meta):
    if char_meta['score'] > 0.9: return True
    return False


def choose_best_match(word_meta, word_alternatives):
    read_word = word_from_meta_array(word_meta)
    chosen_word = read_word

    # Traverse through alternatives, received from elasticsearch
    for word_alt in word_alternatives:
        print 'Word alternative', word_alt['word']

        word_alt_is_wrong = False
        modifying_word_meta = copy.deepcopy(word_meta)

        # Take edit operations from read word to alternative. 
        # Check if alternative is better than original.
        editops = lev.editops(read_word, word_alt['word'])

        for editop in editops:
            (op, source_index, dest_index) = editop
            
            if op == 'replace':
                modifying_word_meta[source_index]['char'] = word_alt['word'][dest_index]
                if replacing_letter_is_wrong(modifying_word_meta[source_index], word_alt['word'][dest_index]):
                    word_alt_is_wrong = True
                    break
            elif op == 'delete':
                if deleting_letter_is_wrong(modifying_word_meta[source_index]):
                    word_alt_is_wrong = True
                    break
                del modifying_word_meta[source_index]
            elif op == 'insert':
                modifying_word_meta.insert(source_index, {'char':word_alt['word'][dest_index]})

        if not word_alt_is_wrong:
            # Word alternative passed all the checks, so we replace the original
            chosen_word = word_alt['word']
            break

    return chosen_word


def correct_words_with_scores(lines):
    word_lines = group_meta_as_words(lines)
    
    text = ''
    for l in word_lines:
      for w in l:
        word = word_from_meta_array(w)
        
        best_match = choose_best_match(w, find_matching_words(word))
        text+=' '+best_match

      text+='\n'

    return text

    
