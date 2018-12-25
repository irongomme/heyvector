#!/usr/bin/env python3

from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if is_authenticated() is False:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view

def is_authenticated():
    return session.get('user', None) is not None
