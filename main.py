#!/usr/bin/env python3
"""SIDNEY(COOKIE MONSTER) IMAGE MANAGER"""
import os
import io
from PIL import Image
from flask import (
    Flask,
    request,
    render_template,
    make_response,
    jsonify,
    redirect,
    send_file,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from models import thumbnail

application = Flask(__name__, template_folder="templates")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/app.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(application)

@application.route("/", methods=["GET", "POST"])
def req_handler():
    #    """GET/POST requests handler"""
    #    try:
    if request.method == "GET":
        thumbnail_link = request.args.get("thumbnail_link")
        if thumbnail_link or thumbnail_link != "":
            existing_thumbnail = thumbnail.query.filter(thumbnail.link == thumbnail_link).first()
            if existing_thumbnail:
                view = request.args.get("view")
                if view != "full":
                    image = Image.open(existing_thumbnail.location)
                    file_object = io.BytesIO()
                    image.save(file_object, image.format)
                    file_object.seek(0)
                    return send_file(file_object, mimetype="*/*")
                return make_response(render_template("thumbnail_info.html"), 200)        
    if request.method == "POST":
        new_thumbnail = thumbnail(location="/home/alien/Projects/cookie/img/cat.jpg", link="012", size="56000", mtype="image/jpeg", hash="None")
        db.session.add(new_thumbnail)
        db.session.commit()
        print(thumbnail.query.all())
        return make_response(render_template("thumbnail_info.html"), 200)
    return redirect("/index.html", code=302)
#    except:
#        print("Error in req_handler()")
#        return abort(404)

@application.errorhandler(500)
def resource_error(exception):
    """Internal Error."""
    return jsonify(str(exception)), 500

@application.errorhandler(405)
def method_forbidden(exception):
    """Method Not Allowed."""
    return jsonify(str(exception)), 405


@application.errorhandler(404)
def resource_not_found(exception):
    """Page not found."""
    return jsonify(str(exception)), 404


@application.errorhandler(403)
def resource_forbidden(exception):
    """Forbidden."""
    return jsonify(str(exception)), 403

@application.route("/index.html")
def default_index():
    """Index page"""
    return make_response(render_template("index.html"), 200)


if __name__ == "__main__":
    application.run(threaded=True)
    db.init_app(application)
