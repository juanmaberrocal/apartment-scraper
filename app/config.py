#!/usr/bin/env python3

import os
import json

ENV_CONFIGS = [
    'APARTMENTS',
    'EMAIL',
    'SLACK'
]

def get_env_config(key):
    # using get will return `None` if a key is not present rather than raise a `KeyError`
    return os.environ.get(key)

def fallback_config():
    file_name = 'config.json'
    root_path = os.path.dirname(__file__)
    file_path = os.path.join(root_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            config = json.load(f)
        return config
    return {}

def set_config():
    config = fallback_config()
    for env_config in ENV_CONFIGS:
        c = get_env_config(env_config)
        if c is not None:
            try:
                config[env_config] = json.loads(c)
            except ValueError:
                config[env_config] = c
    return config
