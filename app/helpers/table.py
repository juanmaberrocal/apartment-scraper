#!/usr/bin/env python3

from tabulate import tabulate

def to_table(data_array):
    count = 0
    rows = []
    headers = []
    for apt in data_array:
        if count == 0:
            headers = apt.keys()
            count += 1
        rows.append(apt.values())
    return tabulate(rows, headers=headers)
