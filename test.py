import bcchapi
import numpy as np
#siete = bcchapi.Siete("ataglem@ext.larrainvial.com", "Larra.2024")


from get_data import Data

data=Data()

data.download_data()
data.plot_data()
#data.plot_data()