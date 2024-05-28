import matplotlib.pyplot as plt
from plots_data import Plot_Data
from utils.json_utils import get_json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils.cchc_preprocess import download_excel_to_df,preprocess_iCE,preprocess_ventas_santiago


#################################################################
### A script for create the required plots in a scpecific way ###
#################################################################

##################################
###  IMACEC vs IMACON vs IMCE  ###
##################################

args={
        "series":["F032.IMC.IND.Z.Z.EP18.Z.Z.0.M","F034.PCC.IND.CCHC.2014.0.M","G089.IME.IND.A0.M"],
        "nombres" : ["IMACEC","IMACON","IMCE"],
        "desde":"2010-01-01"
    }

title="IMACEC vs IMACON vs IMCE"

plot=Plot_Data()
df=plot.get_data_plots(args)

### plot ###

df.plot(title=title, color=["midnightblue", "orange", "powderblue"], lw=3)
plt.xlabel("Fecha")
plt.ylabel("Índice")
plt.savefig(os.path.join("plots",title))
plt.close()

#############################################################
#### Evolución promesas vs viviendas autorizadas Var YoY ####
#############################################################

args={
        "series":["F034.VVNN.FLU.CCHC.Z.0.T","F034.CVN.FLU.INE.Z.0.M"],
        "nombres" : ["Promesas compra venta","Número de viviendas autorizadas"],
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"Promesas compra venta":"last", "Número de viviendas autorizadas":"last"}

    }


title="Evolución promesas vs viviendas autorizadas Var YoY"

plot=Plot_Data()
df=plot.get_data_plots(args)
df=df.dropna(subset="Promesas compra venta")
### plot ###

df.plot(kind="line",title=title,color=["midnightblue","orange"],lw=3)
plt.xlabel("Fecha")
plt.ylabel("%")
plt.savefig(os.path.join("plots",title))
plt.close()



###############################################################
#### Préstamos hipotecarios vs Préstamos Totales % del PIB ####
###############################################################

args={
        "series":["F038.DEUD.PPB2.53.10.N.2018.CLP.T","F038.DEUBH.PPB2.53.10.N.2018.CLP.T"],
        "nombres" :["Deuda total % PIB","Deuda hipotecaria % PIB"]
  
    }

title="Préstamos hipotecarios vs Préstamos Totales % del PIB"

plot=Plot_Data()
df=plot.get_data_plots(args)

### plot ###

df.plot(title=title,color=["midnightblue","orange"],lw=3)

plt.xlabel("Fecha")
plt.ylabel("% del PIB")

plt.savefig(os.path.join("plots",title))
plt.close()

###########################################################
### Préstamos hipotecarios vs Préstamos Totales Var YoY ###
###########################################################

args={
        "series":["F038.DEUD.PPB2.53.10.N.2018.CLP.T","F038.DEUBH.PPB2.53.10.N.2018.CLP.T"],
        "nombres" :["Deuda total","Deuda hipotecaria"],
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"Deuda total":"last", "Deuda hipotecaria":"last"}
  
    }

title="Préstamos hipotecarios vs Préstamos Totales Var YoY"

plot=Plot_Data()
df=plot.get_data_plots(args)
df=df*100

### plot ###

df.plot(title=title,color=["midnightblue","orange"],lw=3)

plt.xlabel("Fecha")
plt.ylabel("%")

plt.savefig(os.path.join("plots",title))
plt.close()



#########################################
### IMACON vs viviendas autorizadas #####
#########################################

args={
        "series":["F034.CST.FLU.INE.Z.0.M","F034.PCC.IND.CCHC.2014.0.M"],
        "nombres" : ["Número de viviendas autorizadas","IMACON"]
    }


title="IMACON vs viviendas autorizadas"

plot=Plot_Data()
df=plot.get_data_plots(args)

df=df*100   
df['Date'] = df.index
df=df.dropna(subset="Número de viviendas autorizadas")

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))

ax2 = ax1.twinx()

df.plot(x="Date",y="IMACON",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Date",y="Número de viviendas autorizadas",title=title,ax=ax2,color="orange",lw=3)
ax1.set_ylabel("IMACON")
ax2.set_ylabel("Miles")

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig(os.path.join("plots",title)) 
plt.close()

###################################################
### IMACON vs viviendas autorizadas Var YoY #######
###################################################


args=    {
        "series":["F034.CST.FLU.INE.Z.0.M","F034.PCC.IND.CCHC.2014.0.M"],
        "nombres" : ["Número de viviendas autorizadas","IMACON"],
        "desde":"2008-01-01",    # tentativo
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"Número de viviendas autorizadas":"last", "IMACON":"last"}
    }


title="IMACON vs viviendas autorizadas Var YoY"

plot=Plot_Data()
df=plot.get_data_plots(args)

