import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from utils import read_json
import datetime
import requests
from industry.scrapping import Cmf_scrapper
from selenium.common.exceptions import TimeoutException

class Industry:
    """
    Industry class that uses the Cmf_scrapper class to download the data to the path 
    
    """
    
    def __init__(self,empresa) -> None:
        self.empresa=empresa
        self.rut=self.get_rut(empresa)
        self.web_link=self.build_website_link_from_industry(empresa)

        ### Default data directories ###
        current_dir = os.getcwd()
        self.html_path=os.path.join(current_dir, "data","industrydata",empresa,"raw","html")
        self.pdf_path_razonados=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf_razonados")
        self.pdf_path_financials=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf_financials")
        self.xbrl_path=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "xbrl")

        ### Use headers for requests ###
        self.headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

    def get_rut(self,industry_name,folderpath="industry/empresas.json"):
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

            default_folder_path="industry/empresas.json" # path to json with {industry_name: rut,...} . Maybe refactor and do it automatically
            rut=self.get_rut(industry_name,folderpath=default_folder_path)

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


        configurador = [año_num, quarter_num, norma] # cambiar configurador
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
                scrappy_instance=Cmf_scrapper()
                scrappy_instance.enter_main_page(self.web_link,configurador)
                break

            except TimeoutException as e:
                print(f"TimeoutException occurred: {e}")

        try:
            ### Get data sources ###
            html=scrappy_instance.get_html()
            xbrl_url=scrappy_instance.find_xbrl()
            pdf_razonados_url=scrappy_instance.find_pdf_razonados()
            pdf_financials_url=scrappy_instance.find_pdf_financials()
            
            ### Download and save data ###

            self.save_html(html,self.html_path,filename=f"html_{año}_{mes}")
            self.save_pdf(pdf_razonados_url,self.pdf_path_razonados,filename=f"Analisis_razonados_{año}_{mes}")
            self.save_pdf(pdf_financials_url,self.pdf_path_financials,filename=f"Estados_financieros_{año}_{mes}")
            self.save_xbrl(xbrl_url,self.xbrl_path,filename=f"XBRL_zip_{año}_{mes}")
            
        except TimeoutException as e:
            print(f"TimeoutException occurred: {e} data not finded")

        scrappy_instance.close_driver()

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

    
    def save_html(self,html,path,filename):
        """
        Function to save html source code in to txt

        Args:
            html (str): html source code
            path (str): path to html saved data
            filename (str): filename to name the txt file

        """
         
        os.makedirs(path, exist_ok=True)

        file_path=os.path.join(path,f"{filename}.txt")  # check if not use string io

        with open(file_path,"wt") as f:
            f.write(html)
        print(f"Downloaded {filename}")

        pass


    def save_pdf(self,pdf_url,path,filename):
        """
        Function to download and save pdf

        Args:
            pdf_url (str): url to download pdf
            path (str): path to html saved data
            filename (str): filename to name the txt file
            
        """

        try:
            response=requests.get(pdf_url,headers=self.headers)
            response.raise_for_status()

            os.makedirs(path, exist_ok=True)

            file_path=os.path.join(path,f"{filename}.pdf")

            with open(file_path,"wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")

        except requests.RequestException as e:
            print(f"Failed to download: {filename}:{e}")
        

    def save_xbrl(self,xbrl_url,path,filename):   
        """
            Function to get data from an url download to the file path.
            The download format is in a zip file

            Args:
                url (str): url to download
                path (str): path to save the file
                filename (str): name of the file        
        """

        try:
            response=requests.get(xbrl_url,headers=self.headers)
            response.raise_for_status()

            os.makedirs(path, exist_ok=True)

            file_path=os.path.join(path,f"{filename}.zip")

            with open(file_path,"wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")

        except requests.RequestException as e:
            print(f"Failed to download: {filename}:{e}")



    


if __name__ == "__main__":
    industry=Industry("besalco")
    industry.get_historic_data(desde=2018,hasta=2020)
