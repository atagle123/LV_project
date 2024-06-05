from utils.excel_downloads import download_excel_file
import pandas as pd
import math
import os



def download_excel_to_df(url,path,filename="ICEWeb",sheet_name=0): # url: "https://cchc.cl/uploads/indicador/archivos/ICEWeb.xls"
    """ Downloads an excel file to a dataframe and read it as a dataframe.
    Args:
        url (str): The url of the excel file to download.
        filename (str): The name of the file to save.
        sheet_name (int): The index of the sheet to read from the excel file.

    Returns:
        df (DataFrame): The dataframe read from the excel file.
    """

    download_excel_file(url,path=path,filename=filename) 

    filepath = os.path.join(path, f"{filename}.xlsx")

    dfs = pd.read_excel(filepath,sheet_name=sheet_name)
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
    df=process_dates(df,first_year=2011,first_month=5)
    df["Day"]=1
    df.index=pd.to_datetime(df.loc[:,("Year","Month","Day")])
    df.index.name = 'Fecha'
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
 


def process_dates(df,first_year=1990,frequency=1,first_month=None):
    """ Process the dates in the dataframe in a specific way given the report format of the Cchc.

    Args:
        df (DataFrame): The dataframe to process the dates in.
        first_year (int): The first year number in the dataframe.
        frequency (int): The number of months between each date (default 1)
        first_month (int): The first month number in the dataframe (default None if it is 1)

    Returns:
        df (DataFrame): The dataframe with processed dates.
    """
    for i,j in enumerate(df.iloc[:,0]):

        if type(j)==int:
            month_counter=frequency
            actual_year=int(j)

            if i==0:
                if first_month is not None:
                    month_counter=first_month
                if first_year is not None:
                    actual_year=first_year


        elif math.isnan(j):
            df.iloc[i,0]=actual_year
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
    df=process_dates(df,first_year=2004,frequency=1)
    df["Period"] = df["Year"].astype(str) +"-Q"+ df["Month"].astype(str)
    df.index = pd.PeriodIndex(df["Period"], freq='Q').to_timestamp()
    df.index.name = 'Fecha'
    df=df.drop(columns=["Year","Month","Period"])
    return df

