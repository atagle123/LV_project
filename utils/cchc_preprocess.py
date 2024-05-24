from utils.excel_downloads import download_excel_file
import pandas as pd
import math




def download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/ICEWeb.xls",filename="ICEWeb",sheet_name=0):

    download_excel_file(url,name=filename)

    file_path=f"download_excels/{filename}.xlsx"

    dfs = pd.read_excel(file_path,sheet_name=sheet_name)
    return(dfs)




def preprocess_iCE(df,new_column_mapping={0: 'Year', 1: 'Month',5:"Índice general", 11:"Materiales peso",12:"Sueldos y Salarios peso",13:"Misceláneos peso", 14:"Obra Gruesa peso",15:"Terminaciones peso",16:"Instalaciones peso",17: "Costos Indirectos peso"}):
    """
    Preprocess the dataframe for ICE excel data
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
    dataframe.columns = [index_mapping.get(i, col) for i, col in enumerate(dataframe.columns)]
    return dataframe
 

def process_dates(df,last_number=1990,frequency=1):
    for i,j in enumerate(df.iloc[:,0]):

        if type(j)==int:
            last_number=int(j)
            month_counter=frequency

        elif math.isnan(j):
            df.iloc[i,0]=last_number
            month_counter+=frequency
        df.iloc[i,1]=month_counter
    return(df)

def preprocess_ventas_santiago(df):
    
    df=df.set_axis(df.iloc[0], axis='columns')
    df=df.drop(index=[0])
    new_column_mapping = {0: 'Year', 1: 'Month',2:"Departamentos stock", 3:"Departamentos ventas",4:"Departamentos Meses",5:"Casas stock", 6:"Casas ventas",7:"Casas meses",8:"Viviendas stock",9: "Viviendas ventas",10: "Viviendas meses"}
    df = rename_col_by_index(df, new_column_mapping)
    df.dropna(axis=0,subset=["Departamentos ventas"], inplace=True)
    df=process_dates(df,last_number=2004,frequency=1)
    df["Period"] = df["Year"].astype(str) +" Q"+ df["Month"].astype(str)
    #df["Day"]=1
    #df.index=pd.to_datetime(df.loc[:,("Year","Month","Day")])
    df=df.drop(columns=["Year","Month"])
    return df

