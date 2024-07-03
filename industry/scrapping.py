import os
import time
import requests
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scrapper:
    """ Class scraper, works with a driver in the drivers folder
    
    """
    def __init__(self,browser="edge",driver_path=None):
        self.browser = browser
        self.drivers_dict = {
            'edge': 'msedgedriver.exe'
            # Add drivers
        }
        self.driver_path = driver_path or self.__get_default_driver_path()
        self.driver=self.__init_driver()
        
    def __get_default_driver_path(self):
        """ 
        Method that returns driver name and if not exit download it 
        
        Returns:
            driver executable path (str): driver exe path 
        """

        driver_exe_path=self.drivers_dict.get(self.browser, self.drivers_dict['edge']) # get driver name and if not use edge driver

        absolute_path = os.path.abspath("drivers") # folder to save the drivers exe
        full_driver_path=os.path.join(absolute_path, driver_exe_path)

        if not os.path.exists(full_driver_path):
            self.__download_driver()

        return full_driver_path
    
    def __download_driver(self):

        url="https://msedgedriver.azureedge.net/126.0.2592.87/edgedriver_win64.zip"

        headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

        response = requests.get(url,headers=headers)

        file_name = os.path.basename(url)
        absolute_path = os.path.abspath("drivers") # folder to save the drivers exe

        os.makedirs(absolute_path,exist_ok=True)

        file_path = os.path.join(absolute_path, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        # If it's a zip file, extract it
        if file_path.endswith('.zip'):
            with ZipFile(file_path, 'r') as zip_ref:
                # Find the .exe file in the zip archive
                exe_files = [name for name in zip_ref.namelist() if name.endswith('.exe')]
                if exe_files:
                    zip_ref.extract(exe_files[0], absolute_path) # extract first exe file
                    self.drivers_dict["edge"]=str(exe_files[0])

        # Delete the zip file after extraction
            os.remove(file_path)

        elif file_path.endswith('.exe'):
            self.drivers_dict["edge"]=file_name
        
        print(f"Driver executable extracted and saved to {absolute_path}")
    
    def __init_driver(self):
        """ 
        Function thats inits the driver 
        
        Returns:
            selenium driver instance
        """

        browser_mapping = {
            "edge": webdriver.Edge,
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            # Add more browsers here as needed
        }

        if self.browser in browser_mapping:
            driver_class = browser_mapping[self.browser]
            driver = driver_class(executable_path=self.driver_path)
            return driver
        
        else:
            raise ValueError(f"Browser {self.browser} not supported")
    
    def close_driver(self):
        """
        Close the driver
        """
        print("Clossing driver...")
        self.driver.close()



class Cmf_scrapper(Scrapper):
    """Class to scrap data from the cmf website, it inherits from the Scrapper class

    """
    def __init__(self, browser="edge", driver_path=None):
        super().__init__(browser, driver_path)
   
    def enter_main_page(self,industry_links,configurador):
        """
        Function that enters the CMF fiscalizados main page of the industry and the given period and year

        Args:
            industry_links (list): list of specific industry website links 
            configurador (list): list of selectors position to click and enter the industry fiscalizados main page
        
        Returns:
            selenium driver: Selenium driver with an open main page

        """

        # Cargar la página de inicio de la empresa en este ejemplo, 
        self.driver.get(industry_links[0])
        td_element=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, industry_links[1])))

        #td_element = self.driver.find_element(By.XPATH,industry_links[1])
        a_element = td_element.find_element(By.XPATH,industry_links[2])
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


    def find_xbrl(self):
        """
        Function that given the enterprise website, it will find the xbrl file.

        Args:
            Empresa (list): list of links from the enterprise website.
            configurador (list): list of configuration parameters.

        Returns:
            str: path to the downloaded xbrl file.
        """

        link=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contenido"]/p/a[6]')))

        xbrl_url = link.get_attribute('href')

        return(xbrl_url)

    
    def get_html(self):
        """
        Get the html of the page from a driver page.

        Returns:
            html : html source code
        
        """
        html= self.driver.page_source
        return(html)
    
    def find_pdf_razonados(self):
        """
        Function that given the enterprise website in the driver, it will find the pdf file.

        Returns:
            str: url path to the downloadable pdf file.
        """

        link=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[3]/p/a[3]'))) # el 3 es el razonado

        pdf_url = link.get_attribute('href')

        return(pdf_url)
    
    def find_pdf_financials(self):
        """
        Function that given the enterprise website in the driver, it will find the pdf file.

        Returns:
            str: url path to the downloadable pdf file.
        """

        link=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[3]/p/a[2]'))) # el 3 es el razonado y el 2 los estados financieros

        pdf_url = link.get_attribute('href')

        return(pdf_url)


if __name__=="__main__":
    scrapper=Scrapper()
