#!/usr/bin/env python3

from flask import Flask, jsonify

from app import apartment_scraper

app = Flask(__name__)

@app.route("/slackbot", methods=['POST'])
def slackbot():
    r = apartment_scraper.main()
    if r:
        resp = jsonify({ 'success': True })
    else:
        resp = jsonify({ 'error': r.text, 'success': False })
    resp.status_code = r.status_code
    return resp

@app.route("/email", methods=['POST'])
def email():
    resp = jsonify({ 'error': 'Not Authorized', 'success': False })
    resp.status_code = 401
    return resp
