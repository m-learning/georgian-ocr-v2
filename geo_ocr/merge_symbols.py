import image_operations as image_ops
from predict_all import *


def converter(each):
    tmp = {}
    tmp['y'] = each['y']
    tmp['x'] = each['x']
    tmp['w'] = each['w']
    tmp['h'] = each['h']
    tmp['id'] = each['id']
    return tmp


# recognize ? ! : % symbols
def merge(lines, vanished_img):
    newLines=[]
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]) - 1:
            first = lines[i][j]
            second = lines[i][j + 1]
            common_lenght = first['x'] + first['w'] - second['x']
            min_with = min(first['w'], second['w'])
            if first['char'] != ' ' and float(common_lenght) / min_with > 0.5:
                second['w'] = max(second['x'] + second['w'] - first['x'], first['w'])
                second['h'] = max(first['y'] + first['h'], second['y'] + second['h']) - min(first['y'], second['y'])
                second['x'] = first['x']
                second['y'] = min(first['y'], second['y'])
                newLines.append(second)

                char_img = image_ops.crop_char_image(converter(second), vanished_img)
                pairs = recognize_image(char_img.flatten())
                second['char'] = pairs[0]['char']
                second['score'] = pairs[0]['score'].item()
                second["alternatives"] = [pairs[1], pairs[2], pairs[3]]
            else:
                newLines.append(first)
            j += 1
    lines=newLines
