from utils.excel_downloads import download_excel_file
import pandas as pd
import math




def download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/ICEWeb.xls",filename="ICEWeb",sheet_name=0):
    """ Downloads an excel file to a dataframe and read ir as a dataframe.
    Args:
        url (str): The url of the excel file to download.
        filename (str): The name of the file to save.
        sheet_name (int): The index of the sheet to read from the excel file.

    Returns:
        df (DataFrame): The dataframe read from the excel file.
    """
    download_excel_file(url,name=filename)

    file_path=f"download_excels/{filename}.xlsx"

    dfs = pd.read_excel(file_path,sheet_name=sheet_name)
    return(dfs)




def preprocess_iCE(df,new_column_mapping={0: 'Year', 1: 'Month',5:"Índice general", 11:"Materiales peso",12:"Sueldos y Salarios peso",13:"Misceláneos peso", 14:"Obra Gruesa peso",15:"Terminaciones peso",16:"Instalaciones peso",17: "Costos Indirectos peso"}):
    """ Preprocess the dataframe for ICEweb excel data, see https://cchc.cl/centro-de-informacion/indicadores/indice-de-costos-de-edificacion
    
    Args:
        df (DataFrame): The dataframe to preprocess with the raw ICE data.
        new_column_mapping (dict): The mapping of the new column names.

    Returns:
        df (DataFrame): The preprocessed dataframe.
    """
    df=df.iloc[:, :18]

    df=df.set_axis(df.iloc[2], axis='columns')
    df=df.drop(index=[0, 1,2])
    df = df.reset_index(drop=True)

    df = rename_col_by_index(df, new_column_mapping)
    df.dropna(axis=0,subset=["Month"], inplace=True)
    df=process_dates(df)
    df["Day"]=1
    df.index=pd.to_datetime(df.loc[:,("Year","Month","Day")])
    df=df.drop(columns=["Year","Month","Day"])
    df=df[pd.to_numeric(df["Índice general"],errors="coerce").notnull()]
    return df

def rename_col_by_index(dataframe, index_mapping):
    """ Rename the columns of a dataframe based on the index mapping.

    Args:
        dataframe (DataFrame): The dataframe to rename the columns of.
        index_mapping (dict): The mapping of the index to column name.

    Returns:
        dataframe (DataFrame): The dataframe with renamed columns.
    """
    dataframe.columns = [index_mapping.get(i, col) for i, col in enumerate(dataframe.columns)]
    return dataframe
 

def process_dates(df,first_number=1990,frequency=1):
    """ Process the dates in the dataframe in a specific way given the report format of the Cchc.

    Args:
        df (DataFrame): The dataframe to process the dates in.
        first_number (int): The first year number in the dataframe.
        frequency (int): The number of months between each date (default 1)

    Returns:
        df (DataFrame): The dataframe with processed dates.
    """
    for i,j in enumerate(df.iloc[:,0]):

        if type(j)==int:
            first_number=int(j)
            month_counter=frequency

        elif math.isnan(j):
            df.iloc[i,0]=first_number
            month_counter+=frequency
        df.iloc[i,1]=month_counter
    return(df)

def preprocess_ventas_santiago(df):
    """ Preprocess the dataframe for ventas Santiago excel data, see https://cchc.cl/centro-de-informacion/indicadores/mercado-inmobiliario-oferta-gran-santiago

    Args:
        df (DataFrame): The dataframe to preprocess with the raw ventas Santiago data.

    Returns:
        df (DataFrame): The preprocessed dataframe.
    """
    
    df=df.set_axis(df.iloc[0], axis='columns')
    df=df.drop(index=[0])
    new_column_mapping = {0: 'Year', 1: 'Month',2:"Departamentos stock", 3:"Departamentos ventas",4:"Departamentos Meses",5:"Casas stock", 6:"Casas ventas",7:"Casas meses",8:"Viviendas stock",9: "Viviendas ventas",10: "Viviendas meses"}
    df = rename_col_by_index(df, new_column_mapping)
    df.dropna(axis=0,subset=["Departamentos ventas"], inplace=True)
    df=process_dates(df,first_number=2004,frequency=1)
    df["Period"] = df["Year"].astype(str) +" Q"+ df["Month"].astype(str)
    df=df.drop(columns=["Year","Month"])
    return df

