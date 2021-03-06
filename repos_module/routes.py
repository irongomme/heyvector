#!/usr/bin/env python3

from flask import request, render_template, session, redirect, jsonify
from datetime import datetime
from heyvector import app, db, github
from heyvector.auth_module.utils import login_required
from heyvector.repos_module.models import Repository
from heyvector.repos_module.utils import list_user_repositories, get_user_repository


@app.route('/explore', endpoint = 'repos.explore')
def explore():
    return render_template('explore.html')


@app.route('/share', endpoint = 'repos.share')
@login_required
def contributions():
    return render_template('share.html')


@app.route('/share/<repository>', endpoint = 'repos.ajax.share', methods=['POST'])
@login_required
def add_repository(repository):
    if request.method == "POST":
        current_username = session.get('user').get('login')
        github_repo = get_user_repository(current_username, repository)
        values = request.get_json()
        try:
            repo = Repository(id = github_repo.get('id'), name = github_repo.get('name'), owner = current_username,
                              version = values.get('version'), entrypoint = values.get('entrypoint'),
                              description = github_repo.get('description'))
            db.session.add(repo)
            db.session.commit()
            result = True
        except:
            result = False

    return jsonify({"success": result or False})


@app.route('/share_update/<repository>', endpoint = 'repos.ajax.update', methods=['POST'])
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
            repo.description = github_repo.get('description')
            repo.updated = datetime.now()
            db.session.commit()
            result = True
        except:
            result = False

    return jsonify({"success": result or False})


@app.route('/unshare/<repository>', endpoint = 'repos.ajax.unshare')
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


@app.route('/repos/user_all', endpoint = 'repos.ajax.user_list')
@login_required
def list_repositories():
    current_username = session.get('user').get('login')
    user_repositories = list_user_repositories(current_username, **request.args)
    shared_repositories = Repository.query.filter_by(owner=current_username).all()
    for repository in user_repositories:
        if repository.get('name') in shared_repositories.__repr__():
            shared_repository = Repository.query.get(repository.get('id'))
            repository['shared_version'] = shared_repository.version
            repository['is_shared'] = True
        else:
            repository['is_shared'] = False

    return jsonify(user_repositories)


@app.route('/repos/all', endpoint = 'repos.ajax.list')
def list():
    page = int(request.args['page'])
    per_page = int(request.args['per_page'])
    offset = (page-1) * per_page
    short_repositories = Repository.query \
        .limit(per_page) \
        .offset(offset) \
        .all()
    full_repositories = []

    for repository in short_repositories:
        full_repository = get_user_repository(repository.owner, repository.name)
        full_repository['version'] = repository.version
        full_repository['created'] = repository.created
        full_repository['updated'] = repository.updated
        full_repository['description'] = repository.description
        full_repositories.append(full_repository)

    return jsonify(full_repositories)


@app.route('/repos/count', endpoint = 'repos.ajax.count')
def count():
    count = Repository.query.count()

    return jsonify({'count': count})
