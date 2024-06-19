import os
import sys
from utils import read_json
import datetime

class Industry:
    def __init__(self,empresa) -> None:
        self.empresa=empresa
        self.rut=self.get_rut(empresa)
        self.web_link=self.build_website_link_from_industry(empresa)

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
                list: website links

            """
            default_folder_path="industry/empresas.json"
            rut=self.get_rut(industry_name,folderpath=default_folder_path)
            print(f"RUT:{rut}")
            
            Empresa = [f'https://www.cmfchile.cl/portal/principal/613/w3-search.php?keywords={industry_name}#fiscalizados',f"//td[text()={rut}]","./following-sibling::td/a"] # esto puede estar sujeto a cambios de la CMF
            return(Empresa)


    def build_configurator_to_scrapping(self,año,quarter,url=None,norma=1): # eventualmente buscar ultimo año disponible por url 
        """ 
        Build configurator to scrapping from the given parameters

        Args:
            año (int): year
            quarter (str): month ["03", "06", "09", "12"]
            norma (int): norma to scrapping 1 IFRS, 2 norma chilena

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

        Args:
            from (int): year

        Returns:
            list: list of years

        """
        current_year = datetime.datetime.now().year
        years_dict={year : i+1 for i,year in enumerate(reversed(range(desde,current_year+1)))}
        return(years_dict)
    


if __name__ == "__main__":
     pass