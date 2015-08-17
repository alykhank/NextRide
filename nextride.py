#!/usr/bin/env python

import os

import requests
from flask import Flask, request, jsonify, render_template, abort

from scraper import scrape

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/m")
def mobile():
    stop = request.args.get("stop", 1, type=int)
    schedule = scrape(stop)
    if schedule:
        response = dict(meta=dict(status=200, message="OK"), data=schedule)
    else:
        abort(400)
    return render_template("m.html", path=response)


@app.route("/api")
def api():
    stop = request.args.get("stop", 1, type=int)
    schedule = scrape(stop)
    if schedule:
        response = jsonify(meta=dict(status=200, message="OK"), data=schedule)
    else:
        abort(400)
    return response

@app.errorhandler(400)
def bad_request(error):
    response = jsonify(meta=dict(status=error.code, message=error.message))
    return response, error.code

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
