# -*- coding: utf-8 -*-
import sys
sys.path.append('../georgian-ocr-v2/')

from flask import Flask
from flask import render_template
from werkzeug.utils import secure_filename
from flask import request
from flask import jsonify
import geo_ocr
import os
import shutil
from flask_mail import Mail, Message

from flask import make_response
from flask import abort
import uuid
from flask import send_file

app = Flask(__name__)
mail=Mail(app)

app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.test.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'noreply@test.com',
    MAIL_PASSWORD = '',
    MAIL_USE_TLS=False
    )
mail=Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read():
    f = request.files['image']
    rnd_str = str(uuid.uuid4())
    print ('rnd_str:', rnd_str)
    or_filename = rnd_str + '_' + secure_filename(f.filename)
    orpath = './tmp_uploads/'+ or_filename
    print('orpath', orpath)
    f.save(orpath)
    filename, extension = os.path.splitext(orpath)
    if extension == '.pdf':
        recognized_text = ""
        num = pdf_to_images(orpath, './tmp_uploads/')
        for i in range(num):
            path = os.path.abspath('tmp_uploads/'+str(i)+'.jpg')
            recognized_text += geo_ocr.read(path,
                correct_words = True,
                debug=False,
                to_pdf=True)
            recognized_text +="\n"
            os.remove(path)
    else:
        recognized_text = geo_ocr.read(orpath,
            correct_words = True,
            debug=False,
            to_pdf=True)
    os.remove(orpath)
    filename, extension = os.path.splitext(or_filename)
    pdf_file = '/tmp/'+filename+'.pdf'
    static_pdf = './static/pdf/'+filename+'.pdf'
    os.makedirs(os.path.dirname(static_pdf), exist_ok=True)
    shutil.copyfile(pdf_file, static_pdf)
    print ('pdf_file:', pdf_file)
    return '/static/pdf/'+filename+'.pdf' 
    #return "<pre>"+recognized_text+"</pre>"

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

@app.route("/send", methods=['POST'])
def send():
    subject = request.form['name']
    sender = request.form['email']
    msg = Message(subject, sender=sender, recipients=['mail@test.com'])
    msg.body = request.form['text']
    mail.send(msg)
    return "გაგზავნილია."

def pdf_to_images(pdf, output_dir):
    pdf = file(pdf, "rb").read()

    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        #print "JPG %d from %d to %d" % (njpg, istart, iend)
        jpg = pdf[istart:iend]
        jpgfile = file(output_dir+"%d.jpg" % njpg, "wb")
        jpgfile.write(jpg)
        jpgfile.close()

        njpg += 1
        i = iend
        return njpg
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
