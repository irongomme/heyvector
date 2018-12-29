#!/usr/bin/env python3

from heyvector import cache, github


@cache.memoize(50)
def user_repositories(user):
    return github.get('/users/%s/repos' % user,
        params = {
            'visibility': 'public',
            'affiliation': 'owner',
            'sort': 'created'})
