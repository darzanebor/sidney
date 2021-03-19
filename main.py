#!/usr/bin/env python3
"""SIDNEY(COOKIE MONSTER) IMAGE MANAGER"""
from io import BytesIO
import os
import io
import re
import base64
import magic
import requests
from PIL import Image
from flask_xcaptcha import XCaptcha
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    request,
    render_template,
    make_response,
    jsonify,
#    redirect,
    send_file,
    abort,
)
from models import thumbnail

application = Flask(__name__, template_folder="templates")
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/app.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SIDNEY_COOKIE"] = "http://localhost:5001"
application.config["XCAPTCHA_SITE_KEY"] = ""
application.config["XCAPTCHA_SECRET_KEY"] = ""
application.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 10
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
        mime = magic.from_buffer(stream.read(2048), mime=True)
        stream.seek(0)
        return mime
    except:
        print("Error in get_image_mime()")
        return abort(500)


def image_to_object(image, image_format=None):
    """Convert Image to Object"""
    try:
        file_object = io.BytesIO()
        image.save(file_object, image_format)
        file_object.seek(0)
        return file_object
    except:
        print("Error in image_to_object()")
        return abort(500)


def image_check(image_url):
    """Uploaded file checks"""
    try:
        headers = {"Range": "bytes=0-2048"}
        req = requests.get(image_url, headers=headers, allow_redirects=True, timeout=5)
        if req.status_code != 206:
            abort(req.status_code)
        content_length = int(req.headers.get("content-length", None))
        content_type = req.headers.get("content-type")
        image_head = BytesIO(req.content)
        mime = get_image_mime(image_head)  # get mime type from uploaded file
        if content_type != mime:
            abort(403, "Content missmatch")
        if content_length > application.config["COOKIE_IMAGE_MAX_SIZE"]:
            abort(403, "Image is too large")
        return True
    except:
        print("Error in image_check()")
        return abort(500)


def is_valid_url(url_list):
    """Validate url by regexp"""
    regex = re.compile(r"^((http|https)?(:\D{2})).*$", re.IGNORECASE)
    if isinstance(url_list, list):
        for url in url_list:
            if not bool(regex.search(url)):
                return False
    elif isinstance(url_list, str):
        return bool(regex.search(url_list))
    return True


@application.route("/", methods=["GET", "POST"])
def req_handler():
    """GET/POST requests handler"""
    try:
        if request.method == "GET":
            thumbnail_id = request.args.get("thumbnail_id")
            if thumbnail_id or thumbnail_id != "":
                # if redis_cache_enabled:
                # load from redis cache
                existing_thumbnail = thumbnail.query.filter(thumbnail.link == thumbnail_id).first()
                if existing_thumbnail:
                    view = request.args.get("view")
                    if view != "full":
                        image = Image.open(existing_thumbnail.location)
                        return send_file(image_to_object(image, image.format), mimetype="*/*")
                    return make_response(render_template("thumbnail_info.html"), 200)
        if request.method == "POST":
            if captcha_verify():
                uploaded_images = request.files.getlist("image_file")
                uploaded_urls = request.form.getlist("image_url")
                if is_valid_url(uploaded_urls):
                    for uploaded_url in uploaded_urls:
                        params = {'url':base64.b64encode(uploaded_url.encode())}
                        req = requests.get(
                            url=application.config["SIDNEY_COOKIE"],
                            params=params,
                            stream=True,
                            timeout=60
                        )
                        if req.status_code == 200:
                            raw_image = Image.open(io.BytesIO(req.content))
                            return_image = image_to_object(raw_image,raw_image.format)
                            mime_type = Image.MIME[raw_image.format]

                            #тумб в базу и добавляем в JSON для рендера в thumbnail_info.html
                    return make_response(render_template("thumbnail_info.html"), 200)
                if uploaded_images or any(f for f in uploaded_images):
                    for uploaded_image in uploaded_images:
                        file_name = uploaded_image.filename
                        file_ext = os.path.splitext(file_name)[1]
                        if file_name != "" and file_ext in application.config["UPLOAD_EXTENSIONS"]:
                            mime_type = get_image_mime(uploaded_image)

                            #тумб в базу и добавляем в JSON для рендера в thumbnail_info.html

                    return make_response(render_template("thumbnail_info.html"), 200)
        return make_response(render_template("index.html"), 200)
    except:
        print("Error in req_handler()")
        return abort(404)
    #GET #return send_file(return_image,mimetype=mime_type,as_attachment=False)
    #POST #return send_file(image_to_object(uploaded_image),mimetype=mime_type,as_attachment=False)

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
