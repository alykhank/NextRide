#!/usr/bin/env python

import json, os, getSchedule
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__)

@app.route('/')
def root():
	return render_template('index.html')

@app.route('/get')
def get():
	stop = request.args.get('stop', '')
	if stop is '' or not stop.isdigit():
		abort(400)
	schedule = getSchedule.parseSchedule(getSchedule.getRides(stop))
	return jsonify(schedule)

@app.errorhandler(400)
def bad_request(error):
	return render_template('bad_request.html'), 400

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
