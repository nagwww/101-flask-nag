#!/usr/bin/env python

import json
from flask import Flask, Response, abort, jsonify, request,send_from_directory,render_template,send_file
from flask.ext.autoindex import AutoIndex
import os

app = Flask(__name__)
app.config['DIRECTORY'] = "./data"
ROOT="/var/log"
app.config['FILE'] = "nag.json"

AUTOINDEX = AutoIndex(app, browse_root=ROOT, add_url_rules=False)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/status")
def status():
        return jsonify({'success': True})

@app.route("/data")
def data():
        CLIENT_REPORT = []
        ipp = open('./data/nag.txt', 'r')
        for line in ipp:
             print line
             client = {}
             ip = line.split(",")
             client["name"]=ip[0].rstrip("\r\n")
             client["title"]=ip[1].rstrip("\r\n")
             CLIENT_REPORT.append(client)
             print CLIENT_REPORT
        return Response(json.dumps(CLIENT_REPORT),  mimetype='application/json')

@app.route('/dir')
def dir():
    path = request.args.get('path', None)
    if path is not None:
        return send_file(ROOT + "/" + path)
    return AUTOINDEX.render_autoindex('.', browse_root=ROOT , endpoint=dir)


@app.route("/file")
def file():
        filename = "{}/{}".format(app.config['DIRECTORY'], "nag.json")
        print filename
        if not os.path.isfile(filename):
                abort(404)
        print filename
        return send_from_directory(app.config['DIRECTORY'], app.config['FILE'])


@app.errorhandler(500)
def error_500(_):
    """500 handler"""
    return render_template('500.html'), 500

@app.errorhandler(404)
def error_404(_):
    """404 handler"""
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.debug = False
	app.run(host="0.0.0.0", port=7101, debug="true", use_reloader=False)

