#encoding: utf-8
# # Organización de datos
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


weather = pd.read_csv('data/parsed_weather.csv', low_memory=False)
station = pd.read_csv('data/parsed_station.csv', low_memory=False)
train = pd.read_csv('data/parsed_trip_train.csv', low_memory=False)
test = pd.read_csv('data/parsed_trip_test.csv', low_memory=False)


train_with_stations = pd.merge(train,station, how='inner', left_on='start_station_id', right_on='station_id')
train_with_stationweather = pd.merge(train_with_stations, weather, on=['date','city'], how='inner')
train_with_stationweather.to_csv('data/trips_train_with_stationweather.csv', index=False)


test_with_stations = pd.merge(test,station, how='inner', left_on='start_station_id', right_on='station_id')
test_with_stationweather = pd.merge(test_with_stations, weather, on=['date','city'], how='inner')
test_with_stationweather.to_csv('data/trips_test_with_stationweather.csv', index=False)