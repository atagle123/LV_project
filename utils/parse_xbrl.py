import pandas as pd
import math
import numpy as np
from arelle import Cntlr, ViewFileFactTable
import arelle.FileSource
#from arelle.api.Session import Session


def xbrl_to_csv(filename):
    # falta ver directorio de guardado
    fs = arelle.FileSource.openFileSource("C:/Users/ataglem/Desktop/Estados_financieros_(XBRL)92434000_202312/92434000_202312_C.xbrl")

    xbrl = Cntlr.Cntlr().modelManager.load(fs)
    ViewFileFactTable.viewFacts(xbrl, 'test_csv.csv')

def xbrl_csv_to_df():
    # falta ver directorio
    df=pd.read_csv("test_csv.csv")
    return(df)


def preprocess_xml(df):
    """
    df multi index
    idea algoritmo: ir de atras para el principio buscando si hay nans en la fila 
    """
    
    #df["Concept"].fillna(method="ffill",inplace=True)
    for col_idx in reversed(range(df.shape[1])):
        last_category=np.float64('nan')
        for row_idx, row in df.iloc[:,:col_idx+1].iterrows():
            
            if type(row[col_idx])==str or not math.isnan(row[col_idx]):
                last_category=row[col_idx]
            else:
                if df.iloc[row_idx,:col_idx+1].isnull().all():
                    df.iloc[row_idx,col_idx]=last_category
    #df = df.rename(columns = {np.float64('nan'):''})
    #df.dropna(inplace=True)
    return(df)
