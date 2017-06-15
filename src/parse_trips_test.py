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


trips = pd.read_csv('data/trip_test.csv', parse_dates=['start_date', 'end_date'], infer_datetime_format=True, low_memory=False)

trips['season'] = trips.start_date.dt.month
trips.season = trips.season.replace(1, 'winter')
trips.season = trips.season.replace(2, 'winter')
trips.season = trips.season.replace(3, 'winter')
trips.season = trips.season.replace(4, 'spring')
trips.season = trips.season.replace(5, 'spring')
trips.season = trips.season.replace(6, 'spring')
trips.season = trips.season.replace(7, 'summer')
trips.season = trips.season.replace(8, 'summer')
trips.season = trips.season.replace(9, 'summer')
trips.season = trips.season.replace(10, 'autumn')
trips.season = trips.season.replace(11, 'autumn')
trips.season = trips.season.replace(12, 'autumn')

#separamos la fecha de las hora
trips['start_time'] = trips.start_date.dt.time
trips['start_hour'] = trips.start_date.dt.hour
trips['day_of_week'] = trips.start_date.dt.dayofweek
trips['start_date'] = trips.start_date.dt.date

trips['end_time'] = trips.end_date.dt.time
trips['end_hour'] = trips.end_date.dt.hour
trips['end_date'] = trips.end_date.dt.date

trips['date'] = trips.start_date
trips['trip_id'] = trips.id

trips = trips[['trip_id','date', 'season','start_station_id','end_station_id',
               'start_hour','day_of_week', 'subscription_type']]

trips.to_csv('data/parsed_trips_test.csv', index=False)
