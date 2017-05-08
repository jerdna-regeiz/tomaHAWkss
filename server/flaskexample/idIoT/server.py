#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from . import config

app = Flask(__name__)
for blue in config.blueprints:
    app.register_blueprint(blue)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

def run():
    port = 4567
    app.run(debug=True, port=port, host="0.0.0.0", threaded=True)

