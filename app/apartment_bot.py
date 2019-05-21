#!/usr/bin/env python3

import requests

from app.config import set_config

EVENT_TYPE = 'app_mention'
EVENT_TEXT = 'Look for apartments'

def main(event):
    config = set_config()
    if event['type'] != EVENT_TYPE:
        return { 'error': 'Invalid event type', 'success': False }
    if event['text'].find(EVENT_TEXT) == -1:
        return { 'error': 'Invalid message string', 'success': False }

    url = 'https://slack.com/api/chat.postMessage'
    data = { 'text': '/apartment-search' }
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(config['SLACK']['TOKEN'])
    }
    return requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    main()
