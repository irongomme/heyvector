#!/usr/bin/env python3

from heyvector import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    github_access_token = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.username
