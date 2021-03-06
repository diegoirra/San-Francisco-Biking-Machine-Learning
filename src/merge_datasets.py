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
train = pd.read_csv('data/parsed_trips_train.csv', low_memory=False)
train_filtered = pd.read_csv('data/parsed_trips_train_filtered.csv', low_memory=False)
test = pd.read_csv('data/parsed_trips_test.csv', low_memory=False)


train_with_stations_filtered = pd.merge(train_filtered,station, how='inner', left_on='start_station_id', right_on='station_id')
train_with_stationweather_filtered = pd.merge(train_with_stations_filtered, weather, on=['date','city'], how='inner')
train_with_stationweather_filtered = train_with_stationweather_filtered[['duration','season','start_station_id','end_station_id',
                                       'start_hour','day_of_week','subscription_type',
                                       'mean_temperature_f','mean_dew_point_f','mean_humidity',
                                       'mean_sea_level_pressure_inches','mean_visibility_miles',
                                       'mean_wind_speed_mph','max_gust_speed_mph',
                                       'precipitation_inches','events','wind_dir_degrees']]

train_with_stationweather_filtered.to_csv('data/trips_train_with_stationweather_filtered.csv', index=False)

train_with_stations = pd.merge(train,station, how='inner', left_on='start_station_id', right_on='station_id')
train_with_stationweather = pd.merge(train_with_stations, weather, on=['date','city'], how='inner')
train_with_stationweather = train_with_stationweather [['duration','season','start_station_id','end_station_id',
                              'start_hour','day_of_week','subscription_type',
                              'mean_temperature_f','mean_dew_point_f','mean_humidity',
                              'mean_sea_level_pressure_inches','mean_visibility_miles',
                              'mean_wind_speed_mph','max_gust_speed_mph',
                              'precipitation_inches','events','wind_dir_degrees']]

train_with_stationweather.to_csv('data/trips_train_with_stationweather.csv', index=False)

test_with_stations = pd.merge(test,station, how='inner', left_on='start_station_id', right_on='station_id')
test_with_stationweather = pd.merge(test_with_stations, weather, on=['date','city'], how='inner')
test_with_stationweather = test_with_stationweather[['trip_id','season','start_station_id','end_station_id',
                             'start_hour','day_of_week','subscription_type',
                             'mean_temperature_f','mean_dew_point_f','mean_humidity',
                             'mean_sea_level_pressure_inches','mean_visibility_miles',
                             'mean_wind_speed_mph','max_gust_speed_mph',
                             'precipitation_inches','events','wind_dir_degrees']]
test_with_stationweather.to_csv('data/trips_test_with_stationweather.csv', index=False)