df=df*100   
df['Date'] = df.index

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

df.plot(x="Date",y="IMACON",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Date",y="Número de viviendas autorizadas",title=title,ax=ax2,color="orange",lw=3)

ax1.set_ylabel("% Imacon")
ax2.set_ylabel("% Número viviendas")

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig(os.path.join("plots",title))
plt.close()

##############################################################
### Ventas inmobiliarias vs tasas de interes hipotecarias ###
##############################################################


args=        {
        "series":["F034.VVNN.FLU.CCHC.Z.0.T","F022.VIV.TIP.MA03.UF.Z.M"],
        "nombres" : ["Venta viviendas nuevas","Tasas anuales reajustadas UF"]  
    }

title="Ventas inmobiliarias vs tasas de interes hipotecarias"

plot=Plot_Data()
df=plot.get_data_plots(args)

df=df.dropna(subset="Venta viviendas nuevas")

df=df*100   
df['Date'] = df.index

### plot ###
fig, ax1 = plt.subplots(figsize=(8, 5))

ax2 = ax1.twinx()

df["Tasas anuales reajustadas UF"]=df["Tasas anuales reajustadas UF"]/100

df.plot(x="Date",y="Tasas anuales reajustadas UF",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Date",y="Venta viviendas nuevas",title=title,ax=ax2,color="orange",lw=3)

ax1.set_ylabel("%")
ax2.set_ylabel("Miles")

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig(os.path.join("plots",title)) 
plt.close()


##############################################################
### Índice costos de edificación desgolse Var YoY ############
##############################################################

title="Índice costos de edificación desgolse Var YoY"

df=download_excel_to_df()
df=preprocess_iCE(df)

df_new=df.loc[:,["Materiales","Sueldos y Salarios","Misceláneos","Índice general"]]
df_new.index.name="Fecha"
var=(df_new.shift(-12)-df_new)/df_new*100
var=var.iloc[250:,:]

### plot ###

fig, ax = plt.subplots(figsize=(8, 5))

ax=sns.lineplot(data=var,dashes=False,palette="rocket").set_title(title)
plt.ylabel('%')

plt.savefig(os.path.join("plots",title))
plt.close()

####################################################################
### Contribución a Índice costos de edificación desgolse Var YoY ###
####################################################################


title="Contribución a Índice costos de edificación desgolse Var YoY"

mat=var["Materiales"]*df["Materiales peso"].shift(-12)
sysal=var["Sueldos y Salarios"]*df["Sueldos y Salarios peso"].shift(-12)
misc=var["Misceláneos"]*df["Misceláneos peso"].shift(-12)

df_combined = pd.concat([mat, sysal, misc], axis=1)
column_names={0:"Materiales",1:"Sueldos y Salarios",2:"Misceláneos"}
df_combined.rename(columns=column_names,inplace=True)

### plot ###

sns.lineplot(data=df_combined,palette="rocket",dashes=False).set_title(title)
plt.ylabel('%')
plt.savefig(os.path.join("plots",title))
plt.close()

#############################
### IMACON vs PIB Var YoY ###
#############################

args=        {
        "series":["F034.PCC.IND.CCHC.2014.0.M","F032.PIB.FLU.R.CLP.2018.Z.Z.0.M"],
        "nombres" : ["IMACON","PIB"],
        "desde":"2008-01-01",    
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"IMACON":"last", "PIB":"last"}
    }

title="IMACON vs PIB Var YoY"

plot=Plot_Data()
df=plot.get_data_plots(args) 
df=df.dropna(subset=["PIB"])
df=df*100

### plot ###

fig, ax = plt.subplots(figsize=(8, 5))

df.plot(use_index=True,y=["IMACON","PIB"],kind="line",title=title,lw=3,color=["midnightblue","orange"],ax=ax)
plt.xlabel('Fecha')
plt.ylabel("%")
plt.savefig(os.path.join("plots",title))
plt.close()

#############################################
### IMACON vs Ventas casas nuevas Var YoY ###
#############################################

args=        {
        "series":["F034.PCC.IND.CCHC.2014.0.M","F034.CVV.FLU.BCCH.Z.CASN.T"],
        "nombres" : ["IMACON","Ventas casas nuevas"],
        "desde":"2008-01-01",    # tentativo
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"IMACON":"last", "Ventas casas nuevas":"last"}
    }

title="IMACON vs Ventas casas nuevas Var YoY"

plot=Plot_Data()
df=plot.get_data_plots(args)

df=df*100  
df['Fecha'] = df.index

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))

ax2 = ax1.twinx()

ax1.set_ylabel("%")
ax2.set_ylabel("%")

