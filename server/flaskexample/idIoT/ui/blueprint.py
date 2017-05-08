#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
test = "Hmpf"
ui = Blueprint('ui', __name__,
                        template_folder='templates')

@ui.route('/', defaults={'page': 'index'})
@ui.route('/<page>')
def show(page):
    try:
        # return render_template('pages/%s.html' % page)
        return "Hallo!"
    except TemplateNotFound:
        abort(404)
