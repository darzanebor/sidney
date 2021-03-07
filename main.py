#!/usr/bin/env python3
"""COOKIE"""
from io import BytesIO
import io
import os
import base64
import hashlib
import requests
from PIL import Image
from flask import Flask, request, send_file, render_template, make_response, abort, jsonify

application = Flask(__name__ , template_folder="templates")

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
    """GET/POST requests handler"""
    try:
        if request.method == "GET":
            return ''
        if request.method == "POST":
            return ''
        return ''
    except:
        print("Error in req_handler()")
        return abort(404)

if __name__ == "__main__":
    application.run(threaded=True)