df.plot(x="Fecha",y="IMACON",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Fecha",y="Ventas casas nuevas",title=title,ax=ax2,color="orange",lw=3)

ax1.set_label('IMACON')
ax2.set_label('Ventas casas nuevas')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xlabel('Fecha')

plt.savefig(os.path.join("plots",title))  # idea agregar casas y deptos
plt.close()


####################################################################
### Ventas inmobiliarias vs Deuda bancaria hipótecaria % del PIB ###
####################################################################

args=        {
        "series":["F034.VVNN.FLU.CCHC.Z.0.T","F038.DEUBH.PPB2.53.10.N.2018.CLP.T"],
        "nombres" : ["Venta viviendas nuevas","Deuda bancaria hipótecaria % del PIB"]  
    }

title="Ventas inmobiliarias vs Deuda bancaria hipótecaria % del PIB"  

plot=Plot_Data()
df=plot.get_data_plots(args)  

df=df.dropna(subset="Venta viviendas nuevas")
df["Fecha"]=df.index

### plots ###

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

plt.title(title)

df.plot(x="Fecha",y="Venta viviendas nuevas",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Fecha",y="Deuda bancaria hipótecaria % del PIB",kind="line",ax=ax2,color="orange",lw=3)

ax1.set_ylabel("Unidades")
ax2.set_ylabel("% del PIB")
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig(os.path.join("plots",title))
plt.close()

############################################################################
### Ventas inmobiliarias vs Deuda bancaria hipótecaria % del PIB Var YoY ###
############################################################################

args=        {
        "series":["F034.VVNN.FLU.CCHC.Z.0.T","F038.DEUBH.PPB2.53.10.N.2018.CLP.T"],
        "nombres" : ["Venta viviendas nuevas","Deuda bancaria hipótecaria"],
        "desde":"2008-01-01",    # tentativo
        "variacion":12,
        "frecuencia":"YE",
        "observado":{"Venta viviendas nuevas":"last", "Deuda bancaria hipótecaria":"last"}
    }

title="Ventas inmobiliarias vs Deuda bancaria hipótecaria Var YoY"  

plot=Plot_Data()
df=plot.get_data_plots(args)  

df=df.dropna(subset="Venta viviendas nuevas")
df=df*100
df["Fecha"]=df.index

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()


df.plot(x="Fecha",y="Venta viviendas nuevas",ax=ax1,color="midnightblue",lw=3)
df.plot(x="Fecha",y="Deuda bancaria hipótecaria",title=title,ax=ax2,color="orange",lw=3)

ax1.set_ylabel("% Ventas")
ax2.set_ylabel("% Deuda")
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')   

plt.savefig(os.path.join("plots",title))
plt.close()



###################################################
### Índice Materiales e insumos de construcción ###
###################################################

args=        {
        "series":["F075.IPP.IND.F.2019.Z.M"],
        "nombres" : ["Índice Materiales e insumos de construcción"]
    }

plot_args={"kind":"line",
    "title":"Índice Materiales e insumos de construcción",
    "lw":3,
    "color":"midnightblue"
    }

plot=Plot_Data()
plot.get_data_plots(args)   # estandarizar este plot
plot.plot_serie(plot_args=plot_args)

######################################
### Oferta viviendas Gran Santiago ###
######################################

title="Oferta viviendas Gran Santiago"


df=download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/GranSantiagoMercadoWeb.xls",filename="GranSantiagoMercadoWeb",sheet_name=1)
df=preprocess_ventas_santiago(df)

### plot ###

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

plt.title(title)
plt.grid()

df.iloc[40:,:].plot(x="Period",y=["Departamentos stock","Casas stock"],kind="bar",stacked=True,ax=ax1,color=["midnightblue","powderblue"])
df.iloc[40:,:].plot(x="Period",y=["Viviendas meses"],kind="line",ax=ax2,color="orange",lw=3)

ax1.set_ylabel("Unidades")
ax2.set_ylabel("Meses")

plt.savefig(os.path.join("plots",title))
plt.close()


###############################################################
### Índice costos de edificación en altura desgolse Var YoY ###
###############################################################

title="Índice costos de edificación en altura desgolse Var YoY"

df=download_excel_to_df(url="https://cchc.cl/uploads/indicador/archivos/ICEAltura.xls",filename="ICEAltura")
new_column_mapping={0: 'Year', 1: 'Month',5:"Índice general", 14:"Materiales peso",15:"Salarios peso",16:"Subcontratos peso",17:"Misceláneos peso"}
df=preprocess_iCE(df,new_column_mapping)

df_new=df.loc[:,["Materiales","Salarios","Subcontratos","Misceláneos","Índice general"]]
df_new.index.name="Fecha"
var=(df_new.shift(-12)-df_new)/df_new*100

### plot ###

fig, ax = plt.subplots(figsize=(8, 5))

ax=sns.lineplot(data=var,dashes=False,palette="rocket",lw=3).set_title(title)
plt.ylabel('%')

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