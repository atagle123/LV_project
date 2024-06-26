import pandas as pd
import math
import numpy as np
from arelle import Cntlr, ViewFileFactTable
import arelle.FileSource
import os
import requests
import zipfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from industry.parse_xbrl import DF_XBRL
from industry.scrapping import Cmf_scrapper
from industry.industry_data import Industry

class Manage_xbrl:
    """ Base class to manage an xbrl file
        The process is as follows:
        - download_xbrl 
        - unzip xbrl 
        - parse xbrl-to-csv
        - csv to dataframe

    """


    def __init__(self,industry,dates):#,base_path="industrydata"): # generar nombre decente que la clase sea empresa_date
        """ 
            Args:
                industry (str): name of the industry
                dates (str): list of dates of the file
        """
        self.industry=industry
        self.dates=dates

        current_dir = os.getcwd()
        self.zip_path=os.path.join(current_dir, "data","industrydata","xbrl","zip")
        self.unzip_path=os.path.join(current_dir, "data","industrydata","xbrl","unzip")
        self.rawcsv_path=os.path.join(current_dir, "data","industrydata","xbrl","raw_csv")
        self.industry_path=os.path.join(self.rawcsv_path, industry) 

        self.filename=self.gen_filename(dates, industry)
    
    def make_dirs(self):
        pass


    def download_xbrl(self,url,zip_path,filename):   
        """
            Function to get data from an url download to the file path.
            The download format is in a zip file

            Args:
                url (str): url to download
                path (str): path to save the file
                filename (str): name of the file        
        """

        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    
        response = requests.get(url,headers=headers)
        response.raise_for_status()

        os.makedirs(zip_path, exist_ok=True)

        self.zip_path=zip_path

        file_path=os.path.join(zip_path,f"{filename}.zip")  

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"XBRL.zip downloaded in {file_path}")



    def unzip_file(self,filename,unzip_path,zip_path):
        """ Function to unzip a file
            Args:
                zip_path (str): path to the zip file
                unzip_path (str): path to the target folder to unzip
                filename (str): name of the file
        """

        zip_path = zip_path or self.zip_path 

        os.makedirs(unzip_path, exist_ok=True)

        file_path=os.path.join(zip_path,filename)
        target_path=os.path.join(unzip_path, filename)

        #self.unzip_path=unzip_path

        with zipfile.ZipFile(f'{file_path}.zip', 'r') as zip_ref:
            zip_ref.extractall(target_path)



    
    def xbrl_to_csv(self,xbrl_path, industry_path, filename):
        """ Function to parse an xbrl file to a csv file with arelle

            Args:
                xbrl_path (str): path to the xbrl file
                industry_path (str): path to the folder to save the csv file
                filename (str): name of the file
        
        """

        fs = arelle.FileSource.openFileSource(xbrl_path)  # tiene que ser el path completo
        print("Parsing XBRL...")
        xbrl = Cntlr.Cntlr().modelManager.load(fs)

        os.makedirs(industry_path, exist_ok=True)

        file_path=os.path.join(industry_path, f"{filename}.csv")

        ViewFileFactTable.viewFacts(xbrl, file_path)
        print(f"XBRL parsed to {file_path}")

    def xbrl_csv_to_df(self,path=None,filename=None):
        """ Function to read a csv file to a dataframe

            Args:
                path (str): path to the csv file
                filename (str): name of the file
        
        """


        file_path=os.path.join(self.industry_path, f"{self.filename}.csv") or os.path.join(path, f"{filename}.csv")
        df=pd.read_csv(file_path)
        return(df)
    

        
    def xbrl_url_to_csv(self,url):
        """ Function to download an xbrl file from a url and parse it to a csv file
            Main download pipeline

            Args:
                url (str): url to download

        """
        
        self.download_xbrl(url,self.zip_path,self.filename) # get xbrl to zip_path/filename
        self.unzip_file(self.filename, self.unzip_path, self.zip_path) # unzip file to unzip_path

        xbrl_path=self.find_xbrl_path(self.unzip_path,self.filename)
        self.xbrl_to_csv(xbrl_path, self.industry_path, self.filename) # xbrl path to indusrty_path
        # ver si retorna un csv o un dataframe





    def find_xbrl_path(self,path,filename):
        """ Find path of XBRL file given path and filename

            Args:
                path (str): path to the folder containing the unzip folder with the whole accounting info
                filename (str): name of the unziped file
        
        """

        directorio=os.path.join(path,filename)

        for ruta_directorio, _, archivos in os.walk(directorio):
            for archivo in archivos:
                if archivo.endswith('.xbrl'):
                    # Imprimir el path completo del archivo
                    path_completo = os.path.join(ruta_directorio, archivo)
        
        print("Path completo del archivo XBRL:", path_completo)
        return(path_completo)


    def gen_filename(self, dates, industry):
        """ Generate filename from dates and industry name

            Args:
                dates (str): list of two dates of the file
                industry (str): name of the industry

        """

        filename=f"{industry}_{dates[0]}_{dates[1]}"
        return(filename)






