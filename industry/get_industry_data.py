import sys,os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from industry.scrapping import find_xbrl_from_rut_name
from utils.xbrl_download import get_data_xbrl_to_path,unzip_xbrl_file, find_xbrl_path
from utils.parse_xbrl import DF_XBRL
from utils import build_website_link_from_industry




def get_accountability(empresa):


    Empresa = build_website_link_from_industry(empresa)

   # keys = ["Url", "selector1", "Selector2"]

    año = ["Año",2024,2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 20211, 2010, 2009, 2008, 2007, 2006, 2005] # eventualmente ver si se estan todos los años y levantar una excepcion si no hay mas alla de lo q se pide
    quarter = ["03", "06", "09", "12"]

   # Tipo_Norma = ["Seleccione", "Estandar IFRS", "Norma Chilena"]


    dates_dict={"03":31,
                "06":30,
                "09":30,
                "12":31
                }


    #----------Reemplazar valores en la siguiente lista ----------------------------
    configurador = [3,1,1] # cambiar configurador

    año=año[configurador[0]]
    mes=quarter[configurador[1]]
    dia=dates_dict[mes]

    useful_dates=[f"{año}-{mes}-{dia}",f"{año-1}-12-31"]

    filaname=f"{empresa}_{año}-{mes}-{dia}"

    xbrl_url = find_xbrl_from_rut_name(Empresa, configurador)
    get_data_xbrl_to_path(xbrl_url,filaname)
    unzip_xbrl_file(filename=filaname, dir="XBRL_files")
    xbrl_path=find_xbrl_path(filename=filaname, dir="XBRL_files")

    df_xbrl_instance=DF_XBRL(xbrl_path,folder_path="xbrl_csv", filename=filaname)

    filtered_df = df_xbrl_instance.search_concept(concept="871100")
    filtered_df=df_xbrl_instance.loc_useful_data(date_list=useful_dates,df=filtered_df)
    df_xbrl_instance.save_readable_data(df=filtered_df, filename=filaname)
