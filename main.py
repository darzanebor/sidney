#!/usr/bin/env python3
import os
import io
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, make_response, jsonify, redirect, send_file, abort

application = Flask(__name__ , template_folder="templates")
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class thumbnail(db.Model):
    __tablename__ = 'thumbnail'
    id       = db.Column('id', db.Integer, primary_key=True)
    location = db.Column(db.String(), index=False, unique=True, nullable=False)
    link     = db.Column(db.String(), index=False, unique=True, nullable=False)

    def __init__(self, location, link):
        self.location = location
        self.link     = link

    def __repr__(self):
        return '<thumbnail {}>'.format(self.link)


@application.errorhandler(404)
def resource_not_found(exception):
    """Page not found."""
    return jsonify(str(exception)), 404

@application.errorhandler(403)
def resource_forbidden(exception):
    """Forbidden."""
    return jsonify(str(exception)), 403

@application.route("/index.html")
def default_page():
    """Index page"""
    return make_response(render_template("index.html"), 200)

@application.route("/",methods=["GET", "POST"])
def req_handler():
#    """GET/POST requests handler"""
#    try:
        if request.method == "GET":
            thumbnail_link = request.args.get('thumbnail_link')
            if thumbnail_link or thumbnail_link != "":
                existing_thumbnail = thumbnail.query.filter(thumbnail.link == thumbnail_link).first()
                if existing_thumbnail:
                    image = Image.open(existing_thumbnail.location)
                    file_object = io.BytesIO()
                    image.save(file_object, image.format)
                    file_object.seek(0)
                    return send_file(file_object, mimetype="*/*")
                else:
                    return make_response(render_template("index.html"), 203)
            return make_response(render_template("index.html"), 200)
        if request.method == "POST":
             new_thumbnail = thumbnail(location="/home/alien/Projects/cookie/img/cat.jpg", link="012")
             db.session.add(new_thumbnail)
             db.session.commit()
             print (thumbnail.query.all())
             return ''
        return ''
#    except:
#        print("Error in req_handler()")
#        return abort(404)

if __name__ == "__main__":
    application.run(threaded=True)
    db.init_app(application)