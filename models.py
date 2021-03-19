#!/usr/bin/env python3
"""models"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class thumbnail(db.Model):
    __tablename__ = 'thumbnail'
    id   = db.Column('id', db.Integer, primary_key=True)
    url  = db.Column(db.String(), index=False, unique=True, nullable=False)
    path = db.Column(db.String(), index=False, unique=True, nullable=False)
    link = db.Column(db.String(), index=False, unique=True, nullable=False)
    size = db.Column(db.String(), index=False, unique=True, nullable=False)    
    mime = db.Column(db.String(), index=False, unique=True, nullable=False)
    hash = db.Column(db.String(), index=False, unique=True, nullable=False)

    def __init__(self, url, path, link, size, mime, hash):
        self.url      = url
        self.path     = path
        self.link     = link
        self.size     = size
        self.mime     = mime
        self.hash     = hash

    def __repr__(self):
        return '<thumbnail {}>'.format(self.link)