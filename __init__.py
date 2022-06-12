from flask import Flask,HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()