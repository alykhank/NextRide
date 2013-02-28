#!/usr/bin/env python

import json, os, getSchedule
from flask import Flask, request, jsonify, send_from_directory, abort

app = Flask(__name__)

@app.route('/')
def root():
	return send_from_directory('public', 'index.html')

@app.route('/get')
def get():
	stop = request.args.get('stop', '')
	if stop is '' or not stop.isdigit():
		abort(400)
	schedule = getSchedule.parseSchedule(getSchedule.getRides(stop))
	return jsonify(schedule)

@app.errorhandler(400)
def bad_request(error):
	return send_from_directory('public', 'bad_request.html'), 400

@app.errorhandler(404)
def not_found(error):
	return send_from_directory('public', 'not_found.html'), 404

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
