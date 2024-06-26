import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import  read_json
from industry.industry_data import Industry





if __name__ == "__main__":
    desde=2018
    hasta=2020

    empresas_json=read_json("C:/Users/ataglem/Desktop/LV_project/industry/empresas.json")
        
    for empresa in empresas_json.keys():
        
        industry=Industry(empresa)
        industry.get_historic_data(desde=desde,hasta=hasta)

        process_and_save_historic_data(self,desde=2018,hasta=None) for empresa
#
