import re

def generate_word_list(source, dest):
  distinct_words = {}

  def replace_callback(match):
      if not match.group(2).strip(): return
      word = match.group(2)
      distinct_words[word] = 1
      

  with open(source, 'r') as myfile:
      content=myfile.read()
      re.compile(r'(^|\s|\.|,|\?|!|\.|:|;|\'|-|")(.*?)(?=\s|\.|,|\?|!|\.|:|;|\'|-|"|\n|$)', flags=re.M).sub(replace_callback, content)

      f = open(dest, 'w')
      for word in distinct_words:
          f.write(word+'\n')
      f.close()
