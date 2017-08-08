#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

test = "Hmpf"
ui = Blueprint('ui', __name__, template_folder='templates', static_folder='static')


@ui.route('/')
def index():
    return render_template('index.html')


@ui.route('/status')
def status():
    return render_template('status.html')


@ui.route('/monitor')
def monitor():
    return render_template('monitor.html')


@ui.route('/target')
def target():
    return render_template('target.html')


@ui.route('/exploits')
def exploits():
    return render_template('exploits.html')

@ui.route('/modules')
def exploits():
    return render_template('modules.html')
