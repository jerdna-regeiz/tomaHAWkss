#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
from flask import request
from flask import json
from . import config
#exploit conf still doesnt work by me(lilli), please check it out
#from exploitsConfiguration.config import ExploitConfig

app = Flask(__name__)
for blue in config.blueprints:
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

def run():
    port = 4567
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)

