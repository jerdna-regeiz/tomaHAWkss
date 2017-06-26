#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
from flask import request
from . import config
from exploitsConfiguration.config import ExploitConfig

app = Flask(__name__)
for blue in config.blueprints:
    app.register_blueprint(blue)

@app.route('/exploit/<name>/<period>', methods=["POST","DELETE"])
def exploit(name, period) :
	conf = ExploitConfig()
	if request.method =='POST': 
		#Exploit with <name> and <period> should be excuted after scheduling here
		#Exploit should be in the file with <name> in the same folder
		conf.put(name, "period", period)
		resp=Response("post request")
		resp.headers['Access-Control-Allow-Origin'] ='*'
		return resp
	else: 

		#Exploit with name = <name> should be stopped here
		conf.remove(name)
		resp=Response("delete request")
		resp.headers['Access-Control-Allow-Origin'] ='*'
		return resp
	
@app.route('/runMonitor', methods=["POST"])
def monitor():
	#Monitoring should be called here and response to the gui

	resp=Response("post request")
	return resp

@app.route('/addTarget', methods=["POST"])
def target() :
	#Target should be added and saved here
	resp=Response("post request")
	return resp	

def run():
    port = 4567
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)

