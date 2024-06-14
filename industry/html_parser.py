import pandas as pd
import numpy as np
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


    def get_historic_data(self,empresa="besalco",desde=2018,hasta=None):

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
        for empresa in ["SIGDO KOPPERS S.A.","besalco"]:
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
                if sheet_name in [ "310000", "510000"]:

                        # Construct all quarter data
                    df=self.construct_all_quarter_data(df)
                    df=self.delete_col_is_not_quarter_data(df)
                    df=self.change_quarter_cols_names(df)

                                    # Convert column names to datetime
                    df.columns = pd.to_datetime(df.columns.map(self.parse_quarter))

                elif sheet_name=="210000":
                    df.columns = pd.to_datetime(df.columns)

                df = df.sort_index(axis=1)
                df.columns = df.columns.map(self.format_quarter)

                """
                aca va funcion para odernar fechas y para cambiar datos en 51000 y 310000   y para cambiar fechas por Qs
                """
                df.to_excel(writer, sheet_name=sheet_name)

### AUX functions to clean and order the data ###

    def clean(self,df):
            df = df.replace('\.', '', regex=True)
            df = df.replace('-', 0)
            df = df.fillna(0)
            for index, row in df.iterrows():
                # Check if all values in the row are the same
                if row.nunique() == 1:
                    # Replace values with NaNs
                    df.loc[index] = np.nan
            df = df.apply(pd.to_numeric, errors='ignore')
            return(df)

    
    def construct_all_quarter_data(self,df): # 510000 or 310000

        cols = df.columns.tolist()
        # Iterate over the columns
        for col_name in cols:
            # Check if the column name contains 'Q' (indicating quarter data)
            año1=self.extract_string_in_position(col_name,[6,10])
            año2=self.extract_string_in_position(col_name,[23,27])

            mes1=self.extract_string_in_position(col_name,[11,13])
            mes2=self.extract_string_in_position(col_name,[28,30])

            
            condicion_años=año1==año2
            condicion_meses=int(mes2)-int(mes1)==2

        # condicion_last_quarter= int(mes2)==12

            if condicion_años and not condicion_meses:  # is not quarter but same year always entre mes1="01"
                try:
                    df=self.construct_quarter_by_past_quarter(df,col_name,año1,mes2)
                except:
                    df=self.construct_quarter_by_all_quarters(df, col_name, año1, mes2)
                
        return(df)

    def construct_quarter_by_past_quarter(self,df,col_name,año_target,mes2_target): # asume that there exist a quarter of the form 01-(mes2-3) and the date is in the same year

        dates_dict={"03":31,
                    "06":30,
                    "09":30,
                    "12":31
                    }
        
        mes2=int(mes2_target)-3
        mes2=f"0{mes2}"
        target_col_name=f"Desde {año_target}-01-01 Hasta {año_target}-{mes2}-{dates_dict[mes2]}"

        mes1_target=f"0{int(mes2_target)-2}" if int(mes2_target)<12 else f"{int(mes2_target)-2}"
        new_col_name=f"Desde {año_target}-{mes1_target}-01 Hasta {año_target}-{mes2_target}-{dates_dict[mes2_target]}"

        df[new_col_name]=df[col_name]-df[target_col_name]  # maybe try here
        return(df)

    def construct_quarter_by_all_quarters(self,df, col_name, año_target, mes2_target): # asume that there exist all the previous quarters in the dataframe

       # cols = df.columns.tolist()

        dates_dict={"03":31,
                    "06":30,
                    "09":30,
                    "12":31
                    }
        
        cols_list=[]

        for mes2 in ["03","06","09"]:

            if int(mes2)<int(mes2_target):

                mes1_target=f"0{int(mes2_target)-2}" if int(mes2_target)<12 else f"{int(mes2_target)-2}"
                target_col_name=f"Desde {año_target}-{mes1_target}-01 Hasta {año_target}-{mes2}-{dates_dict[mes2]}"
                cols_list.append(target_col_name)

        assert len(cols_list)==int(mes2_target)//3-1
        # falta checkear que esten todas...
        # y checkea que no esten repetidas... (importnate)
        result = df[cols_list].sum(axis=1)



        mes1_target=f"0{int(mes2_target)-2}"
        new_col_name=f"Desde {año_target}-{mes1_target}-01 Hasta {año_target}-{mes2_target}-{dates_dict[mes2_target]}"

        df[new_col_name]=df[col_name]-result
        return(df)

    def extract_string_in_position(self,str,pos):
        if type(pos) ==list:
            str=str[pos[0]:pos[1]]

        elif type(pos)==int:
            str=str[pos]

        else:
            raise ValueError("pos must be a list or a string")
        return(str)
    
    def parse_quarter(self,quarter):
        year, q = quarter.split('Q')
        month = int(q) * 3 - 2  # Convert quarter to first month
        return pd.to_datetime(f'{year}-{month:02d}', format='%Y-%m')

    def format_quarter(self,date):
        return f'{date.year}Q{(date.month - 1) // 3 + 1}'
    
    
    def delete_col_is_not_quarter_data(self,df):
        """
        This function deletes columns that are not quarter data from a pandas DataFrame. Asume that all the quarters are in the dataframe. instead it will be removed

        Args:
            df (pandas.DataFrame): The input DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame with columns that are not quarter data removed.
        """
        # Get the column names as a list
        cols = df.columns.tolist()
        # Iterate over the columns
        for col_name in cols:
            # Check if the column name contains 'Q' (indicating quarter data)
            año1=self.extract_string_in_position(col_name,[6,10])
            año2=self.extract_string_in_position(col_name,[23,27])

            mes1=self.extract_string_in_position(col_name,[11,13])
            mes2=self.extract_string_in_position(col_name,[28,30])

            
            condicion_años=año1==año2
            condicion_meses=int(mes2)-int(mes1)==2

            if not (condicion_años and condicion_meses):  # is not quarter
                # Drop the column if it's not quarter data
                df.drop(col_name, axis=1, inplace=True)
        return(df)
    
    def change_quarter_cols_names(self,df):
        """ Function to change the columns names in the format Desde 2018-01-01 Hasta 2018-03-31' or 2018-03-31 to Q1
        The dataframe have to has the data in quarter reports 
        Args:
            df (pandas dataframe): dataframe with the data in quarter reports

        Returns:
            pandas dataframe: dataframe with the columns names in the format Q1, Q2, Q3, Q4
        """
        cols = df.columns.tolist()
        # Iterate over the columns
        dict={}
        for col_name in cols:
            # Check if the column name contains 'Q' (indicating quarter data)
            año1=self.extract_string_in_position(col_name,[6,10])
            año2=self.extract_string_in_position(col_name,[23,27])

            mes1=self.extract_string_in_position(col_name,[11,13])
            mes2=self.extract_string_in_position(col_name,[28,30])

            condicion_años=año1==año2
            condicion_meses=int(mes2)-int(mes1)==2

        # condicion_last_quarter= int(mes2)==12

            if condicion_años and condicion_meses:  # is quarter

                dict[col_name]=f"{año1}Q{int(mes2)//3}"
        df.rename(columns=dict,inplace=True)
                
        return df


    



if __name__=="__main__":

    instance=HTML_industry_data()
    instance.get_all_industry_historic_data(desde=2018)#,hasta=2020)






