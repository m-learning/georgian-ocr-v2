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
    orpath = './tmp_uploads/' + secure_filename(f.filename)
    f.save(orpath)
    filename, extension = os.path.splitext(orpath)
    if extension == '.pdf':
        recognized_text = ""
        num = pdf_to_images(orpath, './tmp_uploads/')
        for i in range(num):
            path = os.path.abspath('tmp_uploads/'+str(i)+'.jpg')
            recognized_text += geo_ocr.read(path,
                correct_words = True,
                debug=True)
            recognized_text +="\n"
            os.remove(path)
    else:
        recognized_text = geo_ocr.read(orpath,
            correct_words = True,
            debug=True)
    os.remove(orpath)
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
	    print "JPG %d from %d to %d" % (njpg, istart, iend)
	    jpg = pdf[istart:iend]
            jpgfile = file(output_dir+"%d.jpg" % njpg, "wb")
	    jpgfile.write(jpg)
	    jpgfile.close()

	    njpg += 1
	    i = iend
        return njpg
