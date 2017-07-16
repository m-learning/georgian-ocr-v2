#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch,helpers
import string
permited_chars = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"
es = Elasticsearch([{'host': 'ocr.mlearning.ge', 'port': 9200}])
path = "../tmp/word_list_dest.txt"

def parse_word_list_file():
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')

cor_words = parse_word_list_file()
my_list = ({'_op_type': 'index', 'word': "".join(c for c in k.decode('utf8') if c in permited_chars.decode('utf8')), '_index':'wordbase', '_type':'words'} for k in cor_words)
helpers.bulk(es, my_list)
