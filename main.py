from macro.plots_data import Plot_Data
from utils.json_utils import read_json

json_series_file="series.json"


if __name__=="__main__":
    print("Executing main...")
    args_list=read_json(json_series_file)
    for args in args_list:
        plot=Plot_Data()
        plot.get_data_plots(args)
        plot.plot_serie()