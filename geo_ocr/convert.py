import sys
import pdfkit
import json
from shutil import copyfile
from PIL import Image
import cairocffi as cairo

def find_max_font_size(text, max_w, max_h):
    surface = cairo.SVGSurface("example.svg", max_w, max_h)
    context = cairo.Context(surface)

    font_size = 1000

    context.set_font_size(font_size)
    box = context.text_extents(text)
    w = box[2]
    h = box[3]
    
    while w > max_w:
        ratio_w = max_w / w
        font_size = font_size * ratio_w
        context.set_font_size(font_size)
        box = context.text_extents(text)
        w = box[2]

    h = box[3]

    while h > max_h:
        ratio_h = max_h / h
        font_size = font_size * ratio_h
        context.set_font_size(font_size)
        box = context.text_extents(text)
        h = box[3]

    print ('cairo', text, w, h, font_size)

    return int(font_size)

def topdf(image, data):
    img = image.split('/')[-1]
    ext = img.split('.')[-1]
    img = img.split('.')[:-1]
    img = ''.join(img)
    img = img.replace('.', '_')
    pdf_name = '%s.pdf' % img
    html_name = '%s.html' % img
    image_name = '%s.%s' % (img, ext)
    image_path = '/tmp/%s' % image_name
    
    pdf_width_px = 595
    pdf_height_px = 842
    
    copyfile(image, image_path)
    
    orientation = 'Portrait'
    with Image.open(image_path) as im:
        image_width, image_height = im.size
        print (image_width, image_height)
    if image_width > image_height:
        pdf_width_px, pdf_height_px = pdf_height_px, pdf_width_px
        orientation = 'Landscape'
    
    size_proportion = 1
    if image_width > pdf_width_px:
        size_proportion = pdf_width_px / image_width
        image_width = pdf_width_px
        image_height = image_height * size_proportion
    if image_height > pdf_height_px:
        size_proportion = pdf_height_px / image_height
        image_height = pdf_height_px
        image_width = image_width * size_proportion
    print (image_width, image_height)
    
    #font-size: calc(100%% - -1.2em);
    css = '<style type="text/css">'
    css += "body{background-image: url('./%s');background-repeat: no-repeat; margin:0px; padding: 0px;background-size:%.2fpx %.2fpx;}" % (image_name, image_width, image_height)
    css += 'span{color: rgba(255,255,255,0);}'
    css += '::selection{background:rgba(120,255,255,0.5);color: rgba(255,255,255, 0);}'
    css += '::-moz-selection{background:rgba(120,255,255,0.5);color: rgba(255,255,255, 0);}'

    html = ''
    for l_num, line in enumerate(data):
        if not len(line):
            continue
            
        count = len(line)
        line_word_0 = line[0]
        line_word_n = line[count-1]
        while 1 < count-1:
            last_word = line[count-1]
            line_word_n = last_word
            if (len(last_word) == 1):
                #if (last_word[0]['char'] == ' '):
                count -= 1
                continue
            break
        
        if len(line_word_0):
            div_start_left = line_word_0[0]['x']/4 * size_proportion
            #div_start_top = line_word_0[0]['y']/4 * size_proportion
            div_width = line_word_n[len(line_word_n)-1]['x']/4 * size_proportion + line_word_n[len(line_word_n)-1]['w']/4 * size_proportion
            line_width = div_width - div_start_left

        '''
        many_h = []
        many_y = []
        for w_num, word in enumerate(line):
            for char in word:
                many_y.append(char['y']/4)
                many_h.append(char['y']/4 + char['h']/4)
        min_y = min(many_y)
        max_h = max(many_h)
        span_height = max_h - min_y
        '''
        div_cls = 'div-line%d' % l_num
        div = '<div class="%s">%s</div>'
        spnas = ''
        
        many_h = []
        many_x = []
        many_y = []
        words = ''
        for w_num, word in enumerate(line):
            many_word_x = []
            many_word_height = []
            if len(word):
                span_start_left = word[0]['x']/4 * size_proportion
                #span_start_top = word[0]['y']/4 * size_proportion
                span_width = word[len(word)-1]['x']/4*size_proportion + word[len(word)-1]['w']/4* size_proportion - span_start_left
            span = '<span class="%s">%s</span>'
            chars = ''
            for c_num, char in enumerate(word):
                x, y, w, h = char['x']/4, char['y']/4, char['w']/4, char['h']/4
                
                many_word_x.append(x)
                many_word_height.append(x+h)
                
                if len(word) != 1 or True:
                    many_x.append(x)
                    many_y.append(y)
                    many_h.append(y + h)
                chars += char['char']
            print ('chars:', chars)
            max_word_x = max(many_word_x)
            min_word_x = min(many_word_x)
            max_word_height = max(many_word_height)
            line_font_height = max_word_height - min_word_x
            font_size = find_max_font_size(chars, int(span_width), int(line_font_height))
            font_size = font_size
            if len(word) == 1:
                font_size = 'inherit'
            else:
                size_percent = 5
                if font_size > 50:
                    size_percent = 10
                font_size = '%dpx' % (font_size-(font_size/100*size_percent),)
            words += chars
            cls = 'span-word%d%d' % (l_num,w_num)
            css += ' span.%s{position:absolute;left:%dpx;font-size:%s;width:%dpx;}' % (cls, span_start_left, font_size, span_width)
            spnas += span % (cls, chars)
            
            
        
        max_x = max(many_x)
        min_x = min(many_x)
        min_y = min(many_y)
        max_h = max(many_h)
        line_font_height = max_h - min_y
        line_font_height = max_x - min_x
        print ('words')
        font_size = find_max_font_size(words, int(line_width), int(line_font_height))
        font_size = font_size
        css += ' div.%s{position:absolute;top:%dpx;font-size:%dpx;}' % (div_cls, min_y * size_proportion, font_size-(font_size/100*10))

        html += div % (div_cls, spnas)

    css += '</style>'

    body = '<head><meta charset="utf-8"/>' + css + '</head>'
    body += '<body>' + html + '</body>'

    options = {
        'orientation': orientation,
    }
    
    pdfkit.from_string(body, '/tmp/%s' % pdf_name, options=options)
    with open('/tmp/%s' % html_name, 'w') as f:
        f.write(body)
    
if __name__ == "__main__":
    #python3 convert.py /tmp/image.jpg /tmp/data.json
    image = sys.argv[1]
    data_file = sys.argv[2]
    with open(data_file, 'r') as f:
        data = json.load(f)
    convert(image, data)
