#!/usr/bin/env python3

import os
import json

class Config:
    def __init__(self):
        configs = self.__get_config()
        for (c, v) in configs.items():
            setattr(self, c, v)

    def __get_env_config(self, key):
        # using get will return `None` if a key is not present rather than raise a `KeyError`
        return os.environ.get(key)

    def __fallback_config(self):
        file_name = 'config.json'
        root_path = os.path.dirname(__file__)
        file_path = os.path.join(root_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                config = json.load(f)
            return config
        return {}

    def __get_config(self):
        configs = self.__fallback_config()
        for env_config in self.__ENV_CONFIGS:
            c = self.__get_env_config(env_config)
            if c is not None:
                try:
                    configs[env_config] = json.loads(c)
                except ValueError:
                    configs[env_config] = c
        return configs

    __ENV_CONFIGS = [
        'APARTMENTS',
        'EMAIL',
        'SLACK',
        'GOOGLE_CHROME_BIN',
        'CHROMEDRIVER_PATH'
    ]
