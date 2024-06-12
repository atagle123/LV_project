from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class Scrapper:
    """ Class scraper, works with a driver in the drivers folder
    
    """
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


class Cmf_scrapper(Scrapper):
    """Class to scrap data from the cmf website, it inherits from the Scrapper class

    """
    def __init__(self, browser="edge", driver_path=None):
        super().__init__(browser, driver_path)
   
    def enter_main_page(self,Empresa,configurador):

        # Cargar la página de inicio de la empresa en este ejemplo, 
        self.driver.get(Empresa[0])
        td_element=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, Empresa[1])))

        #td_element = self.driver.find_element(By.XPATH,Empresa[1])
        a_element = td_element.find_element(By.XPATH,Empresa[2])
        a_element.click()
                
        estados_financieros=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='listado_reportes']/li[3]/a")))

        estados_financieros.click()

        periodo=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,'mm')))

        #periodo = self.driver.find_element(By.ID,'mm')
        # Crear un objeto Select a partir del elemento <select>
        select_periodo = Select(periodo)
        # Obtener todas las opciones del <select> en una lista
        base_periodo = select_periodo.options
        #-----------------------------------------
        año = self.driver.find_element(By.ID,'aa')
        # Crear un objeto Select a partir del elemento <select>
        select_año = Select(año)
        # Obtener todas las opciones del <select> en una lista
        base_año = select_año.options
        #--------------------------------------------------------
        tipo_norma = self.driver.find_element(By.NAME,'tipo_norma')
        # Crear un objeto Select a partir del elemento <select>
        select_tipo_norma = Select(tipo_norma)
        # Obtener todas las opciones del <select> en una lista
        base_tipo_norma = select_tipo_norma.options

        base_año[configurador[0]].click()
        base_periodo[configurador[1]].click()
        base_tipo_norma[configurador[2]].click()


        #consulta=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@alt="Consultar"]')))
        #consulta = self.driver.find_element(By.XPATH, '//input[@alt="Consultar"]')
        #consulta.click()

        time.sleep(2)
        consulta = self.driver.find_element(By.XPATH, '//input[@alt="Consultar"]')
        consulta.click()
        
        return(self.driver)


    def find_xbrl_from_rut_name(self,Empresa,configurador):
        """
        Function that given a list of links from the enterprise website, it will find the xbrl file and download it.

        Args:
            Empresa (list): list of links from the enterprise website.
            configurador (list): list of configuration parameters.

        Returns:
            str: path to the downloaded xbrl file.
        """

        driver=self.enter_main_page(Empresa, configurador)
        link=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contenido"]/p/a[6]')))

        xbrl_url = link[0].get_attribute('href')

        driver.close()
        return(xbrl_url)

    
    def get_html(self,Empresa,configurador):
        """
        Get the html of the page.
        
        """
        driver=self.enter_main_page(Empresa, configurador)
        html= driver.page_source
        driver.close()
        return(html)

