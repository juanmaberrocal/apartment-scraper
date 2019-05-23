#!/usr/bin/env python3

from operator import itemgetter

from .scrapers import equityscraper
from .scrapers import watersidescraper

def scrape(opts = {}):
    apartment_sizes = [1, 2] if opts['SIZES'] is None else opts['SIZES']
    
    apartment_scrape = []
    apartment_scrape += equityscraper.scrape(apartment_sizes)
    apartment_scrape += watersidescraper.scrape(apartment_sizes)

    # return (sorted) list of scraped apartments
    return sorted(apartment_scrape, key=itemgetter('Bd', 'Price')) 

if __name__ == "__main__":
    print(scrape())
