#!/usr/bin/env python3

from flask import render_template, session
from heyvector import app, github
from heyvector.auth_module.utils import login_required
from heyvector.repos_module.utils import user_repositories


@app.route('/share', endpoint = 'share')
@login_required
def contributions():
    username = session.get('user').get('login')
    all_repos = user_repositories(username)
    return render_template('share.html', all_repos = all_repos)

@app.route('/explore', endpoint = 'explore')
def explore():
    return render_template('explore.html')
