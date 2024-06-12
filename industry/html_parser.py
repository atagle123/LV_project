import pandas as pd
import io
import os
import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from utils import build_website_link_from_industry,build_configurator_to_scrapping
from industry.scrapping import Cmf_scrapper


class HTML_parser:
    def __init__(self,html):
        self.df_list=pd.read_html(io.StringIO(html))
    
    def search_concept(self,concept):
        for df in self.df_list:
            if len(df.filter(like=concept).columns)>0:
                df=self.multi_index_create(df)

                return df  # returns first df with the concept match (should work fine)
            
        print("Concept not found")

    def search_concept_list(self,concept_list):
        dict={}
        for concept in concept_list:
            df=self.search_concept(concept)
            dict[concept]=df
        return(dict)
    
    def multi_index_create(self,df):
        df["category"]=""
        
        for row_idx, row in df.iterrows():

            actual_name=df.iloc[row_idx,0]
            post_name=df.iloc[row_idx,1]

            if actual_name==post_name:
                last_category=actual_name
           # df["category"].iloc[row_idx]=last_category
            df.loc[row_idx,"category"]=last_category
        df.set_index([df.columns.values[i] for i in [-1,0]],inplace=True)

        return(df)




class HTML_industry_data():
    def __init__(self):

        current_dir = os.getcwd()
        self.csv_path=os.path.join(current_dir, "data","industrydata","html","csv")
        self.excel_path=os.path.join(current_dir, "data", "industrydata", "html", "excel")


    def get_historic_data(self,empresa="falabella",desde=2018,hasta=None):

        concept_list=["210000","310000","510000"]

        pd_list=[[] for _ in range(len(concept_list))]
        dict_list=dict(zip(concept_list,pd_list))

        empresa_link = build_website_link_from_industry(empresa)

        hasta = hasta or  datetime.datetime.now().year

        for año in range(desde,hasta+1):
            for mes in ["03","06","09","12"]:

                df_dict=self.get_one_period_data(año, mes,empresa_link,concept_list)

                for keys,values in df_dict.items():

                    dict_list[keys].append(values)

        for keys,values in dict_list.items():
            for i,df in enumerate(values):
                if df is not None:
                   print(keys,i,"Index is unique: ", df.index.is_unique)
                else:
                    print(keys, i, "df is None")

            dict_list[keys]=pd.concat(values,join="outer",axis="columns")

        return(dict_list)
    
    def get_one_period_data(self, año, mes,empresa_link,concept_list):

        configurador=build_configurator_to_scrapping(año,mes)  # arreglar lo de si no encuentra la fecha
        scrappy_instance=Cmf_scrapper()
        html=scrappy_instance.get_html(empresa_link,configurador)
        html_instance=HTML_parser(html)
        df_dict=html_instance.search_concept_list(concept_list)

        return(df_dict)


    def get_all_industry_historic_data(self,desde=2018,hasta=None):
        for empresa in ["besalco"]:
            df_dict=self.get_historic_data(empresa, desde,hasta)

            for keys,df in df_dict.items():
                if df is not None:
                    check=self.column_checker(df)
                    print("Column checker: ", check)
                    df_dict[keys] = df.loc[:,~df.columns.duplicated()].copy()
                else: 
                    print("df is None")

            self.save_file_excel(df_dict, filename=empresa)


    def column_checker(self,df):
        columns = df.columns
        num_columns = len(columns)
        for i in range(num_columns):
            for j in range(i + 1, num_columns):
                if columns[i] == columns[j] and not df[columns[i]].equals(df[columns[j]]):
                    return False
        return True

    def save_file_csv(self,df,filename): #excel o csv

        os.makedirs(self.csv_path, exist_ok=True)

        filepath= os.path.join(self.csv_path, f"{filename}.csv")
        df.to_csv(filepath)


    def save_file_excel(self, df_dict, filename): #excel o csv

        os.makedirs(self.excel_path, exist_ok=True)
        filepath=os.path.join(self.excel_path, f"{filename}.xlsx")

        with pd.ExcelWriter(filepath) as writer:
            # Iterate over the dictionary and write each DataFrame to a separate Excel sheet
            for sheet_name, df in df_dict.items():
                df=self.clean(df)
                """
                aca va funcion para odernar fechas y para cambiar datos en 51000 y 310000   y para cambiar fechas por Qs
                """
                df.to_excel(writer, sheet_name=sheet_name)

    def clean(self,df):
        for index, row in df.iterrows():
            # Check if all values in the row are the same
            if row.nunique() == 1:
                # Replace values with NaNs
                df.loc[index] = np.nan   
        return(df)


if __name__=="__main__":

    instance=HTML_industry_data()
    instance.get_all_industry_historic_data(desde=2018)






