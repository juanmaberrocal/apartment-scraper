#!/usr/bin/env python3

import json

def to_json(date, data_array):
    file_path = 'apartments_' + date + '.json'
    with open(file_path, 'w') as outfile:
        json.dump(data_array, outfile)
    return file_path
