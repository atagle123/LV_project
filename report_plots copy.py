import matplotlib.pyplot as plt
from plots_data import Plot_Data
from get_data import Data

from utils.json_utils import get_json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils.cchc_preprocess import download_excel_to_df,preprocess_iCE,preprocess_ventas_santiago
from utils.download_data import download_dfs

#################################################################
### A script for create the required plots in a scpecific way ###
#################################################################

###
## Get all the data ##
#######################





args_mensual=  {
        "series":["F022.VIV.TIP.MA03.UF.Z.M",
                  "F034.CST.FLU.INE.Z.0.M",
                  "F032.IMC.IND.Z.Z.EP18.Z.Z.0.M",
                  "F034.PCC.IND.CCHC.2014.0.M",
                  "G089.IME.IND.A0.M"

                  ],
        "nombres" : ["Tasas anuales reajustadas UF",
                     "Permisos de construccion para vivienda (m2)",
                     "IMACEC",
                     "IMACON",
                     "IMCE"],
        "desde": "2010-01-01"  
    }


data=Data()
df_mensual=data.get_data_from_args(args_mensual)

args_trimestral=  {
        "series":["F034.VVNN.FLU.CCHC.Z.0.T",
                  "F034.EACPH.IND.BCCH.Z.Z.T",
                  "F034.EACEI.IND.BCCH.Z.Z.T",
                  "F034.IPVD.FLU.BCCH.2008.0.T"],
        "nombres" : ["Venta viviendas nuevas",
                     "Percepcion de estándares de aprobación de créditos hipotecarios",
                     "Percepcion de estándares de aprobación de créditos de construccion inmobiliaria",
                     "IPV Departamentos"],
        "desde": "2010-01-01"

        
  
    }

data=Data()
df_trimestral=data.get_data_from_args(args_trimestral)


### datos cchc


df_ice=download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/ICEAltura.xls",filename="ICEAltura")
new_column_mapping={0: 'Year', 1: 'Month',5:"Índice general", 14:"Materiales peso",15:"Salarios peso",16:"Subcontratos peso",17:"Misceláneos peso"}
df_ice=preprocess_iCE(df_ice,new_column_mapping) # mensual append to other df


df_oferta_vivienda=download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/GranSantiagoMercadoWeb.xls",filename="GranSantiagoMercadoWeb",sheet_name=1)
df_oferta_vivienda=preprocess_ventas_santiago(df_oferta_vivienda) # trimestral 


df_mensual=pd.merge(df_mensual, df_ice, how='outer', left_index=True, right_index=True)
df_trimestral=pd.merge(df_trimestral,df_oferta_vivienda, how='outer', left_index=True, right_index=True)

df_dict={"Mensual":df_mensual,"Trimestral":df_trimestral}  # ver que hago con variaciones? ver como queda y ver que se hace...

#download_dfs(df_dict, "all_data")

df=pd.merge(df_mensual, df_trimestral, how='outer', left_index=True, right_index=True)

mask = (df.index >= "2010-01-01")
df=df[mask]
"""
traer 4 dfs variacion, año, mensual,trimestral
unir correspondientes dfs descargados de la cchc
descargar excel con funcion nueva

unir TODOS los dfs
va a tocar crear un dataframe nuevo quizas para cada plot...
para plots, select por plots y hacer dropna si es que hay frecuencias mezcladas


"""
###new plots


##################################
###  grafico1 ###
##################################

title="grafico 1"

df_plot=pd.DataFrame()
df_plot["Tasas anuales hipotecarias reajustadas UF diff % YoY"]=df['Tasas anuales reajustadas UF'].shift(-12)-df['Tasas anuales reajustadas UF']
df_plot["Tasas anuales hipotecarias reajustadas UF diff % YoY"]=df_plot["Tasas anuales hipotecarias reajustadas UF diff % YoY"].shift(12)

df_plot["Número de viviendas vendidas Var % YoY"]=(df['Viviendas ventas'].shift(-12)-df['Viviendas ventas'])/df['Viviendas ventas']*100
df_plot["Número de viviendas vendidas Var % YoY"]=df_plot["Número de viviendas vendidas Var % YoY"].shift(12)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

