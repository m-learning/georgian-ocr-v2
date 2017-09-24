# -*- coding: utf-8 -*-
permitted_chars = u"აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

def lines_to_text(lines):
    word_lines = group_meta_as_words(lines)
    text = word_lines_to_text(word_lines)
    return text

def word_lines_to_text(word_lines):
    text = ''
    for l in word_lines:
      for w in l:
        word = word_from_meta_array(w)
        text += word

      text = text.strip()+'\n'

    return text


def word_from_meta_array(word_meta):
    word = u''
    for meta in word_meta:
#        print meta['char'], meta['score'], meta['alternatives'][0]['char'], meta['alternatives'][1]['char'],meta['alternatives'][2]['char']
        word += meta['char']

    return word


def is_punctuation(line, position):
    for i in range(position, len(line)):
        meta = line[i]
        if meta['char'] in permitted_chars:
            return False
        elif meta['char'] == u' ':
            return True

    return True


def take_word_from_line(line, position):
    # If first char is punctuation, return as separate word
    first_char = line[position]
    if first_char['char'] not in permitted_chars: 
        return [[line[position]], position+1]
    
    word_metas=[]
    for index in range(position, len(line)):
        meta = line[index]
        if meta['char'] == u' ':
            return [word_metas, index]
        if meta['char'] not in permitted_chars:
#            print 'Checking punctuation', word_from_meta_array(word_metas)
            if is_punctuation(line, index):
                return [word_metas, index]
                
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

def merge_split_words(word_lines):
    for i in range(1, len(word_lines)):
        last_word = word_lines[i-1][-1]
        if last_word[-1]['char'] == '-':
            first_word = word_lines[i][0]
            del last_word[-1]
            last_word += first_word
            del word_lines[i][0]

            # Move following punctuation with it's word
            if len(word_lines[i]) == 0: continue

            new_first_word = word_lines[i][0]
            if new_first_word[0]['char'] in ".,:!?;'":
                word_lines[i-1].append(new_first_word)
                del word_lines[i][0]

            # Remove startin space
            new_first_word = word_lines[i][0]
            if len(word_lines[i]) == 0: continue
            if new_first_word[0]['char'] == ' ':
                del word_lines[i][0]

    return word_lines
