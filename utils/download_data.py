import os



def download_dfs(dict_of_dfs=None,filename="excel_data"):
    """ Make a 3 big df (anual,mensual and trimestral) and download an excel with all the data
    descargar todos los datos mensuales de una. depues todos los anuales y trimestrales, hacer join con los datos rescatados de otros lados... {"name":dfs}

    """
    data_dir="data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with pd.ExcelWriter(os.path.join(data_dir, f"{filename}.xlsx")) as writer:
        for sheet_name,df in dict_of_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name)