#!/usr/bin/env python3

from heyvector import db


class Repository(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'owner', name='unique_owner_repo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '%s/%s' % (self.owner, self.name)
