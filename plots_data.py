from get_data import Data   
import matplotlib.pyplot as plt
import os


class Plot_Data(Data):
    
    def __init__(self, plot_directory="plots"):
        super().__init__()
        self.plot_directory=plot_directory
        if not os.path.exists( self.plot_directory):
              os.makedirs( self.plot_directory)

    """
    def make_plots(self):  # make plots from all the data in the data folder
        for file in os.listdir(self.data_directory):
            if file.endswith(".csv"):
                self.plot_serie(file)
    """
    def get_data_plots(self,args):
        self.get_data_from_args(args)
        
    def plot_serie(self,serie_name="",plot_args={}):
        """
        Function to plot the data series of Data
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        for col in self.data.columns:
            self.data[col].dropna().plot(ax=ax, label=col, **plot_args)
            #sns.lineplot(data=data[col], label=col)#, **plot_args)
        #  data.plot(**plot_args)
        plt.grid()
        plt.legend()
        plt.xlabel("Fecha")

        name=str(serie_name)
        if "title" in plot_args:
          name=str(plot_args["title"]) #falta probar
        elif self.name is not None:
          name=str(self.name)
        else:
          name=str(serie_name) # falta probar
        plt.title(name)
        plt.savefig(os.path.join(self.plot_directory, name))
    


















'''
json_plot_file ="plotting.json" # donde estan los plot de las series


    def preprocses_data(self):  # hacer preprocess normal
        
        for i,data in self.data_list:
            self.data_list[i]=data.dropna()
            
        return(None)
        
    def match_lists(self,list_1,list_2): # list 1 es la mas larga
        list_empty_dicts=[{} for _ in range(len(list_1)-len(list_2))]
        list_2.extend(list_empty_dicts)
        return(list_2)
      '''