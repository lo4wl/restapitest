#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 05:44:48 2022

@author: paul
"""

from flask import Flask, request, jsonify
from flask_script import Manager
from functools import wraps
from flask_httpauth import HTTPBasicAuth
import pathlib
import configparser

directory=str(pathlib.Path(__file__).parent.resolve())
conf=configparser.ConfigParser()
conf.read(directory+'/conf.ini')
TOKEN=conf['configs']['token']

app = Flask(__name__)
manager=Manager(app)
auth=HTTPBasicAuth()

@auth.verify_password
def authenticate(username, password):
    username,password=request.headers['username'],request.headers['password']
    if username and password:
        if username == 'roy' and password == 'roy':
            return True
        else:
            return False
    return False

@app.route('/v1/login',subdomain='static',methods=['POST'])
@auth.login_required
def get_response():
	return jsonify({'token':TOKEN})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['X-Access-Tokens']
        if not token:
            return jsonify({'message:' : 'Token was not found.'}), 403
#        try:
        if token==TOKEN:
            return f(*args, **kwargs)
        else:
            return jsonify({'message' : 'Token is invalid'}), 403
    return decorated


@app.route("/", methods=['GET'], subdomain="static")
@token_required
def static_index():
    return "LUCK"

if __name__ == "__main__":
    website_url = '2example.com:5000'
    app.config['SERVER_NAME'] = website_url
#    app.host="0.0.0.0"
#   app.port=5000
#    app.debug=True
    manager.run()#, port=5000,debug=True)