class DF_XBRL(Manage_xbrl):
    def __init__(self,url,industry,dates,already_downloaded=False): # path es industry_data
        """ Class to preprocess an xbrl file
        works with the following directories:
        - data/industry_data/
            - excel/
            - csv/
            - xbrl/
                - zip_xbrl
                - unzip_xbrl

        To name a countabiity file: /industry_dates
            

        Args:
            xbrl_path (str): Path to the xbrl file
            path (str): Path to the folder containing the xbrl file
            industry_name (str): Name of the industry
        """
        super().__init__(industry,dates)

        current_dir = os.getcwd()

        if not already_downloaded:
            self.xbrl_url_to_csv(url)
        
        self.df=self.xbrl_csv_to_df(self.industry_path, self.filename)

        self.multiindex_col=11 # eventually get index...
        self.original_index=self.df.iloc[:,:self.multiindex_col]
        self.multiindex_df=self.__preprocess_xml(self.original_index)

        self.df.iloc[:,:self.multiindex_col]=self.multiindex_df
        self.df.set_index(list(self.df.columns.values)[:self.multiindex_col],inplace=True)

        self.csv_path=os.path.join(current_dir, "data","industrydata","xbrl","csv",industry,f"{dates[0]}_{dates[1]}")
        self.excel_path=os.path.join(current_dir, "data", "industrydata", "xbrl", "excel",industry,f"{dates[0]}_{dates[1]}")

   


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
        """ Function to search a concept in the dataframe, corresponds to a conntextref id. For example 210000 to EE.FF

            Args:
                concept (str): concept to search
                df (dataframe): dataframe to search in
                inplace (bool): if True, the dataframe is modified
        
        """

        if df is None:
            df=self.df

        filtered_df=df[df.index.get_level_values(0).str.contains(concept)]

        if inplace:
            self.df=filtered_df
        return(filtered_df)


    def loc_data(self, date_list,df=None,inplace=False):
        """ Function to lock specific columns of the dataframe, usually the columns has date format
            
            Args:
                date_list (list): list of columns to lock
                df (dataframe): dataframe to lock
                inplace (bool): if True, the dataframe is modified
        
        """

        if df is None:
            df=self.df
        if isinstance(date_list,list):
            filtered_df=df.loc[:,date_list]

        elif date_list=="all":
            filtered_df=df

        if inplace:
            self.df=filtered_df

        return(filtered_df)
    
    def save_df_to_csv(self, df_new,filename): # cambiar esto
        filepath=os.path.join(self.csv_path, filename)
        df_new.to_csv(f"{filepath}.csv")

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
    

    def save_data(self, df=None, concept_name="readable_data"): # cambiar filename 

        os.makedirs(self.excel_path, exist_ok=True)
        os.makedirs(self.csv_path, exist_ok=True)

        if df is None:
            df=self.df

        df.reset_index(inplace=True) # cambia el indice de vuelta a la normalidad, para que sea leible en excel
        df_index_new=self.multi_index_to_original_index(df=df.iloc[:,:self.multiindex_col])
        df.iloc[:,:self.multiindex_col]=df_index_new
        df.set_index(list(df_index_new.columns.values),inplace=True)
        


        self.save_df_to_csv(df,concept_name)

        excel_path=os.path.join(self.excel_path,f"{concept_name}.xlsx")

        df.to_excel(excel_path)  # eventualmente usar excel lwriter


    def show_columns_names(self, df=None):

        if df is None:
            df=self.df
        df_non_nan=df.dropna(axis=1, how='all')
        columns_list=df_non_nan.columns.tolist()
        return(columns_list)

    def show_concept_names(self, df=None):

        if df is None:
            df=self.df

        concepts=df.index.get_level_values(0).to_list()
        #" quizas hacer unique"

        return(concepts)
    
    def download_concepts(self,concept_dict=None):

        for concept,useful_dates in concept_dict.items():

            filtered_df = self.search_concept(concept=concept)
            filtered_df=self.loc_data(date_list=useful_dates,df=filtered_df)
            self.save_data(df=filtered_df, concept_name=concept)
        pass


def get_industry_data(empresa="falabella", año=2022, mes="06"):

    industry_instance=Industry(empresa)

    empresa_link = industry_instance.web_link

    dates_dict={"03":31,
                "06":30,
                "09":30,
                "12":31
                }
    
    dia=dates_dict[mes]

    configurador=industry_instance.build_configurator_to_scrapping(año,mes)

    useful_dates=[f"{año}-{mes}-{dia}",f"{año-1}-12-31"]

    scrapper_instance=Cmf_scrapper()
    scrapper_instance.enter_main_page(empresa_link,configurador)
    xbrl_url=scrapper_instance.find_xbrl()
    
    scrapper_instance.close_driver() 

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

if __name__=="__main__":
    get_industry_data("besalco")
