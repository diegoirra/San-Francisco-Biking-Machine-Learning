#encoding: utf-8
# # Organización de datos
# 
# ## Grupo Kernel for Machines that can't Learn good:
# 
# ### Bacigaluppo, Ivan
# ### Irrazabal, Diego
# 

import pandas as pd
import numpy as np
#import seaborn as sns
#import datetime as dt
import os
os.chdir("..")


weather = pd.read_csv('data\weather.csv',
                    parse_dates=['date'], infer_datetime_format=True,
                    low_memory=False)

#Parseo las fechas
weather.date = weather.date.dt.date

weather['city'] = weather['zip_code']
weather['city'] = weather['city'].replace(94301, 'Palo Alto')
weather['city'] = weather['city'].replace(95113, 'San Jose')
weather['city'] = weather['city'].replace(94041, 'Mountain View')
weather['city'] = weather['city'].replace(94107, 'San Francisco')
weather['city'] = weather['city'].replace(94063, 'Redwood City')
# zipcodes verificados de www.unitedstateszipcodes.org

weather['events'] = weather['events'].replace('rain', 'Rain')
weather['events'] = weather['events'].replace(np.nan, 'Clear')


'''NOS SIRVE STATION?'''
station = pd.read_csv('data/station.csv', low_memory=False)

station['coordinates'] = list(zip(station.lat, station.long))
station['station_id'] = station.id
station = station[['station_id', 'name', 'dock_count', 'city', 'coordinates']]


trips = pd.read_csv('data/trip_train.csv',
                    parse_dates=['start_date', 'end_date'], infer_datetime_format=True,
                    low_memory=False)

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

# filtraremos registros con duraciones menores a 5 minutos (300 segundos)y más 24hrs (86400 segundos)
trips = trips[(trips.duration >=300) & (trips.duration <= 86400)]
trips['date'] = trips.start_date
trips['trip_id'] = trips.id

trips = trips[['trip_id','duration','date', 'season',
               'start_station_name','start_station_id','start_time','start_hour', 'day_of_week',
               'end_time','end_hour','end_station_name','end_station_id', 'subscription_type']]


#Merge 1
'''NECESITAMOS STATIONS?????'''
trips_with_stations = pd.merge(trips,station, how='inner',
                              left_on='start_station_id', right_on='station_id')


#Merg 2: weather
trips_with_stationweather = pd.merge(trips_with_stations, weather,
                                     on=['date','city'], how='inner')


trips_with_stationweather.to_csv('data/trips_with_stationweather.csv', index=False)
