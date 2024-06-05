import os
import pandas as pd


def download_dfs(path,dict_of_dfs=None,filename="excel"):
    """ Make a 3 big df (anual,mensual and trimestral) and download an excel with all the data
    descargar todos los datos mensuales de una. depues todos los anuales y trimestrales, hacer join con los datos rescatados de otros lados... {"name":dfs}

    """
    os.makedirs(path, exist_ok=True)

    filepath=os.path.join(path, f"{filename}.xlsx")

    with pd.ExcelWriter(filepath) as writer:
        for sheet_name,df in dict_of_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name)