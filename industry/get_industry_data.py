import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from industry.parse_xbrl import DF_XBRL
from utils import build_website_link_from_industry,build_configurator_to_scrapping
from industry.scrapping import find_xbrl_from_rut_name


def get_industry_data(empresa="falabella", año=2022, mes="06"):

    empresa_link = build_website_link_from_industry(empresa)

    dates_dict={"03":31,
                "06":30,
                "09":30,
                "12":31
                }
    
    dia=dates_dict[mes]

    configurador=build_configurator_to_scrapping(año,mes)

    useful_dates=[f"{año}-{mes}-{dia}",f"{año-1}-12-31"]

    xbrl_url=find_xbrl_from_rut_name(empresa_link,configurador)

    df_xbrl_instance=DF_XBRL(xbrl_url,empresa,useful_dates)

    concept_dict={"210000":useful_dates,
                "310000":"all",
                "420000":"all"} #" hacer algo para construir esto quizas..."
    #[f"Desde {año-1}-01-01 Hasta {año-1}-{mes}-{dia}",f"Desde {año}-01-01 Hasta {año}-{mes}-{dia}"]} # ojo que esto cambia dependiendo del quarter, que se elija... ver

    df_xbrl_instance.download_concepts(concept_dict)



def get_historic_data_of_industry(empresa="falabella",desde=2005):
    for i in range(desde,2022):
        for j in ["03","06","09","12"]:
            get_industry_data(empresa, i, j)

    pass

if __name__ == "__main__":
    get_industry_data(empresa="besalco")