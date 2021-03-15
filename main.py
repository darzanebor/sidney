#!/usr/bin/env python3
"""SIDNEY(COOKIE MONSTER) IMAGE MANAGER"""
import os
import io
import magic
from PIL import Image
from flask_xcaptcha import XCaptcha
from flask_sqlalchemy import SQLAlchemy
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
from models import thumbnail

application = Flask(__name__, template_folder="templates")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/app.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SIDNEY_COOKIE"] = "http://localhost:5001"
application.config["XCAPTCHA_SITE_KEY"] = ''
application.config["XCAPTCHA_SECRET_KEY"] = ''
application.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
application.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]

db = SQLAlchemy(application)
xcaptcha = XCaptcha(application)

def captcha_verify():
    """Verify Captcha"""
    try:
        if xcaptcha.verify():
            return True
        return False
    except:
        print("Error in captcha_verify()")
        return abort(500)  

def get_image_mime(stream):
    """Get Mime Type from stream"""
    try:
        mime = magic.from_buffer(stream.read(1024), mime=True)
        stream.seek(0)
        if mime == None:
            return None
        return mime
    except:
        print("Error in get_image_mime()")
        return abort(500)

def image_to_object(image,image_format=None):
#    """Convert Image to Object"""
#    try:
        file_object = io.BytesIO()
        image.save(file_object,image_format)
        file_object.seek(0)
        return file_object
#    except:
#        print("Error in image_to_object()")
#        return abort(500)

@application.route("/", methods=["GET", "POST"])
def req_handler():
#    """GET/POST requests handler"""
#    try:
        if request.method == "GET":
            thumbnail_id = request.args.get("thumbnail_id")
            if thumbnail_id or thumbnail_id != "":
                existing_thumbnail = thumbnail.query.filter(thumbnail.link == thumbnail_id).first()
                if existing_thumbnail:
                    view = request.args.get("view")
                    if view != "full":
                        image = Image.open(existing_thumbnail.location)
                        return send_file(image_to_object(image, image.format), mimetype="*/*")
                    #if redis_cache_enabled:
#
                    return make_response(render_template("thumbnail_info.html"), 200)
        if request.method == "POST":            
            if captcha_verify():
                uploaded_images = request.files.getlist("images")
                print(uploaded_images)
                for uploaded_file in uploaded_images:
                    file_name = uploaded_file.filename
                    file_ext = os.path.splitext(file_name)[1]
                    if file_name != "" and file_ext in application.config["UPLOAD_EXTENSIONS"]:
                        image_mime_type = get_image_mime(uploaded_file)
                        return send_file(image_to_object(uploaded_file), mimetype=image_mime_type, as_attachment=False)
                        # image magic here
                        # then show picture with                        
        #               return make_response(render_template("thumbnail_info.html"), 200)
        return make_response(render_template("index.html"), 200)
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


if __name__ == "__main__":
    application.run(threaded=True)
    db.init_app(application)
