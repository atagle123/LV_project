import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
import sys
sys.path.append(os.path.abspath(os.path.join('..', "LV_project")))

from utils.scrapping import find_xbrl_from_rut_name
from utils.xbrl_download import get_data_xbrl_to_dir



empresa="besalco"
rut="92434000"

Empresa = [f'https://www.cmfchile.cl/portal/principal/613/w3-search.php?keywords={empresa}#fiscalizados',f"//td[text()={rut}]","./following-sibling::td/a"]
keys = ["Url", "selector1", "Selector2"]

año = ["Año",2024,2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 20211, 2010, 2009, 2008, 2007, 2006, 2005]
quarter = ["Q4", "Q3", "Q2", "Q1"]
Tipo_Norma = ["Seleccione", "Estandar IFRS", "Norma Chilena"]

# ver tema del año 

#----------Reemplazar valores en la siguiente lista ----------------------------
configurador = [3,1,1]




if __name__=="__main__":
    print("Executing xbrl parse main...")
    xbrl_url = find_xbrl_from_rut_name(Empresa, configurador)
    get_data_xbrl_to_dir(xbrl_url,"besalco")
    unzip_xbrl_file(file_path)
    
