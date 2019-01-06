#!/usr/bin/env python3

from flask import request, render_template, session, redirect, jsonify
from heyvector import app, db, github
from heyvector.auth_module.utils import login_required
from heyvector.repos_module.models import Repository
from heyvector.repos_module.utils import list_user_repositories, get_user_repository


@app.route('/explore', endpoint = 'explore')
def explore():
    short_repositories = Repository.query.all()
    full_repositories = []

    for repository in short_repositories:
        full_repositories.append(get_user_repository(repository.owner, repository.name))

    return render_template('explore.html', repositories = full_repositories)


@app.route('/share', endpoint = 'share')
@login_required
def contributions():
    return render_template('share.html')


@app.route('/share/<repository>', endpoint = 'share_repo', methods=['POST'])
@login_required
def add_repository(repository):
    if request.method == "POST":
        current_username = session.get('user').get('login')
        github_repo = get_user_repository(current_username, repository)
        values = request.get_json()
        try:
            repo = Repository(id = github_repo.get('id'), name = github_repo.get('name'), owner = current_username,
                              version = values.get('version'), entrypoint = values.get('entrypoint'))
            db.session.add(repo)
            db.session.commit()
            result = True
        except:
            result = False

    return jsonify({"success": result or False})


@app.route('/share_update/<repository>', endpoint = 'update_repo', methods=['POST'])
@login_required
def update_repository(repository):
    if request.method == "POST":
        current_username = session.get('user').get('login')
        github_repo = get_user_repository(current_username, repository)
        values = request.get_json()
        try:
            repo = Repository.query.get(github_repo.get('id'))
            repo.version =  values.get('version')
            repo.entrypoint = values.get('entrypoint')
            db.session.commit()
            result = True
        except:
            result = False

    return jsonify({"success": result or False})


@app.route('/unshare/<repository>', endpoint = 'unshare_repo')
@login_required
def remove_repository(repository):
    current_username = session.get('user').get('login')
    github_repo = get_user_repository(current_username, repository)
    try:
        repo = Repository.query.get(github_repo.get('id'))
        db.session.delete(repo)
        db.session.commit()
        result = True
    except:
        result = False

    return jsonify({"success": result or False})


@app.route('/repos/user_all', endpoint = 'ajax_repos_user_all')
@login_required
def list_repositories():
    current_username = session.get('user').get('login')
    user_repositories = list_user_repositories(current_username, **request.args)
    shared_repositories = Repository.query.filter_by(owner=current_username).all()
    for repository in user_repositories:
        repository['is_shared'] = True if repository.get('name') in shared_repositories.__repr__() else False

    return jsonify(user_repositories)
