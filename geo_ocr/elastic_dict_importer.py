#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch,helpers
import string
permited_chars = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"
es = Elasticsearch([{'host': 'ocr.mlearning.ge', 'port': 9200}])
path = "tmp/word_list_dest.txt"

def parse_word_list_file():
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')

# import words from wordlist text file
cor_words = parse_word_list_file()
# remove punctuation from words
list_of_truncated_words = ["".join(c for c in k.decode('utf8') if c in permited_chars.decode('utf8')) for k in cor_words]
# remove duplicates
unique_list = set(list_of_truncated_words)
# create list of jsons for bulk importer
my_list = [{'_op_type': 'index', 'word': k, '_index':'wordbase', '_type':'words'} for k in unique_list]
# iterator for bulk importer
iter_list = iter(my_list)
# bulk import
helpers.bulk(es, iter_list)
