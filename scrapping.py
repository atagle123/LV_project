import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time


class Cmf_scrapper:  
    def __init__(self,browser="edge",driver_path=None):
        self.browser = browser
        self.driver_path = driver_path or self.get_default_driver_path()
        self.driver=self._init_driver()
        
    def get_default_driver_path(self):
        drivers = {
            'edge': 'msedgedriver.exe'
        }
        return drivers.get(self.browser, drivers['edge'])
    
    def _init_driver(self):
        if self.browser == "edge":
            absolute_path = os.path.abspath("drivers")
            full_driver_path=os.path.join(absolute_path, self.driver_path)
            driver = webdriver.Edge(executable_path=full_driver_path)
            return(driver)
        else:
            raise ValueError("Browser not supported")
    
    def get_data(self):
        pass
    def get_data_from_url(self,url):
        pass
    def data_to_file(self, format="excel"):
        pass 