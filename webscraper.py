#!/usr/bin/env python3

import equityscraper

def scrape(opts = {}):
    apartmentSizes = [1, 2] if opts['SIZES'] is None else opts['SIZES']
    
    apartmentScrape = []
    apartmentScrape += equityscraper.scrape(apartmentSizes)

    # return list of scraped apartments
    return apartmentScrape

if __name__ == "__main__":
    print(scrape())
