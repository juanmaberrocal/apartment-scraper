#!/usr/bin/env python3

import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

from app.classes.selenium_chrome import SeleniumChrome

APARTMENT_LINKS = [
    { 'name': 'Park Lane Seaport', 'url': 'https://www.parklaneseaport.com/floorplans/bedrooms--1' },
    { 'name': 'Park Lane Seaport', 'url': 'https://www.parklaneseaport.com/floorplans/bedrooms--2' }
]

def scrape(apartment_sizes):
    apartment_scrape = []

    # go thru list of buildings
    for apartment_link in APARTMENT_LINKS:
        chrome = SeleniumChrome()
        chrome.get_url(apartment_link['url'])

        try:
            element = chrome.get_element_by_id('floorplanCards')
            content = element.get_attribute('innerHTML')
        finally:
            chrome.quit()

        if content is None:
            continue

        apartments = BeautifulSoup(content, "html.parser")

        for apartment in apartments.findAll('div', attrs={'class': 'fp-card'}):
            apartment_object = {
                'Building': apartment_link['name']
            }

            scrape_parse(apartment, apartment_object)

            # add apartment info into list of scraped items
            if apartment_object['Price'] != 'N/A':
                apartment_scrape.append(apartment_object)

    # return list of scraped apartments
    return apartment_scrape

def scrape_parse(scrape_data, scrape_object):
    details_div = scrape_data.find('div', attrs={'class': 'fp-detail'})
    price_div = scrape_data.find('div', attrs={'class': 'fp-price'})
    avail_div = scrape_data.find('div', attrs={'class': 'fp-availability'})

    price = price_div.find('span', attrs={'class': 'amount'}) if price_div else None
    scrape_object['Price'] = re.search(r'(\$\d+,\d+).\d+', price.text).group(1) if price else 'N/A'

    bd_bth = details_div.find('span', attrs={'class': 'fp-type'}) if details_div else None
    bd = re.search(r'(\d+) Bed', bd_bth.text).group(1) if bd_bth else 'N/A'
    bth = re.search(r'(\d+) Bath', bd_bth.text).group(1) if bd_bth else 'N/A'
    scrape_object['Bd'] = bd
    scrape_object['Bth'] = bth


    sq_ft = details_div.find('span', attrs={'class': 'fp-sqft'}) if details_div else None
    sqft = re.search(r'(\d+) sq ft', sq_ft.text).group(1) if sq_ft else 'N/A'
    scrape_object['Size (sq.ft.)'] = sqft

    scrape_object['Floor'] = 'N/A'

    avail = re.search(r'Available On: (\d+\/\d+\/\d+)', avail_div.text) if avail_div else None
    avail = avail.group(1) if avail else 'N/A'
    scrape_object['Available'] = avail

    return scrape_object
