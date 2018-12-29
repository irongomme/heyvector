#!/usr/bin/env python3

from flask import render_template, session, redirect
from heyvector import app, db, github
from heyvector.auth_module.utils import login_required
from heyvector.repos_module.models import Repository
from heyvector.repos_module.utils import user_repositories


@app.route('/explore', endpoint = 'explore')
def explore():
    return render_template('explore.html')


@app.route('/share', endpoint = 'share')
@login_required
def contributions():
    username = session.get('user').get('login')
    all_repos = user_repositories(username)
    imported_repos = Repository.query.filter_by(owner=username).all()

    return render_template('share.html',
        all_repos = all_repos,
        imported_repos = imported_repos)


@app.route('/share/<repository>', endpoint = 'share_repo')
@login_required
def add_repository(repository):
    current_username = session.get('user').get('login')
    github_repo = github.get('/repos/%s/%s' % (current_username, repository))
    repo = Repository(id = github_repo.get('id'), name = github_repo.get('name'), owner = current_username)
    db.session.add(repo)
    db.session.commit()

    return redirect('share')

@app.route('/unshare/<repository>', endpoint = 'unshare_repo')
@login_required
def remove_repository(repository):
    current_username = session.get('user').get('login')
    github_repo = github.get('/repos/%s/%s' % (current_username, repository))
    repo = Repository.query.get(github_repo.get('id'))
    db.session.delete(repo)
    db.session.commit()

    return redirect('share')
