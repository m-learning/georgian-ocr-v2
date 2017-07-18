from flask import Flask
app = Flask(__name__)
from flask import render_template
from werkzeug.utils import secure_filename
from flask import request
from flask import jsonify
import geo_ocr
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read():
    f = request.files['image']
    path = './tmp_uploads/' + secure_filename(f.filename)
    f.save(path)
    recognized_text = geo_ocr.read(path,
        correct_words = True,
        debug=True)
    os.remove(path)
    return "<pre>"+recognized_text+"</pre>"

@app.route('/api/read', methods=['POST'])
def api_read():
    f = request.files['image']
    path = './tmp_uploads/' + secure_filename(f.filename)
    f.save(path)
    recognized_text = geo_ocr.read(path,
        correct_words = True,
        debug=True)
    os.remove(path)
    return jsonify(text=recognized_text)
