# # Organización de datos
# 
# ## Grupo:
# 
# ### Bacigaluppo, Ivan
# ### Irrazabal, Diego
# 

import datetime as datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pyspark

plt.style.use('default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)
get_ipython().magic(u'matplotlib inline')

station = pd.read_csv('data/station.csv', low_memory=False)


# # Analizando weather.csv

weather = pd.read_csv('data/weather.csv',
                    parse_dates=['date'], infer_datetime_format=True,
                    low_memory=False)

#Parseo las fechas
weather.date = weather.date.dt.date
weather.date.describe()

#Cambio los zip_codes
print set(station.city.values)
print set(weather.zip_code.values)

weather['city'] = weather['zip_code']

weather['city'] = weather['city'].replace(94301, 'Palo Alto')
weather['city'] = weather['city'].replace(95113, 'San Jose')
weather['city'] = weather['city'].replace(94041, 'Mountain View')
weather['city'] = weather['city'].replace(94107, 'San Francisco')
weather['city'] = weather['city'].replace(94063, 'Redwood City')
# zipcodes verificados de www.unitedstateszipcodes.org

weather['events'] = weather['events'].replace('rain', 'Rain')
weather['events'] = weather['events'].replace(np.nan, 'Clear')


# ## Analizando station.csv

# transformamos lat y long en tupla de coordenadas
station['coordinates'] = list(zip(station.lat, station.long))

# installation_date no nos sirve
# lat y long fueron incorporadas como tupla en coordinates
# los nombres pueden ser utiles para graficar
station['station_id'] = station.id

station = station[['station_id', 'name', 'dock_count', 'city', 'coordinates']]

#Cantidad de estaciones por ciudad
station_cities = station.groupby('city')
cant_station_city = station_cities['station_id'].count()


# # Cantidad de estaciones por ciudad

#Agrupo estaciones por ciudad
station_per_city = pd.DataFrame({'station_count' : station.groupby(['city'])['station_id'].count()}).reset_index()
station_per_city = station_per_city.sort_values(by='station_count', ascending=False)


# # Porcentaje de estaciones por ciudad
station_per_city['station_city_percentage'] = station_per_city['station_count'] / station_total


# # Bicicletas por ciudad
bikes_per_city = pd.DataFrame({'bikes_count' : station.groupby(['city'])['dock_count'].sum()}).reset_index()
bikes_per_city = bikes_per_city.sort_values(by='bikes_count', ascending=False)

total_bikes = bikes_per_city['bikes_count'].sum()
bikes_per_city['bikes_city_percentage'] = bikes_per_city['bikes_count'] / station_total

# # Bicicletas por estación
bikes_per_station = pd.DataFrame({'bikes_count' : station.groupby(['name'])['dock_count'].sum()}).reset_index()
bikes_per_station = bikes_per_station.sort_values(by='bikes_count', ascending=False)


# ## Analizando trip.csv

# In[24]:

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


# 
# Debido al alto número de trips con duraciones muy chicas, de pocos minutos, teorizamos que estos "trips" no son en verdad alquileres si no bicicletas retiradas para reparación o control. Asimismo podemos observar picos de "alquileres" en horas muy extrañas del día, que no por casualidad coinciden con los viajes de poca duración. Concluimos entonces que estos registros en el set de datos no corresponden a viajes reales.
# 
# Por lo tanto filtraremos los registros con duraciones menores a 5 minutos (300 segundos). A su vez, la misma página aclara que los viajes no puede durar más de 24hrs (86400 segundos) pues entonces se considera la bicicleta como 'robada', por lo que filtramos este tipo de viajes también.
# Teniendo en cuenta también este dato, reemplazamos las columnas start_date y end_date por una única date correspondiente al día de comienzo del viaje.
# 
# Los zip_codes no parecen brindar información clara. Son demasiados valores y no corresponden con los zip codes de las 5 ciudades de weather y station.
# 
# Finalmente, bike_id no nos brinda mayor información por sí solo. Sin otros datos sobre la bicicleta, como por ejemplo modelo, tracción, o tamaño, no sirve más que para ver las más usadas sin posibilitar algún analisis. Sería interesante analizar que características de la bicicleta importan más según condiciones climáticas, que modelos son los más usados.

trips = trips[(trips.duration >=300) & (trips.duration <= 86400)]
trips['date'] = trips.start_date
trips['trip_id'] = trips.id

trips = trips[['trip_id','duration','date', 'season',
               'start_station_name','start_station_id','start_time','start_hour', 'day_of_week',
               'end_time','end_hour','end_station_name','end_station_id', 'subscription_type']]

trips_total_count = trips['trip_id'].count()


# # Análisis por temporada

# ### Cantidad

trips_season = pd.DataFrame({'trip_count' : trips.groupby(['season'])['trip_id'].count()}).reset_index()

# # Duración y cantidad según día de la semana

# In[40]:

trips_dayofweek = pd.DataFrame({'trip_count' : trips.groupby(['day_of_week'])['trip_id'].count()})
trips_dayofweek.index = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

dayofweek_duration = pd.DataFrame({'duration_mean' : trips.groupby(['day_of_week'])['duration'].mean()})
dayofweek_duration.index = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

# # Duración por hora
trips_duration = pd.DataFrame({'duration_mean' : trips.groupby(['start_hour','end_hour'])['duration'].mean()}).reset_index()
trips_duration = trips_duration.sort_values(by='duration_mean', ascending=False)

duration = trips_duration.pivot("start_hour", "end_hour", "duration_mean")

trips_per_hour = pd.DataFrame({'TRIP_COUNT' : trips.groupby(['start_hour','end_hour'])['trip_id'].count()}).reset_index()
trips_per_hour = trips_per_hour.sort_values(by='TRIP_COUNT', ascending=False)

hours = trips_per_hour.pivot("start_hour", "end_hour", "TRIP_COUNT")

# # Análisis según subscripción
trip_subscription = pd.DataFrame({'trip_count' : trips.groupby(['subscription_type'])['trip_id'].count(),                                  'duration_mean': trips.groupby(['subscription_type'])['duration'].mean()}).reset_index()

# ### Cantidad 
#Cantidad según estación del año
subscription_count = pd.DataFrame({'trip_count' : trips.groupby(['subscription_type','season'])['trip_id'].count()}).reset_index()
subscription_count = subscription_count.sort_values(by='trip_count', ascending=False)

mapa = subscription_count.pivot("subscription_type", "season", "trip_count")

#Cantidad según día de la semana
subscription_count = pd.DataFrame({'trip_count' : trips.groupby(['subscription_type','day_of_week'])['trip_id'].count()}).reset_index()

mapa = subscription_count.pivot("subscription_type", "day_of_week", "trip_count")

# Cantidad según hora del día
subscriber  = trips[['start_hour','subscription_type']][trips['subscription_type'] == 'Subscriber'].groupby('start_hour').count() # subscriber
customer  = trips[['start_hour','subscription_type']][trips['subscription_type'] == 'Customer'].groupby('start_hour').count() # customer
subscriber.rename(columns={'subscription_type': 'Subscriber'}, inplace=True)
customer.rename(columns={'subscription_type': 'Customer'}, inplace=True)
subs_and_cust = pd.merge(subscriber, customer, right_index=True, left_index=True)

# ### Duración
plt.figure()
trips.loc[trips.subscription_type.str.contains('Subscriber'),['trip_id','duration','season']].groupby('season').mean().loc[:,'duration'].plot(rot=90,xticks=range(0,4), linewidth=2,figsize=(12,8),label='Subscriber');
trips.loc[trips.subscription_type.str.contains('Customer'), ['trip_id','duration','season']].groupby('season').mean().loc[:,'duration'].plot(rot=90,xticks=range(0,4), linewidth=2,label='Customer');
plt.legend();

# Media de duración según día por tipo de subscripción
plt.figure()
trips.loc[trips.subscription_type.str.contains('Subscriber'),                 ['trip_id','duration','day_of_week']].groupby('day_of_week').mean()                 .loc[:,'duration'].plot(rot=90,xticks=range(0,7),                  linewidth=2,figsize=(12,8),label='Subscriber');
trips.loc[trips.subscription_type.str.contains('Customer'),                 ['trip_id','duration','day_of_week']].groupby('day_of_week').mean()                 .loc[:,'duration'].plot(rot=90,xticks=range(0,7),                  linewidth=2,label='Customer');
plt.legend();

# Media de duración según hora por tipo de subscripción
plt.figure()
trips.loc[trips.subscription_type.str.contains('Subscriber'),                 ['trip_id','duration','start_hour']].groupby('start_hour').mean()                 .loc[:,'duration'].plot(rot=90,xticks=range(0,24),                  linewidth=2,figsize=(12,8),label='Subscriber');
trips.loc[trips.subscription_type.str.contains('Customer'),                 ['trip_id','duration','start_hour']].groupby('start_hour').mean()                 .loc[:,'duration'].plot(rot=90,xticks=range(0,24),                  linewidth=2,label='Customer');
plt.legend();

trips_with_stations = pd.merge(trips,station, how='inner',
                              left_on='start_station_id', right_on='station_id')


station_trip_count = pd.DataFrame({'TRIP_COUNT' : trips_with_stations.groupby(['name'])['name'].count()}).reset_index()
station_trip_count = station_trip_count.sort_values(by='TRIP_COUNT', ascending=False)

endstation_trip_count = pd.DataFrame({'TRIP_COUNT' : trips_with_stations.groupby(['end_station_name'])['trip_id'].count()}).reset_index()
endstation_trip_count = endstation_trip_count.sort_values(by='TRIP_COUNT', ascending=False)


# # Porcentaje de salida de viajes en cada estación
station_trip_count['station_trip_percentage'] = station_trip_count['TRIP_COUNT'] / trips_total_count

# # Cantidad de salidas y entradas por ciudad
city_trip_count = pd.DataFrame({'TRIP_COUNT' : trips_with_stations.groupby(['city'])['trip_id'].count()}).reset_index()
city_trip_count = city_trip_count.sort_values(by='TRIP_COUNT', ascending=False)
city_trip_count['city_trip_percentage'] = city_trip_count['TRIP_COUNT'] / trips_total_count

# # Viajes entre estaciones 

trips_start_end = pd.DataFrame({'TRIP_COUNT' : trips_with_stations.groupby(['start_station_name', 'end_station_name'])['trip_id'].count()}).reset_index()
trips_start_end = trips_start_end.sort_values(by='TRIP_COUNT', ascending=False)


# ## Duración entre las estaciones con mas viajes entre sí

#df.pivot(index='date', columns='variable', values='value')
top_stations_start = trips_start_end['start_station_name'].value_counts()[0:10].index.tolist()
bt_stations = trips_start_end[trips_start_end['start_station_name'].isin(top_stations_start)]
bt_stations = bt_stations.pivot("start_station_name", "end_station_name", "TRIP_COUNT")

#df.pivot(index='date', columns='variable', values='value')
top_stations_end = trips_start_end['end_station_name'].value_counts()[0:10].index.tolist()
bt_stations = trips_start_end[trips_start_end['end_station_name'].isin(top_stations_end)]
bt_stations = bt_stations.pivot("end_station_name", "start_station_name", "TRIP_COUNT")

# ## Merging trips con station, con weather

trips_with_stationweather = pd.merge(trips_with_stations, weather,
                                     on=['date','city'], how='inner')


# # Comparaciones de cantidad y duración de viajes según clima

# ## Según lluvia

weather_event_count = pd.DataFrame({'TRIP_COUNT' : trips_with_stationweather.groupby(['events'])['trip_id'].count()}).reset_index()
weather_event_count = weather_event_count.sort_values(by='TRIP_COUNT', ascending=False)
cant_clear = trips_with_stationweather


trips_with_stationweather.groupby('events').mean()['duration'];


trips_with_stationweather.groupby('precipitation_inches').mean()['duration'];

#df.pivot(index='date', columns='variable', values='value')
prec_and_vis = pd.DataFrame({'TRIP_COUNT' : trips_with_stationweather.groupby(['mean_visibility_miles', 'precipitation_inches'])['trip_id'].count()}).reset_index()
prec_and_vis = prec_and_vis.pivot('mean_visibility_miles', 'precipitation_inches', 'TRIP_COUNT')

# ## Según temperatura

trips_with_stationweather.plot.scatter('duration','max_temperature_f', alpha=0.25,figsize=(10,6));
plt.xlim(0,100000);


trips_with_stationweather.plot.scatter('duration','min_temperature_f',alpha=0.25,figsize=(10,6));
plt.xlim(0,100000);


# Los gráficos nos permiten ver que la temperatura mínima no suele influir en la duración de los viajes, mas las mayores duraciones se concentran alrededor de los 75°F (24 °C) o 60°F (15°C) de temperatura máxima. Se puede observar también una pendiente pronunciada cuando la temperatura se acerca a los 90°F (32°C), lo cual nos puede parecer raro porque no es tan alta, pero lo más probable es que la temperatura suela subir tanto en estas ciudades. Como vemos, de hecho, la temperatura máxima a penas supera los 100°F (37°C).

# ## Según visibilidad

trips_with_stationweather.plot.scatter('duration','mean_visibility_miles', alpha=0.25,figsize=(10,6));
plt.xlim(0,100000);
plt.ylim(0,21);


# En este gráfico podemos ver claramente la diferencia entre los días despejados (por defecto un día normal tiene visibilidad de 10 millas) y los días de visibilidad reducida causada probablemente por niebla. Estos datos corresponden con lo que uno supondría que pasa, a menor visibilidad, menor duración de viajes. Mas cabe mencionar que visibilidad mayor de 10 millas es un suceso extraño, como dijimos un día despejado normal le corresponden 10 millas no más. Además no se observa ninguna pendiente de correlación. Es posible esos datos sean erróneos.

# ## Según el viento

trips_with_stationweather.plot.scatter('duration','mean_wind_speed_mph',alpha=0.25,figsize=(10,6));
plt.xlim(0,100000);
plt.ylim(0,25);


# ## Segun nubosidad

trips_with_stationweather.plot.scatter('duration','cloud_cover',alpha=0.25,figsize=(10,6));
plt.xlim(0,100000);