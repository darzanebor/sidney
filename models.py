#!/usr/bin/env python3
"""models"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class thumbnail(db.Model):
    __tablename__ = 'thumbnail'
    id       = db.Column('id', db.Integer, primary_key=True)
    location = db.Column(db.String(), index=False, unique=True, nullable=False)
    link     = db.Column(db.String(), index=False, unique=True, nullable=False)
    size     = db.Column(db.String(), index=False, unique=True, nullable=False)
    mtype    = db.Column(db.String(), index=False, unique=True, nullable=False)
    hash    = db.Column(db.String(), index=False, unique=True, nullable=False)

    def __init__(self, location, link, size, hash, mtype):
        self.location = location
        self.link     = link
        self.size     = size
        self.hash     = hash
        self.mtype    = mtype

    def __repr__(self):
        return '<thumbnail {}>'.format(self.link)