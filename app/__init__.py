#!/usr/bin/env python3

from flask import Flask, request, jsonify

from app import apartment_scraper
from app import apartment_bot

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

@app.route("/slack-event", methods=['POST'])
def slack_event():
    print(request)
    print(request.json)
    content = request.json
    
    if content['type'] == 'url_verification':
        resp = jsonify({ 'challenge': content['challenge'] })
        resp.status_code = 200
    elif content['type'] == 'event_callback':
        r = apartment_bot.main(content['event'])
        if r:
            resp = jsonify({ 'success': True })
        else:
            resp = jsonify({ 'error': r.text, 'success': False })
        resp.status_code = r.status_code
        return resp
    else:
        resp = jsonify({ 'error': 'Bad Request', 'success': False })
        resp.status_code = 400
    return resp
