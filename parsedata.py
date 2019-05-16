#!/usr/bin/env python3

import json
import re

DEFAULT_PRICE = 9999
DEFAULT_SQFT = 0

def parse(apartment_data, apartment_filters = []):
    apartment_list = []

    for apartment in apartment_data:
        add_apartment = False

        for apartment_filter in apartment_filters:
            add_apartment = apt_filter(apartment, apartment_filter)
            if add_apartment == True:
                break

        if add_apartment == True:
            apartment_list.append(apartment)

    return apartment_list;

def apt_filter(apartment_data, apartment_filter):
    bedrooms = apartment_filter['bedrooms'] if 'bedrooms' in apartment_filter else bedroom_filter_error()
    price = apartment_filter['price'] if 'price' in apartment_filter else DEFAULT_PRICE
    sqft = apartment_filter['sqft'] if 'sqft' in apartment_filter else DEFAULT_SQFT

    return (
        int(apartment_data['Bd']) == bedrooms and
        int(re.sub(r'[$,]', '', apartment_data['Price'])) < price and
        int(apartment_data['Size (sq.ft.)']) >= sqft
    )

def bedroom_filter_error():
    raise ValueError('Bedroom filter required')
