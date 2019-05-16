#!/usr/bin/env python3

import requests
import re

from bs4 import BeautifulSoup

APARTMENT_LINKS = [
    { 'name': 'Girard', 'url': 'https://www.equityapartments.com/boston/south-end/girard-apartments' },
    { 'name': '315 on A', 'url': 'https://www.equityapartments.com/boston/fort-point/315-on-a-apartments' },
    { 'name': 'Troy', 'url': 'https://www.equityapartments.com/boston/south-end/troy-boston-apartments' }
]

def scrape(apartmentSizes):
    apartmentScrape = []

    # go thru list of buildings
    for apartmentLink in APARTMENT_LINKS:
        response = requests.get(apartmentLink['url'], timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        # check for list of apartment sizes
        for apartmentSize in apartmentSizes:
            apartments = content.find('div', attrs={"id": ("bedroom-type-" + str(apartmentSize))})

            # ensure building has search size
            if apartments is not None:
                # list of apartments is expected to be in <li> elements
                for apartment in apartments.findAll('li', attrs={"class": "unit"}):
                    apartmentData = apartment.find('div', attrs={"class": "specs"})

                    # ensure apartment has specs defined
                    if apartmentData is not None:
                        apartmentObject = {
                            'Building': apartmentLink['name']
                        }

                        for i, apartmentSpecs in enumerate(apartmentData.children):
                            scrapeParse(i, apartmentSpecs, apartmentObject)
                    
                        # add apartment info into list of scraped items
                        apartmentScrape.append(apartmentObject)

    # return list of scraped apartments
    return apartmentScrape

def scrapeParse(scrapeIndex, scrapeData, scrapeObject):
    if scrapeIndex == 1:
        scrapeObject['Price'] = re.sub(r'[\ \n\r]{2,}', '', scrapeData.find('span', attrs={"class": "pricing"}).text)
    elif scrapeIndex == 3:
        scrapeObject['Bd'] = re.sub(r'[\ \n\r]{1,}', '', re.sub(' Bed', '', scrapeData.text.split('/')[0]))
        scrapeObject['Bth'] = re.sub(r'[\ \n\r]{1,}', '', re.sub(' Bath', '', scrapeData.text.split('/')[1]))
    elif scrapeIndex == 5:
        scrapeObject['Size (sq.ft.)'] = re.sub(r'[\ \n\r]{1,}', '', re.sub('sq.ft.', '', scrapeData.text.split('/')[0]))
        scrapeObject['Floor'] = re.sub(r'[\ \n\r]{1,}', '', re.sub('Floor ', '', scrapeData.text.split('/')[1]))
    elif scrapeIndex == 7:
        scrapeObject['Available'] = re.sub(r'[\ \n\r]{2,}', '', re.sub('Available ', '', scrapeData.text))

    return scrapeObject
