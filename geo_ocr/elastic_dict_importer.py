from elasticsearch import Elasticsearch,helpers
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
path = "tmp/word_list_dest.txt"

def parse_word_list_file():
    with open(path, 'r') as myfile:
        content=myfile.read()
        return content.split('\n')

cor_words = parse_word_list_file()
my_list = ({'_op_type': 'index', 'word': k.decode('utf8'), '_index':'wordbase', '_type':'words'} for k in cor_words)
helpers.bulk(es, my_list)
