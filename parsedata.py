#!/usr/bin/env python3

import json
import re

DEFAULT_PRICE = 9999
DEFAULT_SQFT = 0

def parse(apartmentData, apartmentFilters = []):
    apartmentList = []

    for apartment in apartmentData:
        addApartment = False

        for apartmentFilter in apartmentFilters:
            addApartment = aptFilter(apartment, apartmentFilter)
            if addApartment == True:
                break

        if addApartment == True:
            apartmentList.append(apartment)

    return apartmentList;

def aptFilter(apartmentData, apartmentFilter):
    bedrooms = apartmentFilter['bedrooms'] if 'bedrooms' in apartmentFilter else bedroomFilterError()
    price = apartmentFilter['price'] if 'price' in apartmentFilter else DEFAULT_PRICE
    sqft = apartmentFilter['sqft'] if 'sqft' in apartmentFilter else DEFAULT_SQFT

    return (
        int(apartmentData['Bd']) == bedrooms and
        int(re.sub(r'[$,]', '', apartmentData['Price'])) < price and
        int(apartmentData['Size (sq.ft.)']) >= sqft
    )

def bedroomFilterError():
    raise ValueError('Bedroom filter required')
