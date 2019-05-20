#!/usr/bin/env python3

import csv

def to_csv(date, data_array):
    count = 0
    file_path = 'apartments_' + date + '.csv'
    apt_data = open(file_path, 'w')
    csvwriter = csv.writer(apt_data)
    for apt in data_array:
        if count == 0:
            header = apt.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(apt.values())
    apt_data.close()
    return file_path
