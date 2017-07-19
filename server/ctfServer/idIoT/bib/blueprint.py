#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bib = Blueprint('bib', __name__, template_folder='templates')


@bib.route('/bib')
def show():
    try:
        # return render_template('pages/%s.html' % page)
        return "Biblio!"
    except TemplateNotFound:
        abort(404)
