#!/usr/bin/env python3

import requests
import re

from bs4 import BeautifulSoup

APARTMENT_LINKS = [
    { 'name': 'Girard', 'url': 'https://www.equityapartments.com/boston/south-end/girard-apartments' },
    { 'name': '315 on A', 'url': 'https://www.equityapartments.com/boston/fort-point/315-on-a-apartments' },
    { 'name': 'Troy', 'url': 'https://www.equityapartments.com/boston/south-end/troy-boston-apartments' }
]

def scrape(apartment_sizes):
    apartment_scrape = []

    # go thru list of buildings
    for apartment_link in APARTMENT_LINKS:
        response = requests.get(apartment_link['url'], timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        # check for list of apartment sizes
        for apartment_size in apartment_sizes:
            apartments = content.find('div', attrs={"id": ("bedroom-type-" + str(apartment_size))})

            # ensure building has search size
            if apartments is not None:
                # list of apartments is expected to be in <li> elements
                for apartment in apartments.findAll('li', attrs={"class": "unit"}):
                    apartment_data = apartment.find('div', attrs={"class": "specs"})

                    # ensure apartment has specs defined
                    if apartment_data is not None:
                        apartment_object = {
                            'Building': apartment_link['name']
                        }

                        for i, apartment_specs in enumerate(apartment_data.children):
                            scrape_parse(i, apartment_specs, apartment_object)
                    
                        # add apartment info into list of scraped items
                        apartment_scrape.append(apartment_object)

    # return list of scraped apartments
    return apartment_scrape

def scrape_parse(scrape_index, scrape_data, scrape_object):
    if scrape_index == 1:
        scrape_object['Price'] = re.sub(r'[\ \n\r]{2,}', '', scrape_data.find('span', attrs={"class": "pricing"}).text)
    elif scrape_index == 3:
        scrape_object['Bd'] = re.sub(r'[\ \n\r]{1,}', '', re.sub(' Bed', '', scrape_data.text.split('/')[0]))
        scrape_object['Bth'] = re.sub(r'[\ \n\r]{1,}', '', re.sub(' Bath', '', scrape_data.text.split('/')[1]))
    elif scrape_index == 5:
        scrape_object['Size (sq.ft.)'] = re.sub(r'[\ \n\r]{1,}', '', re.sub('sq.ft.', '', scrape_data.text.split('/')[0]))
        scrape_object['Floor'] = re.sub(r'[\ \n\r]{1,}', '', re.sub('Floor ', '', scrape_data.text.split('/')[1]))
    elif scrape_index == 7:
        scrape_object['Available'] = re.sub(r'[\ \n\r]{2,}', '', re.sub('Available ', '', scrape_data.text))

    return scrape_object
