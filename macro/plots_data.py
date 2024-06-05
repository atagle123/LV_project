from macro.get_data import Data   
import matplotlib.pyplot as plt
import os


class Plot_Data(Data):
    """ Class to plot the data series of Data class
    
    """
    
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
        """ Function to get the data series of Data

        Args:
          args (dict): dictionary with the arguments to get the data series
          
        Returns:
          data (DataFrame): data series of Data
        """
        data=self.get_data_from_args(args)
        return(data)
    
    def plot_serie(self,serie_name="",plot_args={}):
        """ Function to plot quickly the data series of Data

        Args:
          serie_name (str): name of the data series to plot
          plot_args (dict): dictionary with the arguments to plot the data series see the documentation: 
                            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html

        """
        fig, ax = plt.subplots(figsize=(8, 6))
        for col in self.data.columns:
            self.data[col].dropna().plot(ax=ax, label=col, **plot_args)
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
        plt.close()