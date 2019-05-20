#!/usr/bin/env python3

import os
import json
import csv
from tabulate import tabulate
from datetime import datetime

import slack
import mailer
import webscraper
import parsedata

def set_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def set_date():
    now  = datetime.now()
    return now.strftime("%Y-%m-%d")

def to_json(date, data_array):
    file_path = 'apartments_' + date + '.json'
    with open(file_path, 'w') as outfile:
        json.dump(data_array, outfile)
    return file_path

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

def needs_mail(date, data_array):
    file_path = 'apartments_' + date + '.json'

    # do not send mail if no data
    if (len(data_array) == 0):
        return False

    # do not send mail if data for today already pulled
    # and data has not changed
    if file_exists(file_path) and compare_json_file(file_path, data_array):
        return False

    # create new json file with updated data
    # and return true flag to send mail
    to_json(date, data_array)
    return True

def file_exists(file_path):
    return os.path.isfile(file_path)

def compare_json_file(file_path, data_array):
    """
    Check if JSON file data is same as apartment data scraped.

    Args:
        file_path: Existing JSON dump file.
        data_array: JSON array of apartment data.

    Returns:
        Boolean True|False
    """
    is_same = False

    with open(file_path, 'r') as f:
        existing_array = json.load(f)

        for index, data in enumerate(data_array):
            if data == existing_array[index]:
                is_same = True
            if is_same:
                break

    return is_same

def main():
    config = set_config()
    date = set_date()

    scrape_json = webscraper.scrape(config['APARTMENTS'])
    scrape_json = parsedata.parse(scrape_json, config['APARTMENTS']['FILTERS'])

    table_data = to_table(scrape_json)
    slack.send(config['SLACK']['URL'], table_data)

    # if (needs_mail(date, scrape_json)):
    #     file_path = to_csv(date, scrape_json)
    #     mailer.send(date, len(scrape_json), file_path, config['EMAIL'])
    # else:
    #     print('No new data to send')

if __name__ == "__main__":
    main()
