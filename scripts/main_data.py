import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import  read_json
from industry.industry_data import Industry_Data
from industry.html_parser import HTML_industry_data 



def main(desde,hasta):
    current_dir=os.getcwd()
    empresas_dir=os.path.join(current_dir,"configs","empresas.json")
    
    empresas_json=read_json(empresas_dir)
    for empresa in empresas_json.keys():
        
        industry=Industry_Data(empresa)
        industry.get_historic_data(desde=desde,hasta=hasta)

        html_industry=HTML_industry_data(empresa)
        html_industry.process_and_save_historic_data(desde=desde,hasta=hasta)





if __name__ == "__main__":
    desde=2010
    hasta=2024
    
    main(desde,hasta)
