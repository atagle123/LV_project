import pandas as pd
import numpy as np
import io
import os
import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from industry.data_manager import Manage_Data


class HTML_parser:
    """ Base class to manage the HTML tables.
        Given html string parse to a list of dataframes with pandas.

    """
    def __init__(self,html):
        try:
            self.df_list=pd.read_html(io.StringIO(html))
        except:
            print("No tables extracted from html")
            self.df_list=[]


    def search_concept(self,concept):
        """ 
        Function that search a given concept in the tables and returns the FIRST dataframe with the concept
        Note that first is enough for the task of searching accountability ID's

        Args:
            concept (str): concept to match
        
        Returns:
            df (pandas.df): dataframe with given concept

        """
        for df in self.df_list:
            if len(df.filter(like=concept).columns)>0:
                df=self.multi_index_create(df) 
                return df  # returns first df with the concept match (should work fine)
            
        print("Concept not found")

    def search_concept_list(self,concept_list):
        """ 
        Function that search a given list of concept in the tables and returns a dict {concept:df,...}
        calls method search_concept

        Args:
            concept list (list of str): list of concepts to match
        
        Returns:
            dict: dict of concepts and dataframes

        """
        dict={}
        for concept in concept_list:
            df=self.search_concept(concept)
            dict[concept]=df
        return(dict)
    
    def multi_index_create(self,df):
        """ Function that creates a multi index to a df in the given way desired.

        Args: 
            df: df without complete index

        Returns:
            df: df with index
        """
        df["category"]=""
        last_category=""
        for row_idx, row in df.iterrows():

            actual_name=df.iloc[row_idx,0]
            post_name=df.iloc[row_idx,1]

            if actual_name==post_name:
                last_category=actual_name
           # df["category"].iloc[row_idx]=last_category
            df.loc[row_idx,"category"]=last_category
        df.set_index([df.columns.values[i] for i in [-1,0]],inplace=True)

        return(df)


