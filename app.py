#!/usr/bin/env python3

from flask import render_template, session
from heyvector import app, github
from heyvector.auth_module.utils import login_required


@app.route('/', endpoint = 'index')
def index():
    return render_template('index.html')

@app.route('/share', endpoint = 'share')
@login_required
def contributions():
    return render_template('share.html', repos = github.get('/user/repos',
        params = {'visibility': 'public', 'affiliation': 'owner', 'sort': 'created'}))

@app.route('/explore', endpoint = 'explore')
def explore():
    return render_template('explore.html')
