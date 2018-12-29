#!/usr/bin/env python3

from flask import render_template
from heyvector import app


@app.route('/', endpoint = 'index')
def index():
    return render_template('index.html')
