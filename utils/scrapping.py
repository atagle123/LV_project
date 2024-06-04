import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
import os

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



def find_xbrl_from_rut_name(Empresa,configurador):
    scrappy=Cmf_scrapper()
    driver=scrappy.driver
    # Cargar la página de inicio de la empresa en este ejemplo, 
    driver.get(Empresa[0])
    time.sleep(2)
    td_element = driver.find_element(By.XPATH,Empresa[1])
    a_element = td_element.find_element(By.XPATH,Empresa[2])
    a_element.click()
    time.sleep(2)


    estados_financieros = driver.find_element(By.XPATH, "//*[@id='listado_reportes']/li[3]/a")
    estados_financieros.click()
    time.sleep(2)

    periodo = driver.find_element(By.ID,'mm')
    # Crear un objeto Select a partir del elemento <select>
    select_periodo = Select(periodo)
    # Obtener todas las opciones del <select> en una lista
    base_periodo = select_periodo.options
    #-----------------------------------------
    año = driver.find_element(By.ID,'aa')
    # Crear un objeto Select a partir del elemento <select>
    select_año = Select(año)
    # Obtener todas las opciones del <select> en una lista
    base_año = select_año.options
    #--------------------------------------------------------
    tipo_norma = driver.find_element(By.NAME,'tipo_norma')
    # Crear un objeto Select a partir del elemento <select>
    select_tipo_norma = Select(tipo_norma)
    # Obtener todas las opciones del <select> en una lista
    base_tipo_norma = select_tipo_norma.options

    base_año[configurador[0]].click()
    base_periodo[configurador[1]].click()
    base_tipo_norma[configurador[2]].click()

    time.sleep(2)
    consulta = driver.find_element(By.XPATH, '//input[@alt="Consultar"]')
    consulta.click()

    link = driver.find_elements_by_xpath( '//*[@id="contenido"]/p/a[6]')  #xpath a xbrl, esto puede llegar a cambiar

    xbrl_url = link[0].get_attribute('href')

    driver.close()
    return(xbrl_url)
