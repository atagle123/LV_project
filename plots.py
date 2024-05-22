   

















def plot_data(self): # eventually use args
        
        plot_args_list=self.match_lists(self.args_list,self.plot_args_list)

        for plot_args,args,data in zip(plot_args_list,self.args_list,self.data_list):  # quizas hacer dos funciones separadas
          fig, ax = plt.subplots(figsize=(8,6))
          for col in data.columns:
              data[col].dropna().plot(ax=ax,label=col,**plot_args)
              #sns.lineplot(data=data[col], label=col)#, **plot_args)
        #  data.plot(**plot_args)
          plt.grid()
          plt.legend()
          plt.xlabel("Fecha")

          if "title" in plot_args:
            name=str(plot_args["title"]) #falta probar
          else:
            name=str(args["nombres"]) # falta probar
            plt.title(name)
          plt.savefig(os.path.join(self.plot_directory, name))

    def match_lists(self,list_1,list_2): # list 1 es la mas larga
        list_empty_dicts=[{} for _ in range(len(list_1)-len(list_2))]
        list_2.extend(list_empty_dicts)
        return(list_2)
        
if __name__ == "__main__":
    data=Get_data()


class Data:
    def __init__(self): 
        self.siete = bcchapi.Siete(file="credentials.txt")  # tiene que ser string # file="credenciales.txt" hacer mas seguro el logging con variables de ambiente
        self.data=None
        self.args_list=get_json(json_series_file)  # ver si hacer un args list o uno a uno
        self.plot_args_list=get_json(json_plot_file)  # ver si hacer un args list o uno a uno  # agregar el mapping de las funciones de agregacion y ver cuales hay , si no inventarlas.
      
        self.plot_directory="plots"
        if not os.path.exists( self.plot_directory):
              os.makedirs( self.plot_directory)

    def download_data(self):
        self.data_list=[]
        for args in self.args_list:
            self.data_list.append(self.siete.cuadro(**args))
        return(self.data_list)


    def preprocses_data(self):  # hacer preprocess normal
        
        for i,data in self.data_list:
            self.data_list[i]=data.dropna()
            
        return(None)
        

    def plot_data(self): # eventually use args
        
        plot_args_list=self.match_lists(self.args_list,self.plot_args_list)

        for plot_args,args,data in zip(plot_args_list,self.args_list,self.data_list):  # quizas hacer dos funciones separadas
          fig, ax = plt.subplots(figsize=(8,6))
          for col in data.columns:
              data[col].dropna().plot(ax=ax,label=col,**plot_args)
              #sns.lineplot(data=data[col], label=col)#, **plot_args)
        #  data.plot(**plot_args)
          plt.grid()
          plt.legend()
          plt.xlabel("Fecha")

          if "title" in plot_args:
            name=str(plot_args["title"]) #falta probar
          else:
            name=str(args["nombres"]) # falta probar
            plt.title(name)
          plt.savefig(os.path.join(self.plot_directory, name))

    def match_lists(self,list_1,list_2): # list 1 es la mas larga
        list_empty_dicts=[{} for _ in range(len(list_1)-len(list_2))]
        list_2.extend(list_empty_dicts)
        return(list_2)