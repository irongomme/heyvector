#!/usr/bin/env python3

from heyvector import cache, github


@cache.memoize(50)
def list_user_repositories(user, **kwargs):
    return github.get('/users/%s/repos' % user,
        params = {
            'visibility': 'public',
            'affiliation': 'owner',
            'sort': 'created',
            **kwargs})

@cache.memoize(50)
def get_user_repository(user, repository):
    return github.get('/repos/%s/%s' % (user, repository),
        params = {
            'type' : 'owner',
            'sort' : 'updated'})
