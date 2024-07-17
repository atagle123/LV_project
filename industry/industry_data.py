import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
import requests
from utils import read_json
from industry.scrapping import Cmf_scrapper
from selenium.common.exceptions import TimeoutException
from industry.data_manager import Manage_Data


class Industry:
    """
    Industry class that uses the Cmf_scrapper class to download the data to the path 
    
    """
    
    def __init__(self,empresa) -> None:
        self.empresa=empresa
        self.default_empresas_path= "configs/empresas.json" # path to json with {industry_name: rut,...} . Maybe refactor and do it automatically

        self.rut=self.get_rut(empresa)
        self.web_link=self.build_website_link_from_industry(empresa)

        ### Default data directories ###
        current_dir = os.getcwd()
        self.html_path=os.path.join(current_dir, "data","industrydata",empresa,"raw","html")
        self.pdf_path_razonados=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf_razonados")
        self.pdf_path_financials=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf_financials")
        self.xbrl_path=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "xbrl")

        self.Scrappy_instance=Cmf_scrapper() # scrapper class to find the data 
        self.Data_Manager=Manage_Data() # data manager class, to get and download the data

    def get_rut(self,industry_name,folderpath="configs/empresas.json"):
        """
        Get RUT from the json file in the given path by industry name

        Args:
            industry_name (str): industry name
            folderpath (str): path to the json file
        
        Returns:
            str: RUT
        
        """
        json_data=read_json(folderpath)
        rut=json_data[industry_name]
        return(rut)


    def build_website_link_from_industry(self,industry_name):
            """ Build specific website link from industry name to the scrapper to work

            Args:
                industry_name (str): industry name

            Returns:
                industry_links (list): industry website links

            """

            rut=self.get_rut(industry_name,folderpath=self.default_empresas_path)

            print(f"RUT:{rut}")
            
            industry_links = [f'https://www.cmfchile.cl/portal/principal/613/w3-search.php?keywords={industry_name}#fiscalizados',f"//td[text()={rut}]","./following-sibling::td/a"] # esto puede estar sujeto a cambios de la CMF
            return(industry_links)


    def build_configurator_to_scrapping(self,año,quarter,url=None,norma=1): # eventualmente buscar ultimo año disponible por url 
        """ 
        Build configurator to scrapping from the given parameters

        Args:
            año (int): year
            quarter (str): month ["03", "06", "09", "12"]
            norma (int): norma to scrapping 1 IFRS, 2 norma chilena
        
        Returns:
            configurador (list): specific configurator to scrapping, to map year,month and norm into a lit of element position in the clickable selection

        """
        quarter_dict={"03":0,
            "06":1,
            "09":2,
            "12":3
                    }

        años_dict=self.generate_years_dict(desde=año)
        año_num=años_dict[año]
        quarter_num=quarter_dict[quarter]


        configurador = [año_num, quarter_num, norma] 
        return(configurador)


    def generate_years_dict(self,desde=2005):
        """
        Generate dict of years from the given year in the fllowing way {1:2024, 2:2023, ...} 
        Note that 0 is not a year, is "Año" see the CMF page

        Args:
            desde (int): year

        Returns:
            dict: dict of years

        """
        current_year = datetime.datetime.now().year
        years_dict={year : i+1 for i,year in enumerate(reversed(range(desde,current_year+1)))}
        return(years_dict)
    
    def get_one_period_data(self, año, mes):
        """
        Function that calls scrapper, enter page of the deired industry, quarter and year. And downloads all the relevant data (pdf's, html, xbrl)

        Args:
            año (int): Year to download data
            mes (str): Month to download data, is one of the following ["03","06","09","12"]

        """

        configurador=self.build_configurator_to_scrapping(año,mes)  # arreglar lo de si no encuentra la fecha


        for i in range(5): # do 5 trys to enter the page

            try:
                self.Scrappy_instance.init_driver()
                self.Scrappy_instance.enter_main_page(self.web_link,configurador)
                break

            except TimeoutException as e:
                print(f"TimeoutException occurred: {e}")

        try:
            ### Get data sources ###
            html=self.Scrappy_instance.get_html()
            xbrl_url=self.Scrappy_instance.find_xbrl()
            pdf_razonados_url=self.Scrappy_instance.find_pdf_razonados()
            pdf_financials_url=self.Scrappy_instance.find_pdf_financials()
            
            ### Download and save data ###
            self.Data_Manager.download_data(file_content=html,path=self.html_path,filename=f"html_{año}_{mes}",extension="txt",mode="wt") # download html
            self.Data_Manager.get_and_download_data(url=xbrl_url,path=self.xbrl_path,filename=f"XBRL_zip_{año}_{mes}",extension="zip") # download and get xbrl
            self.Data_Manager.get_and_download_data(url=pdf_razonados_url,path=self.pdf_path_razonados,filename=f"Analisis_razonados_{año}_{mes}",extension="pdf") # download and get pdf
            self.Data_Manager.get_and_download_data(url=pdf_financials_url,path=self.pdf_path_financials,filename=f"Estados_financieros_{año}_{mes}",extension="pdf") # download and get pdf

        except TimeoutException as e:
            print(f"TimeoutException occurred: {e} Data not finded from {self.empresa}, {año}, {mes}")

        self.Scrappy_instance.close_driver()

        pass
    

    def get_historic_data(self,desde=2018,hasta=None):
        """
        Function that gets all the historic data from a given date, it calls get one period data
        
        Args:
            desde (int): initial year to download the data  
            hasta (int): final year to download the data

        """

        hasta = hasta or  datetime.datetime.now().year # if none current year is provided

        for año in range(desde,hasta+1):
            for mes in ["03","06","09","12"]:

                self.get_one_period_data(año, mes)

        print(f"Downloaded all data of {self.empresa} from {desde} to {hasta}")
