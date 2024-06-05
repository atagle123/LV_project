import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.cchc_preprocess import download_excel_to_df

current_dir = os.getcwd()
filepath=os.path.join(current_dir, "data\macrodata\excel")

df_ice=download_excel_to_df("https://cchc.cl/uploads/indicador/archivos/ICEAltura.xls",filepath,filename="ICEAltura")
