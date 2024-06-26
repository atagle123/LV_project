import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import  read_json
from industry.industry_data import Industry
from industry.html_parser import HTML_industry_data 




if __name__ == "__main__":
    desde=2018
    hasta=2020

    empresas_json=read_json("C:/Users/ataglem/Desktop/LV_project/industry/empresas.json")
    empresas_json={"besalco":1}
    for empresa in empresas_json.keys():
        
        industry=Industry(empresa)
        industry.get_historic_data(desde=desde,hasta=hasta)

        html_industry=HTML_industry_data(empresa)
        html_industry.process_and_save_historic_data(desde=desde,hasta=hasta)
#
