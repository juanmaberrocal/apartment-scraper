#!/usr/bin/env python3

from flask import Flask, request

from app.config import Config
from app.router import Router

app = Flask(__name__)
config = Config()
router = Router(config)

@app.route("/slackbot", methods=['POST'])
def slackbot():
    return router.slackbot(request.json)

@app.route("/email", methods=['POST'])
def email():
    return router.email(request.json)

@app.route("/slack-event", methods=['POST'])
def slack_event():
    return router.slack_event(request.json)