ax1.set_ylabel("Diff %")
ax2.set_ylabel("Var %")

df_plot["Tasas anuales hipotecarias reajustadas UF diff % YoY"].dropna().plot(use_index=True,y="Tasas anuales hipotecarias reajustadas UF diff % YoY",ax=ax1,color="midnightblue",lw=3)
df_plot["Número de viviendas vendidas Var % YoY"].dropna().plot(use_index=True,y="Número de viviendas vendidas Var % YoY",title=title,ax=ax2,color="orange",lw=3)

ax1.set_label('IMACON')
ax2.set_label('Ventas casas nuevas')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xlabel('Fecha')
plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 2 ###
##################################

title="grafico2"

df_plot=pd.DataFrame()
df_plot["Venta viviendas nuevas Var % YoY"]=(df['Venta viviendas nuevas'].shift(-12)-df['Venta viviendas nuevas'])/df['Venta viviendas nuevas']*100
df_plot["Venta viviendas nuevas Var % YoY"]=df_plot["Venta viviendas nuevas Var % YoY"].shift(12)
df_plot['Percepcion de estándares de aprobación de créditos hipotecarios']=df[ 'Percepcion de estándares de aprobación de créditos hipotecarios']
df_plot.dropna().plot(title=title, color=["orange", "midnightblue"], lw=3)

plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 3 ###
##################################

title="grafico3"


df_plot=pd.DataFrame()
df_plot['Percepcion de estándares de aprobación de créditos hipotecarios']=df['Percepcion de estándares de aprobación de créditos hipotecarios']
df_plot["Percepcion de estándares de aprobación de créditos de construccion inmobiliaria"]=df['Percepcion de estándares de aprobación de créditos de construccion inmobiliaria']

df_plot.dropna().plot(title=title, color=["orange", "midnightblue"], lw=3)

plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 4 ###
##################################

title="grafico4"

df_plot=pd.DataFrame()
df_plot['Permisos de construccion para vivienda (m2)']=(df['Permisos de construccion para vivienda (m2)']/(df['Permisos de construccion para vivienda (m2)'].shift(12))-1)*100
df_plot["Percepcion de estándares de aprobación de créditos de construccion inmobiliaria"]=df['Percepcion de estándares de aprobación de créditos de construccion inmobiliaria']

df_plot.dropna().plot( color=["orange", "midnightblue"], lw=3)


plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 5 ###
##################################

title="grafico5"



df_plot=pd.DataFrame()
df_plot['IMACON Var YoY']=(df['IMACON']/(df['IMACON'].shift(12))-1)*100
df_plot["IMCE"]=df['IMCE']
df_plot.dropna(inplace=True)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

ax1.set_ylabel("%")
ax2.set_ylabel("Niveles")

df_plot['IMACON Var YoY'].plot(ax=ax1,color="midnightblue",lw=3)
df_plot["IMCE"].dropna().plot(use_index=True,y="IMCE",title=title,ax=ax2,color="orange",lw=3)

ax1.set_label('IMACON')
ax2.set_label('IMCE')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xlabel('Fecha')

plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 6 ###
##################################

title="grafico6"



df_plot=pd.DataFrame()
df_plot['IMACON Var YoY']=(df['IMACON']/(df['IMACON'].shift(12))-1)*100
df_plot['IMACEC Var YoY']=(df['IMACEC']/(df['IMACEC'].shift(12))-1)*100
df_plot.dropna(inplace=True)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

ax1.set_ylabel("%")
ax2.set_ylabel("%")

df_plot['IMACON Var YoY'].plot(ax=ax1,color="midnightblue",lw=3)
df_plot["IMACEC Var YoY"].dropna().plot(title=title,ax=ax2,color="orange",lw=3)

ax1.set_label('IMACON Var YoY')
ax2.set_label('IMACEC Var YoY')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xlabel('Fecha')

plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 7 ######
##################################

title="grafico7"

df_plot=pd.DataFrame()
df_plot['Viviendas meses']=df['Viviendas meses']
df_plot['Viviendas meses'].dropna(inplace=True)
df_plot["Promedio histórico"]=df_plot['Viviendas meses'].mean()


df_plot.dropna().plot( color=["orange", "midnightblue"], lw=3)

