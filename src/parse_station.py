#encoding: utf-8
# # Organizaci�n de datos
# 
# ## Grupo Kernel for Machines that can't Learn good:
# 
# ### Bacigaluppo, Ivan
# ### Irrazabal, Diego
# 

import pandas as pd
#import numpy as np
#import seaborn as sns
#import datetime as dt
import os
os.chdir("..")


station = pd.read_csv('data/station.csv', low_memory=False)

station['coordinates'] = list(zip(station.lat, station.long))
station['station_id'] = station.id
station = station[['station_id', 'name', 'dock_count', 'city', 'coordinates']]

station.to_csv('data/parsed_station.csv', index=False)