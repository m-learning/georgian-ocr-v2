#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, request, render_template, jsonify
from random import randint
import os
import base64
import json
import sys
import cv2

sys.path.insert(0, '../geo_ocr/')
import read

app = Flask(__name__)

app.secret_key = '31D041CEB9916A0AF926B496445BA6B2'

def createDirIfNotExists(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

UPLOADED_IMAGES_DIR = 'uploaded-images'
RESULT_IMAGES_DIR = 'result-images'
TRAINING_DATA_DIR = 'training-data'

ALLOWED_CHARS = ['d', '=', '-', ',', ';', ':', '!', '?',
    '\'', '"', '(', ')', '*', '%', '+',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    u'ა', u'ბ', u'გ', u'დ', u'ე', u'ვ', u'ზ', u'თ', u'ი', u'კ', u'ლ', u'მ', u'ნ',
    u'ო', u'პ', u'ჟ', u'რ', u'ს', u'ტ', u'უ', u'ფ', u'ქ', u'ღ', u'ყ', u'შ', u'ჩ',
    u'ც', u'ძ', u'წ', u'ჭ', u'ხ', u'ჯ', u'ჰ']

createDirIfNotExists(UPLOADED_IMAGES_DIR)
createDirIfNotExists(RESULT_IMAGES_DIR)
createDirIfNotExists(TRAINING_DATA_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        #if 'last_image_path' in session:
        #    if session['last_image_path'] != 0:
        #        return render_template('index.html')
        #    else:
        #        return render_template('upload.html')
        #else:
        return render_template('upload.html')

    elif request.method == 'POST' and 'image' in request.files:
        filename = str(len(os.walk(UPLOADED_IMAGES_DIR).next()[2]) + 1)
        last_image_path = os.path.join(UPLOADED_IMAGES_DIR, filename)
        _file = request.files['image']
        _file.save(last_image_path)
        print 'File ' + filename + ' was uploaded successfully'
        session['last_image_path'] = last_image_path
        return render_template('index.html')

@app.route('/load', methods=['GET'])
def load():
    if 'last_image_path' in session:
        last_image_path = session['last_image_path']
    else:
        last_image_path = ''

    if not os.path.isfile(last_image_path):
        print('File' + last_image_path + ' not found')
        return ''

    filenames = []

    char_images = read.read_lines(last_image_path)    
    
    for i in range(len(char_images)):
        if char_images[i] == 'space':
            filenames.append('space')
        elif char_images[i] == 'newline':
            filenames.append('newline')
        else:
            filename = os.path.join(RESULT_IMAGES_DIR, str(i) + '.png')
            filenames.append(filename)
            cv2.imwrite(filename, char_images[i])

    images = []
    for filename in filenames:
        if filename == 'space':
            images.append('space')
        elif filename == 'newline':
            images.append('newline')
        else:
            images.append(read_image(filename))
    
    return jsonify(images)

def read_image(src):
    with open(src, 'rb') as image_file:
        data = image_file.read()
        return 'data:image/jpeg;base64,' + data.encode('base64')
        
        
@app.route('/clear', methods=['GET'])
def clear():
    print 'Cleared'
    session['last_image_path'] = 0
    return ''

@app.route('/save', methods=['POST'])
def save():
    data = json.loads(request.form['data'])
    for i in range(len(data)):
        result = data[i].get('result').replace('.', 'd')
        
        if result not in ALLOWED_CHARS:
            continue

        directory = os.path.join(TRAINING_DATA_DIR, result)
        
        createDirIfNotExists(directory)

        if os.path.isdir(directory):
            try:
                img = base64.decodestring(data[i].get('image'))
                files_count = len(os.walk(directory).next()[2])
                file_path = os.path.join(directory, str(files_count + 1) + '.png')
                f = open(file_path, 'w')
                f.write(img)
                f.close()
            except:
                print 'Could not write image in ' + directory
    print 'Training data was saved sucessfully'

    return 'OK'
    
if __name__ == '__main__':
    app.run()
