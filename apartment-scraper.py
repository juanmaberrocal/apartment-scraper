#!/usr/bin/env python3

import os
import json
import csv
from datetime import datetime

import mailer
import webscraper
import parsedata

def setConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def setDate():
    now  = datetime.now()
    return now.strftime("%Y-%m-%d")

def toJson(date, dataArray):
    file_path = 'apartments_' + date + '.json'
    with open(file_path, 'w') as outfile:
        json.dump(dataArray, outfile)
    return file_path

def toCsv(date, dataArray):
    count = 0
    file_path = 'apartments_' + date + '.csv'
    apt_data = open(file_path, 'w')
    csvwriter = csv.writer(apt_data)
    for apt in dataArray:
        if count == 0:
            header = apt.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(apt.values())
    apt_data.close()
    return file_path

def needsMail(date, dataArray):
    file_path = 'apartments_' + date + '.json'

    # do not send mail if no data
    if (len(dataArray) == 0):
        return False

    # do not send mail if data for today already pulled
    # and data has not changed
    if fileExists(file_path) and compareJsonFile(file_path, dataArray):
        return False

    # create new json file with updated data
    # and return true flag to send mail
    toJson(date, dataArray)
    return True

def fileExists(file_path):
    return os.path.isfile(file_path)

def compareJsonFile(file_path, dataArray):
    """
    Check if JSON file data is same as apartment data scraped.

    Args:
        file_path: Existing JSON dump file.
        dataArray: JSON array of apartment data.

    Returns:
        Boolean True|False
    """
    is_same = False

    with open(file_path, 'r') as f:
        existingArray = json.load(f)

        for index, data in enumerate(dataArray):
            if data == existingArray[index]:
                is_same = True
            if is_same:
                break

    return is_same

def main():
    config = setConfig()
    date = setDate()

    scrapeJson = webscraper.scrape(config['APARTMENTS'])
    scrapeJson = parsedata.parse(scrapeJson, config['APARTMENTS']['FILTERS'])

    if (needsMail(date, scrapeJson)):
        file_path = toCsv(date, scrapeJson)
        mailer.send(date, len(scrapeJson), file_path, config['EMAIL'])
    else:
        print('No new data to send')

if __name__ == "__main__":
    main()
