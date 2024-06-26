import os
import sys
from utils import read_json
import datetime
import requests
from industry.scrapping import Cmf_scrapper

class Industry:
    def __init__(self,empresa) -> None:
        self.empresa=empresa
        self.rut=self.get_rut(empresa)
        self.web_link=self.build_website_link_from_industry(empresa)

        current_dir = os.getcwd()

        self.csv_path=os.path.join(current_dir, "data","industrydata",empresa,"raw","html")
        self.pdf_path=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf")
        self.excel_path=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "pdf")
        self.xbrl_path=os.path.join(current_dir, "data", "industrydata",empresa,"raw", "xbrl")


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
    
    def get_one_period_data(self, año, mes,concept_list):

        configurador=self.build_configurator_to_scrapping(año,mes)  # arreglar lo de si no encuentra la fecha

        scrappy_instance=Cmf_scrapper()
        scrappy_instance.enter_main_page(self.web_link,configurador)

        html=scrappy_instance.get_html()
        xbrl_url=scrappy_instance.find_xbrl()
        pdf_razonados_url=scrappy_instance.find_pdf_razonados()
        pdf_financials_url=scrappy_instance.find_pdf_financials()

        scrappy_instance.close_driver()


        # llamar a manage xbrl



      #  html_instance=HTML_parser(html)
      #  df_dict=html_instance.search_concept_list(concept_list)

        return(df_dict)
    
    def get_historic_data(self,empresa="besalco",desde=2018,hasta=None):

        concept_list=["210000","310000","510000"]

        pd_list=[[] for _ in range(len(concept_list))]
        dict_list=dict(zip(concept_list,pd_list))


        hasta = hasta or  datetime.datetime.now().year

        for año in range(desde,hasta+1):
            for mes in ["03","06","09","12"]:

                df_dict=self.get_one_period_data(año, mes,empresa,concept_list)

                for keys,values in df_dict.items():

                    dict_list[keys].append(values)

        for keys,values in dict_list.items():
            for i,df in enumerate(values):
                if df is not None:
                   print(keys,i,"Index is unique: ", df.index.is_unique)
                else:
                    print(keys, i, "df is None")

            dict_list[keys]=pd.concat(values,join="outer",axis="columns")

        return(dict_list)
    


if __name__ == "__main__":
     pass