#!/usr/bin/env python3

import requests

def send(url, data, headers=None):
    headers = headers if headers is not None else {'Content-type': 'application/json'}
    data = {
        # 'username': 'apartment-scraper',
        # 'icon_emoji': ':house:',
        'text': '```{}```'.format(data)
    }

    return requests.post(url, json=data, headers=headers)
    
