#!/usr/bin/env python3

from datetime import datetime
import json
import csv

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

def main():
    config = setConfig()
    date = setDate()

    scrapeJson = webscraper.scrape(config['APARTMENTS'])
    scrapeJson = parsedata.parse(scrapeJson, config['APARTMENTS']['FILTERS'])

    if len(scrapeJson) > 0:
        file_path = toCsv(date, scrapeJson)
        mailer.send(date, len(scrapeJson), file_path, config['EMAIL'])

if __name__ == "__main__":
    main()
