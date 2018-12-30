#!/usr/bin/env python3

from flask import render_template, session, redirect
from heyvector import app, db, github
from heyvector.auth_module.utils import login_required
from heyvector.repos_module.models import Repository
from heyvector.repos_module.utils import list_user_repositories, get_user_repository


@app.route('/explore', endpoint = 'explore')
def explore():
    return render_template('explore.html')


@app.route('/share', endpoint = 'share')
@login_required
def contributions():
    username = session.get('user').get('login')
    user_shared_repos = []
    user_unshared_repos = []
    imported_repos = Repository.query.filter_by(owner=username).all()

    for repo in list_user_repositories(username):
        if repo.get('name') in imported_repos.__repr__():
            user_shared_repos.append(repo)
        else:
            user_unshared_repos.append(repo)

    return render_template('share.html',
        shared_repos = user_shared_repos,
        unshared_repos = user_unshared_repos)


@app.route('/share/<repository>', endpoint = 'share_repo')
@login_required
def add_repository(repository):
    current_username = session.get('user').get('login')
    github_repo = get_user_repository(current_username, repository)
    repo = Repository(id = github_repo.get('id'), name = github_repo.get('name'), owner = current_username)
    db.session.add(repo)
    db.session.commit()

    return redirect('share')

@app.route('/unshare/<repository>', endpoint = 'unshare_repo')
@login_required
def remove_repository(repository):
    current_username = session.get('user').get('login')
    github_repo = get_user_repository(current_username, repository)
    repo = Repository.query.get(github_repo.get('id'))
    db.session.delete(repo)
    db.session.commit()

    return redirect('share')