plt.savefig(os.path.join("plots",title))
plt.close()


##################################
###  grafico 8 ######
##################################

title="grafico8"

df_plot=pd.DataFrame()
df_plot["IPV Departamentos Var YoY"]=(df["IPV Departamentos"]/(df["IPV Departamentos"].shift(12))-1)*100
df_plot["Índice general Var YoY"]=(df["Índice general"]/(df["Índice general"].shift(12))-1)*100
df_plot.dropna(inplace=True)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

ax1.set_ylabel("%")
ax2.set_ylabel("%")

df_plot['IPV Departamentos Var YoY'].plot(ax=ax1,color="midnightblue",lw=3)
df_plot["Índice general Var YoY"].dropna().plot(title=title,ax=ax2,color="orange",lw=3)

ax1.set_label('IPV Departamentos Var YoY')
ax2.set_label('Índice general Var YoY')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xlabel('Fecha')

plt.savefig(os.path.join("plots",title))
plt.close()



######################################
### Oferta viviendas Gran Santiago ###
######################################

title="Oferta viviendas Gran Santiago"

df_plot=pd.DataFrame()
df_plot=df.loc[:,["Departamentos stock","Casas stock","Viviendas meses"]]
df_plot.dropna(inplace=True)
df_plot["Period"]=df_plot.index
df_plot['Period']=df_plot['Period'].dt.to_period('Q')

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

plt.title(title)
plt.grid()

df_plot.plot(x="Period",y=["Departamentos stock","Casas stock"],kind="bar",use_index=False,stacked=True,ax=ax1,color=["midnightblue","powderblue"])
df_plot.plot(x="Period",y=["Viviendas meses"],use_index=False,kind="line",ax=ax2,color="orange",lw=3)

ax1.set_ylabel("Unidades")
ax2.set_ylabel("Meses")

plt.savefig(os.path.join("plots",title))
plt.close()


###############################################################
### Índice costos de edificación en altura desgolse Var YoY ###
###############################################################

title="Índice costos de edificación en altura desgolse Var YoY"

df_plot=pd.DataFrame()
df_plot=df.loc[:,["Materiales","Salarios","Subcontratos","Misceláneos","Índice general"]]
var=(df_plot.shift(-12)-df_plot)/df_plot*100
#var=df_plot/(df_plot.shift(12)-1)*100

### plot ###

fig, ax = plt.subplots(figsize=(8, 5))

ax=sns.lineplot(data=var,dashes=False,palette="rocket",lw=3).set_title(title)

plt.savefig(os.path.join("plots",title))
plt.close()

##############################################################################
### Contribución a Índice costos de edificación en altura desgolse Var YoY ###
##############################################################################


title="Contribución a Índice costos de edificación en altura desgolse Var YoY"

mat=var["Materiales"]*df["Materiales peso"].shift(-12)
sysal=var["Salarios"]*df["Salarios peso"].shift(-12)
subcon=var["Subcontratos"]*df["Subcontratos peso"].shift(-12)
misc=var["Misceláneos"]*df["Misceláneos peso"].shift(-12)

df_combined = pd.concat([mat, sysal, subcon, misc], axis=1)
df_combined=df_combined.dropna()
column_names={0:"Materiales",1:"Sueldos y Salarios",2:"Subcontratos",3:"Misceláneos"}
df_combined.rename(columns=column_names,inplace=True)


### plot ###

y=df_combined.to_numpy(dtype=float).T
y_stack = np.cumsum(y, axis=0)   
x=df_combined.index.to_numpy()
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.fill_between(x, 0, y_stack[0,:], facecolor="black", alpha=.7,label="Materiales")
ax1.fill_between(x, y_stack[0,:], y_stack[1,:], facecolor="darkslategrey", alpha=.7,label="Sueldos y Salarios")
ax1.fill_between(x, y_stack[1,:], y_stack[2,:], facecolor="darkred",label="Subcontratos")
ax1.fill_between(x, y_stack[2,:], y_stack[3,:], facecolor="midnightblue",label="Misceláneos")
plt.title(title)
plt.xlabel('Fecha')
plt.ylabel('%')
ax1.legend(loc="upper left")
plt.savefig(os.path.join("plots",title))
plt.close()


