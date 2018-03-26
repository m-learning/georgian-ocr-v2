# -*- coding: utf-8 -*-
import re
import urllib3
import json
import Levenshtein as lev
import copy
from . import char_operations as co

permitted_chars = u"აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

# Obsolete
def remove_symbols(word):
    return "".join(c for c in word if c in permitted_chars)

def parse_word_list_file(path):
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')


def find_matching_words(word):
    if len(word) > 20:
        print ('Word is too long to find alternatives')
        return []

    url = "http://elasticsearch:9200/wordbase/_search"
    data = {'size':20, 'query': {'fuzzy' : { 'word' :{'value':word,'fuzziness': 2}}}}
    encoded_data = json.dumps(data).encode('utf-8')
    http = urllib3.PoolManager()
    r = http.request(
            'GET',
            url,
            body=encoded_data,
            headers={'Content-Type': 'application/json'})
    json_data = json.loads(r.data.decode('utf-8'))

    results = []
    for hit in json_data['hits']['hits']:
        results.append({
          'word': hit['_source']['word'],
          'score': hit['_score']
        })

    return results


def replacing_letter_is_wrong(char_meta, replacing_letter):
    if 'score' not in char_meta: return True
    if char_meta['score'] > 0.8: return True

    for alt in char_meta['alternatives']:
        if alt['score'] < 0.1: return True
        if alt['char'] == replacing_letter: return False

    return True


def deleting_letter_is_wrong(char_meta):
    if char_meta['score'] > 0.8: return True
    return False


def choose_best_match(word_meta, word_alternatives):
    #word_alternatives = sort_word_alternatives(word_alternatives)
    read_word = co.word_from_meta_array(word_meta)
#    print "Checking -- ", read_word
    chosen_word = read_word

    # Traverse through alternatives, received from elasticsearch
    for word_alt in word_alternatives:
#        print 'Word alternative', word_alt['word'], word_alt['score']

        word_alt_is_wrong = False
        modifying_word_meta = copy.deepcopy(word_meta)

        # Take edit operations from read word to alternative. 
        # Check if alternative is better than original.
        editops = lev.editops(read_word, word_alt['word'])

        for editop in editops:
            (op, source_index, dest_index) = editop

#            print op, source_index, dest_index, read_word, word_alt['word']
            if op == 'replace':
                if len(modifying_word_meta) <= source_index:
                    print ('Asking to replace unknown index in word. Skipping alternative word')
                    word_alt_is_wrong = True
                    break

                if replacing_letter_is_wrong(modifying_word_meta[source_index], word_alt['word'][dest_index]):
                    word_alt_is_wrong = True
                    break

                modifying_word_meta[source_index]['char'] = word_alt['word'][dest_index]
            elif op == 'delete':
                if len(modifying_word_meta) <= source_index:
                    print ('Asking to delete unknown index in word. Skipping alternative word')
                    word_alt_is_wrong = True
                    break

                if deleting_letter_is_wrong(modifying_word_meta[source_index]):
                    word_alt_is_wrong = True
                    break

                del modifying_word_meta[source_index]
            elif op == 'insert':
                modifying_word_meta.insert(source_index, {'char':word_alt['word'][dest_index]})

        if not word_alt_is_wrong:
            # Word alternative passed all the checks, so we replace the original
            chosen_word = word_alt['word']
            if read_word != chosen_word:
                print ('Word was corrected ' + read_word + ' with ' + chosen_word)
            break

    return chosen_word


def reorder_word_alternatives(read_word, word_alternatives):
    with_insert_op = []
    without_insert_op = []

    for w in word_alternatives:
        editops = lev.editops(read_word, w['word'])

        with_insert = False
        for editop in editops:
            (op, _, _) = editop
            if op == 'insert':
                # FIXME: Disable better
                # with_insert_op.append(w)
                with_insert = True 
                break

        if not with_insert:
            without_insert_op.append(w)

    without_insert_op.extend(with_insert_op)
    return without_insert_op


def correct_words_with_scores(word_lines):

    text = ''
    for l in word_lines:
      for w in l:
        word = co.word_from_meta_array(w)
        if len(w) > 1:
            word_alternatives = find_matching_words(word)
            word_alternatives = reorder_word_alternatives(word, word_alternatives)
            word = choose_best_match(w, word_alternatives)
          
        text += word

      text = text.strip()+'\n'

    return text

    
