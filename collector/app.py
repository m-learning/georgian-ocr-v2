from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from random import randint
import os
import base64
import json

app = Flask(__name__)

last_image = 0

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/load', methods=['GET'])
def load():
	images = []
	for i in range(randint(2, 10)):
		images.append(read_image("images/" + str(randint(1, 2)) + ".jpg"))
	
	
	global last_image
	print(last_image)
	
	return jsonify(images)
	

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	global last_image
	last_image += 1
	return render_template('index.html')

def read_image(src):
	with open(src, "rb") as image_file:
		data = image_file.read()
		return "data:image/jpeg;base64," + data.encode("base64")

@app.route("/save", methods=['POST'])
def save():
	data = json.loads(request.form['data'])
	for i in range(len(data)):
		img = base64.decodestring(data[i].get("image"))
		f = open("results/" + data[i].get("result") + ".png", "w")
		f.write(img)
		f.close()

	return "OK"
    
if __name__ == '__main__':
    app.run()
