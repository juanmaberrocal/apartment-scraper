#!/usr/bin/env python3

import equityscraper

def scrape(opts = {}):
    apartment_sizes = [1, 2] if opts['SIZES'] is None else opts['SIZES']
    
    apartment_scrape = []
    apartment_scrape += equityscraper.scrape(apartment_sizes)

    # return list of scraped apartments
    return apartment_scrape

if __name__ == "__main__":
    print(scrape())
