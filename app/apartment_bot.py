#!/usr/bin/env python3

import requests

EVENT_TYPE = 'app_mention'
EVENT_TEXT = 'Look for apartments'

def main(config, event):
    if event['type'] != EVENT_TYPE:
        return { 'error': 'Invalid event type', 'success': False }
    if event['text'].find(EVENT_TEXT) == -1:
        return { 'error': 'Invalid message string', 'success': False }

    url = 'https://slack.com/api/chat.postMessage'
    data = {
        'text': 'I\'m sorry, you need to trigger `/apartment-search` yourself',
        'channel': event['channel']
    }
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(config['SLACK']['TOKEN'])
    }
    r = requests.post(url, json=data, headers=headers)
    return r

if __name__ == "__main__":
    main()
