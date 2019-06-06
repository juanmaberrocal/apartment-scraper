# APARTMENT WEB SCRAPER
Little scraper that goes into specified apartment webpages and looks for available apartments. You can configure the amount of bedrooms + any specific filters to search for.  
After all results are pulled and filtered, it sends out an email with the list of apartments.

### Heroku Buildpacks:
- heroku/python
- heroku-buildpack-chromedriver
- heroku-buildpack-google-chrome

### Dependencies
- pip install -r requirements.txt
- pip freeze > requirements.txt

### Run commands:
- cd ~/apartment-scraper/
- source apartment-scraper/bin/activate
- python app/apartment-scraper.py
- deactivate
