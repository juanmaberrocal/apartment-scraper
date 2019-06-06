# APARTMENT WEB SCRAPER
Little scraper that goes into specified apartment webpages and looks for available apartments. You can configure the amount of bedrooms + any specific filters to search for.  
After all results are pulled and filtered, prints out slack message with the list of apartments.

### Dependencies
- pip install -r requirements.txt
- pip freeze > requirements.txt

### Run Commands:
- cd ~/apartment-scraper/
- source apartment-scraper/bin/activate
- python run.py
- [deactivate]

### URL Requests:
- curl -X Post <LOCALHOST>/slackbot
- curl -X POST -H "Content-type: application/json" --data '{"type":"event_callback","event":{"type":"app_mention","text":"<SLACK LOOKUP TEXT>","channel":"<SLACK_CHANNEL>"}}' <LOCALHOST>/slack-event

## Heroku
### Buildpacks:
- heroku/python
- heroku-buildpack-chromedriver
- heroku-buildpack-google-chrome

### Deploy:
- git commit
- git push
- git push heroku master
