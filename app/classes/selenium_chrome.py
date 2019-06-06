#!/usr/bin/env python3

from app.config import Config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class SeleniumChrome:
    def __init__(self):
        chrome_options = self.__chrome_options()
        chrome_executable = self.__chrome_executable()
        
        self.driver = webdriver.Chrome(
            executable_path=chrome_executable,
            chrome_options=chrome_options
        )

    def quit(self):
        self.driver.quit()

    def get_url(self, url):
        self.driver.get(url)

    def get_element_by_id(self, element_id):
        try:
            return WebDriverWait(self.driver, self.__TIMEOUT).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            print("Loading took too much time!")

    __TIMEOUT = 10

    def __configs(self, key):
        config = Config()
        return getattr(config, key)

    def __chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = self.__configs('GOOGLE_CHROME_BIN')
        return chrome_options

    def __chrome_executable(self):
        chrome_executable = self.__configs('CHROMEDRIVER_PATH')
        return chrome_executable

