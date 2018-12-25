#!/usr/bin/env python3

from flask import render_template, request, redirect, flash, url_for, g, session
from heyvector import app, db, bcrypt, github
from heyvector.auth_module.models import User
from heyvector.auth_module.utils import is_authenticated


@app.context_processor
def inject_user():
    if 'user' in session:
        return dict(user = session['user'], is_authenticated = is_authenticated())

    return dict(user = None)

@app.route('/signin', endpoint = 'auth.login', methods=['GET', 'POST'])
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'

@app.route('/signout', endpoint = 'auth.logout', methods=['GET'])
def logout():
    session.pop('user', None)
    session.pop('oauth_token', None)
    return redirect(url_for('index'))

@app.route('/github')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    session['oauth_token'] = oauth_token
    session['user'] = github.get('user')

    return redirect(next_url)


@github.access_token_getter
def token_getter():
    return session['oauth_token']
