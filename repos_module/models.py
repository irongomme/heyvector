#!/usr/bin/env python3

from heyvector import db
from datetime import datetime


class Repository(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'owner', name='unique_owner_repo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(6), nullable=False)
    entrypoint = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '%s/%s' % (self.owner, self.name)