class HTML_industry_data(Manage_Data):
    """ 
    HTML industry class that works by specific industry name, and saerch specific concepts, the class assumes that ALL the data is previously downloaded by the scrapper
    the objective of the class is to extract and parse the html tables of the CMF industries data.
    
    """
    def __init__(self,industry):
        super().__init__() # data manager class, to get and download the data

        self.industry=industry

        ### data paths ###
        current_dir = os.getcwd()
        self.html_path=os.path.join(current_dir, "data","industrydata",industry,"raw","html")
        self.csv_path=os.path.join(current_dir, "data","industrydata",industry,"results","csv")
        self.excel_path=os.path.join(current_dir, "data", "industrydata",industry,"results", "excel")


    def get_historic_data(self,desde=2018,hasta=None):
        """
        Function that gets all the historic data of the concept_list, from the html savepath

        Args:
            desde (int): initial year to get the data
            hasta (int): If None current year is used
        
        Returns:
            dict: A dict with concepts as keys, and the merged dataframe from all the periods of the industry ej: {210000: df,...}
        
        """

        concept_list=["210000","310000","510000"]

        dict_list={key: [] for key in concept_list}


        hasta = hasta or  datetime.datetime.now().year

        for año in range(desde,hasta+1):
            for mes in ["03","06","09","12"]:

                df_dict=self.get_one_period_data(año, mes,concept_list)

                for keys,values in df_dict.items(): 

                    dict_list[keys].append(values)

        ### Join dataframes ###
        for keys,values in dict_list.items():
            self.check_index(df_list=values)

            dict_list[keys]=pd.concat(values,join="outer",axis="columns")

        return(dict_list)

    
    def get_one_period_data(self, año, mes,concept_list):
        """
        Function that gets one period data from the html savepath

        Args: 
            año (int): Year to search the file
            mes (str): Quarter to search the file could be one of: (03,06,09,12)
            concept_list (list of str): list of strings of concepts to search in the tables

        Returns:
            dict: A dict with concepts as keys, and the dataframe from the given period of the industry ej: {210000: df,...}
        
        """
        
        html_path=os.path.join(self.html_path,f"html_{año}_{mes}") # specific path to the file
        ### change this for the data manager class
        try:
            html_content=self.open_file(file_path=html_path,extension="txt")

            html_instance=HTML_parser(html_content)
            df_dict=html_instance.search_concept_list(concept_list)
            return(df_dict)
        
        except FileNotFoundError:
            print(f"Not found file: html_{año}_{mes} for {self.industry}")
            return({})


    def process_and_save_historic_data(self,desde=2018,hasta=None):
        """ 
        Function that gets the historic data of the industry, preprocess it and save it into excel format

        Args:
            desde (int): initial year to get the data
            hasta (int): If None current year is used
            
        """

        df_dict=self.get_historic_data(desde,hasta)

        for keys,df in df_dict.items():
            if df is not None:
                check=self.column_checker(df)  # check the columns of the dataframe to robust results 
                print("Column checker: ", check)
                df_dict[keys] = df.loc[:,~df.columns.duplicated()].copy()
            else: 
                print("df is None")

        self.save_file_excel(df_dict, filename=self.industry)

    def check_index(self,df_list):
        """
        Sanity check if index is unique
        
        """
        for i,df in enumerate(df_list):
            if df is not None:
                print("Index is unique: ", df.index.is_unique)

            else:
                print( i, "df is None")


    def column_checker(self,df):
        """
        Function that given a dataframe checks all the columns and return False if one duplicated columns are not equal.

        Args:
            df (pandas.df): df to check columns

        Returns:
            bool: True if the dataframe it's fine False if not

        Obs:
            This function is very important and could be more robust and more efficent
        
        """
        columns = df.columns
        num_columns = len(columns)
        
        for i in range(num_columns):
            for j in range(i + 1, num_columns):
                if columns[i] == columns[j] and not df[columns[i]].equals(df[columns[j]]):
                    return False
        return True

    def save_file_csv(self,df,filename): #excel o csv
        """
        Function that saves df in csv format in the csv path
        
        Args: 
            df (pandas.df): df to save
            filename (str): name of the file
        
        """

        os.makedirs(self.csv_path, exist_ok=True)

        filepath= os.path.join(self.csv_path, f"{filename}.csv")
        df.to_csv(filepath)


    def save_file_excel(self, df_dict, filename): #excel o csv
        """
        Function that saves df in excel format in the excel path
        This funciton also do specific preprocessing for concepts before saving to excel 
        
        Args: 
            df_dict (dict of pandas.df): dict of df's to save 
            filename (str): name of the file
        
        """

        os.makedirs(self.excel_path, exist_ok=True)
        filepath=os.path.join(self.excel_path, f"{filename}.xlsx")

        with pd.ExcelWriter(filepath) as writer:
            # Iterate over the dictionary and write each DataFrame to a separate Excel sheet
            for sheet_name, df in df_dict.items():
                df=self.main_cleaning_pipeline(df,concept_type=sheet_name) # se aplica preprocesamiento por concepto 
                
                df.to_excel(writer, sheet_name=sheet_name)

    def main_cleaning_pipeline(self,df,concept_type):
        
        processing_functions={
        "310000": self.process_310000,
        "510000": self.process_310000,
        "210000": self.process_210000,
            }

        if concept_type in processing_functions:
            processing_function = processing_functions[concept_type]
            processed_df = processing_function(df)

        return processed_df
    
    def process_310000(self,df): # or 510000

        df=self.clean(df)
        # Construct all quarter data
        df=self.construct_all_quarter_data(df)
        df=self.delete_col_is_not_quarter_data(df)
        df=self.change_quarter_cols_names(df)

        # Convert column names to datetime
        df.columns = pd.to_datetime(df.columns.map(self.parse_quarter))

        df = df.sort_index(axis=1)
        df.columns = df.columns.map(self.format_quarter)
        return(df)
    
    def process_210000(self,df):
        df=self.clean(df)
        df.columns = pd.to_datetime(df.columns)

        df = df.sort_index(axis=1)
        df.columns = df.columns.map(self.format_quarter)
        return(df)

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

    instance=HTML_industry_data("besalco")
    instance.process_and_save_historic_data(desde=2018)#,hasta=2020)






