#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
from flask import request
from flask import json
from flask.json import jsonify
import subprocess

from config import blueprints
#exploit conf still doesnt work by me(lilli), please check it out
#from exploitsConfiguration.config import ExploitConfig

import os
from os import walk
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'assets/lib'
ALLOWED_EXTENSIONS = set(['py'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
for blue in blueprints:
   app.register_blueprint(blue)

@app.route('/exploit/<name>/<period>', methods=["POST","DELETE"])
def exploit(name, period) :
#	conf = ExploitConfig()
	if request.method =='POST': 
		#Exploit with <name> and <period> should be excuted after scheduling here
		#Exploit should be in the file with <name> in the same folder
#		conf.put(name, "period", period)
		addE={'status' :'ok'}
		return json.dumps(addE)
	else: 

		#Exploit with name = <name> should be stopped here
#		conf.remove(name)
		deleteE={'status':'ok'}
		return json.dumps(deleteE)
	
@app.route('/runMonitor/<regex>', methods=["POST"])
def monitor(regex):
	#Monitoring should be called here and response to the gui
	monitor={'time' : '2017-07-03','result' : 'monitoring is running, here is the result'}
	return json.dumps(monitor)

@app.route('/exploitResult', methods=["POST"])
def result():
	#so should implement result(a json object) of all exploit with its status sofar
	#for example there are current ex1, ex2, ex3 
	results={'ex1':'SUCESS', 'ex2':'FAILED','ex3':'IS RUNNING'}
	return json.dumps(results)
	
@app.route('/addTarget/<name>/<user>/<password>', methods=["POST"])
def target(name, user, password) :
	#Target should be added and saved here
	resp=Response("post request")
	return resp	

@app.route('/exploit/delete/<string:file_name>', methods=["DELETE"])
def exploitDelete(file_name):
	if request.method == 'DELETE':
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
		local.cmd('*', 'cmd.run', ['rm ~/lib/' + file_name])
		subprocess.call(['salt "*" cmd.run "rm ~/lib/' + file_name + '"'], shell=True)
		return 'succesfully deleted ' + file_name

@app.route('/exploit/upload', methods=["POST"])
def exploitUpload():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return 'No file part'
		
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'No selected file'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			subprocess.call(['salt-cp "*" ' + os.path.join(app.config['UPLOAD_FOLDER'], filename) + ' ~/lib'], shell=True)
			#subprocess.call(os.path.join('assets','deploy.sh'), shell=True)
			return 'succesfully added ' + file.filename
		return ''

@app.route('/exploit/all', methods=["GET"])		
def getAllExploits():
	f = []
	for (dirpath, dirnames, filenames) in walk(app.config['UPLOAD_FOLDER']):
		f.extend(filenames)
		break
	return jsonify({'data': f})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run():
    port = 4567
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)

