#!/usr/bin/env python3

import os
from datetime import datetime

from app.modules import mailer
from app.modules import parsedata
from app.modules import slack
from app.modules import webscraper

from app.helpers.csv import to_csv
from app.helpers.json import to_json
from app.helpers.table import to_table

def set_config():
    file_name = 'config.json'
    root_path = os.path.dirname(__file__)
    file_path = os.path.join(root_path, file_name)

    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

def set_date():
    now  = datetime.now()
    return now.strftime("%Y-%m-%d")

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

    # if (needs_mail(date, scrape_json)):
    #     file_path = to_csv(date, scrape_json)
    #     mailer.send(date, len(scrape_json), file_path, config['EMAIL'])
    # else:
    #     print('No new data to send')

    table_data = to_table(scrape_json)
    return slack.send(config['SLACK']['URL'], table_data)

if __name__ == "__main__":
    main()
