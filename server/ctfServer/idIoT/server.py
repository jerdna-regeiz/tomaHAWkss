#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.json import jsonify
from config import blueprints
import os
from os import walk
from flask import Flask, request, redirect, url_for, Response, json, flash
from werkzeug.utils import secure_filename
import subprocess

import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

import salt.client

LIB_UPLOAD_FOLDER = 'assets/lib'
MODULES_UPLOAD_FOLDER = 'assets/modules'
ALLOWED_EXTENSIONS = set(['py'])

app = Flask(__name__, static_url_path='')
app.secret_key= b'p\x03z\xaf*\xe6*:\xd8\x82\xfc\xb5<;\xbe\xd3\xe9s\xcbM\x01\xbe\xfbm'

app.config['LIB_UPLOAD_FOLDER'] = LIB_UPLOAD_FOLDER
app.config['MODULES_UPLOAD_FOLDER'] = MODULES_UPLOAD_FOLDER
for blue in blueprints:
    app.register_blueprint(blue)


@app.route('/exploit/<name>/<period>', methods=["POST", "DELETE"])
def exploit(name, period):
    # conf = ExploitConfig()
    if request.method == 'POST':
        # Exploit with <name> and <period> should be excuted after scheduling here
        # Exploit should be in the file with <name> in the same folder
        # conf.put(name, "period", period)
        addE = {'status': 'ok'}
        return json.dumps(addE)
    else:

        # Exploit with name = <name> should be stopped here
        # conf.remove(name)
        deleteE = {'status': 'ok'}
        return json.dumps(deleteE)


@app.route('/exploitResult', methods=["POST"])
def result():
    # so should implement result(a json object) of all exploit with its status sofar
    # for example there are current ex1, ex2, ex3
    results = {'ex1': 'SUCESS', 'ex2': 'FAILED', 'ex3': 'IS RUNNING'}
    return json.dumps(results)


@app.route('/addTarget/<name>/<user>/<password>', methods=["POST"])
def target(name, user, password):
    # Target should be added and saved here
    resp = Response("post request")
    return resp

@app.route('/exploit/all', methods=["GET"])
def getAllExploits():
    f = []
    for (dirpath, dirnames, filenames) in walk(app.config['LIB_UPLOAD_FOLDER']):
        f.extend(filenames)
        break
    return jsonify({'data': f})

@app.route('/exploit/delete/<string:file_name>', methods=["DELETE"])
def exploitDelete(file_name):
    if request.method == 'DELETE':
        os.remove(os.path.join(app.config['LIB_UPLOAD_FOLDER'], file_name))
        local = salt.client.LocalClient()
        local.cmd('*', 'cmd.run', ['rm ~/lib/' + file_name])
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
            file.save(os.path.join(app.config['LIB_UPLOAD_FOLDER'], filename))
            local = salt.client.LocalClient()
            ret = local.cmd('*', 'state.sls', ['cplib', 'saltenv=ctf'])
            return 'succesfully added ' + file.filename

        return ''

@app.route('/module/delete/<string:file_name>', methods=["DELETE"])
def moduleDelete(file_name):
    if request.method == 'DELETE':
        os.remove(os.path.join(app.config['MODULES_UPLOAD_FOLDER'], file_name))
        local = salt.client.LocalClient()
        local.cmd('*', 'cmd.run', ['rm ~/modules/' + file_name])
        return 'succesfully deleted ' + file_name


@app.route('/module/upload', methods=["POST"])
def moduleUpload():
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
            file.save(os.path.join(app.config['MODULES_UPLOAD_FOLDER'], filename))
            local = salt.client.LocalClient()
            ret = local.cmd('*', 'state.sls', ['cpmodules', 'saltenv=ctf'])
            return 'succesfully added ' + file.filename

        return ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run():
    port = 4567
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)
