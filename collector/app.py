from flask import Flask, request, render_template, jsonify
from random import randint
import os
import base64
import json
import sys
import cv2

sys.path.insert(0, '../geo_ocr/')
import read

app = Flask(__name__)

UPLOADED_IMAGES_DIR = 'uploaded-images'
RESULT_IMAGES_DIR = 'result-images'

last_image_path = 0

@app.route('/', methods=['GET', 'POST'])
def index():
	global last_image_path
	if request.method == 'GET':
		if last_image_path != 0:
			return render_template('index.html')
		else:
			return render_template('upload.html')
	elif request.method == 'POST' and 'image' in request.files:
		filename = str(len(os.walk(UPLOADED_IMAGES_DIR).next()[2]) + 1)
		last_image_path = os.path.join(UPLOADED_IMAGES_DIR, filename)
		_file = request.files['image']
        _file.save(last_image_path)
        print "File " + filename + " was uploaded successfully"
        return render_template('index.html')

@app.route('/load', methods=['GET'])
def load():
	# TODO run read.py for last_image_path
	# return json array of base64 strings of extracted images
    global last_image_path
    print last_image_path

    if not os.path.isfile(last_image_path):
		print("File" + last_image_path + " not found")
		return ""

    filenames = []
    char_images = read.read(last_image_path)
    for i in range(len(char_images)):
        filename = RESULT_IMAGES_DIR + "/" + str(i) + ".png"
        filenames.append(filename)
        cv2.imwrite(filename, char_images[i])

    images = []
    for filename in filenames:
        images.append(read_image(filename))
    
    return jsonify(images)

def read_image(src):
	with open(src, "rb") as image_file:
		data = image_file.read()
		return "data:image/jpeg;base64," + data.encode("base64")
		
		
@app.route('/clear', methods=['GET'])
def clear():
	print "clear"
	global last_image_path
	last_image_path = 0
	return ""

@app.route("/save", methods=['POST'])
def save():
	data = json.loads(request.form['data'])
	for i in range(len(data)):
		
		result = data[i].get("result")
		if result == ".":
			result = "dot_and_others"

		directory = "training-data/" + result

		if os.path.isdir(directory):
			try:
				img = base64.decodestring(data[i].get("image"))
				files_count = len(os.walk(directory).next()[2])
				file_path = directory + "/" + str(files_count + 1) + ".png"
				f = open(file_path, "w")
				f.write(img)
				f.close()
				print "Image was written sucessfully in " + directory
			except:
				print "Could not write image in " + directory

	return "OK"
    
if __name__ == '__main__':
    app.run()
