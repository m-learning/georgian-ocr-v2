from flask import Flask, request, render_template, jsonify
from random import randint
import os
import base64
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('upload.html')
	elif request.method == 'POST' and 'image' in request.files:
		_file = request.files['image']
		filename = str(len(os.walk('uploaded-images').next()[2]) + 1)
        _file.save('uploaded-images/' + filename)
        print "File " + filename + " was uploaded successfully"
        return render_template('index.html')

@app.route('/load', methods=['GET'])
def load():
	images = []
	for i in range(randint(2, 10)):
		images.append(read_image("images/" + str(randint(1, 2)) + ".jpg"))
	
	return jsonify(images)
	
def read_image(src):
	with open(src, "rb") as image_file:
		data = image_file.read()
		return "data:image/jpeg;base64," + data.encode("base64")

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
