#!/usr/bin/env python3

from flask import jsonify

from app import apartment_scraper
from app import apartment_bot

class Router:
    def __init__(self, configs):
        self.configs = configs

    def slackbot(self, args):
        r = apartment_scraper.main(self.configs)
        if r:
            resp = jsonify({ 'success': True })
        else:
            resp = jsonify({ 'error': r.text, 'success': False })
        resp.status_code = r.status_code
        return resp

    def email(self, args):
        resp = jsonify({ 'error': 'Not Authorized', 'success': False })
        resp.status_code = 401
        return resp

    def slack_event(self, args):
        content = args
        
        if content['type'] == 'url_verification':
            resp = jsonify({ 'challenge': content['challenge'] })
            resp.status_code = 200
        elif content['type'] == 'event_callback':
            r = apartment_bot.main(self.configs, content['event'])
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
