#!/usr/bin/env python3

import requests
import re
from datetime import datetime

from bs4 import BeautifulSoup

APARTMENT_LINKS = [
    { 'name': 'Waterside Place', 'url': 'https://www.watersideboston.com/search-property/' }
]

def scrape(apartment_sizes):
    apartment_scrape = []

    # go thru list of buildings
    for apartment_link in APARTMENT_LINKS:
        response = requests.get(apartment_link['url'], timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        # list of apartments is expected to be in <div> elements
        apartments = content.find('div', attrs={'class': 'property-result'})

        if apartments is not None:
            for apartment in apartments.findAll('div', attrs={'class': 'property-box-area'}):
                apartment_data = apartment.find('div', attrs={'class': 'property-price'})

                # ensure apartment has specs defined
                if apartment_data is not None:
                    apartment_object = {
                        'Building': apartment_link['name']
                    }

                    apartment_specs = apartment_data.p
                    scrape_parse(apartment_specs, apartment_object)

                    # add apartment info into list of scraped items
                    if int(apartment_object['Bd']) in apartment_sizes:
                        apartment_scrape.append(apartment_object)

    # return list of scraped apartments
    return apartment_scrape

def scrape_parse(scrape_data, scrape_object):
    price = re.search(r'(\$\d+,\d+).\d+', scrape_data.text)
    scrape_object['Price'] = price.group(1) if price else 'N/A'

    bd = re.search(r'(\d+) BED', scrape_data.text)
    scrape_object['Bd'] = bd.group(1) if bd else 'N/A'

    bth = re.search(r'(\d+) BATH', scrape_data.text)
    scrape_object['Bth'] = bth.group(1) if bth else 'N/A'

    size = re.search(r'(\d+) SQ\. FT\.', scrape_data.text)
    scrape_object['Size (sq.ft.)'] = size.group(1) if size else 'N/A'

    scrape_object['Floor'] = 'N/A'

    avail = re.search(r'AVAILABLE (\w+(\.\d+,\d+)?)', scrape_data.text)
    avail = avail.group(1) if avail else 'N/A'
    if avail == 'NOW':
        avail = datetime.now().strftime("%m/%d/%Y")
    elif avail != 'N/A':
        avail = datetime.strptime(avail, '%b.%d,%Y').strftime("%m/%d/%Y")
    scrape_object['Available'] = avail

    return scrape_object
