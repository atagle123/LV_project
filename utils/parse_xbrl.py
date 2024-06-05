import pandas as pd
import math
import numpy as np
from arelle import Cntlr, ViewFileFactTable
import arelle.FileSource
import os



class DF_XBRL:
    def __init__(self, xbrl_path,folder_path="xbrl_csv", filename="besalco"):

        self.__xbrl_to_csv(xbrl_path,filename)
        self.df=self.__xbrl_csv_to_df(folder_path=folder_path,filename=filename)

        self.folder_path=folder_path
        self.filename=filename

        self.multiindex_col=11 # eventually get index...
        self.original_index=self.df.iloc[:,:self.multiindex_col]
        self.multiindex_df=self.__preprocess_xml(self.original_index)

        self.df.iloc[:,:self.multiindex_col]=self.multiindex_df
        self.df.set_index(list(self.df.columns.values)[:self.multiindex_col],inplace=True)


    def __xbrl_to_csv(self,path_to_xbrl,path_csv_folder,filename):
        fs = arelle.FileSource.openFileSource(path_to_xbrl)
        print("Parsing XBRL...")
        xbrl = Cntlr.Cntlr().modelManager.load(fs)

        os.makedirs(path_csv_folder, exist_ok=True)
        file_path=os.path.join(path_csv_folder, f"{filename}.csv")

        ViewFileFactTable.viewFacts(xbrl, file_path)

    def __xbrl_csv_to_df(self,path,filename):
        file_path=os.path.join(path, f"{filename}.csv")
        df=pd.read_csv(file_path)
        return(df)


    def __preprocess_xml(self,df):
        """
        df multi index
        idea algoritmo: ir de atras para el principio buscando si hay nans en la fila 
        """
        
        #df["Concept"].fillna(method="ffill",inplace=True)
        for col_idx in reversed(range(df.shape[1])):
            last_category=np.float64('nan')
            for row_idx, row in df.iterrows():
                
                if type(row.iloc[col_idx])==str or not math.isnan(row.iloc[col_idx]):
                    last_category=row.iloc[col_idx]
                else:
                    if df.iloc[row_idx,:col_idx+1].isnull().all():
                        df.iloc[row_idx,col_idx]=last_category
        #df = df.rename(columns = {np.float64('nan'):''})
        #df.dropna(inplace=True)
        return(df)
    
    def search_concept(self, concept,df=None,inplace=False):
        if df is None:
            df=self.df

        filtered_df=df[df.index.get_level_values(0).str.contains(concept)]
        if inplace:
            self.df=filtered_df
        return(filtered_df)


    def loc_useful_data(self, date_list,df=None,inplace=False):
        if df is None:
            df=self.df

        filtered_df=df.loc[:,date_list]

        if inplace:
            self.df=filtered_df

        return(filtered_df)
    
    def save_df(self, df_new,filename):
        df_new.to_csv(f"{filename}.csv")

    def multi_index_to_original_index(self,df):
        """
                df index
                        
        """

        for col_idx in range(df.shape[1]):

            for row_idx, row in df.iterrows():
                next_idx=col_idx+1 if col_idx+1<df.shape[1] else col_idx

                next_col_data=row.iloc[next_idx] if col_idx+1<df.shape[1] else np.float64('nan')
                
                if type(next_col_data)==str or not math.isnan(next_col_data):
                    df.iloc[row_idx,col_idx]=np.float64('nan')
        return(df)
    

    def save_readable_data(self, df=None, filename="readable_data"):

        if df is None:
            df=self.df

        df.reset_index(inplace=True)
        df_index_new=self.multi_index_to_original_index(df=df.iloc[:,:self.multiindex_col])
        df.iloc[:,:self.multiindex_col]=df_index_new
        df.set_index(list(df_index_new.columns.values),inplace=True)

        self.save_df(df,filename)
        
        if not os.path.exists("download_excels"):
            os.makedirs("download_excels")

        df.to_excel(f'download_excels/{filename}.xlsx')  # eventualmente usar exce lwriter


    def show_columns_names(self, df=None):

        if df is None:
            df=self.df
        return(df.dropna(axis=1, how='all'))

    def show_concept_names(self, df=None):

        if df is None:
            df=self.df
        return(df)