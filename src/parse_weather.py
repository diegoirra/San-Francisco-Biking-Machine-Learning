#encoding: utf-8
# # Organizaci�n de datos
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


weather = pd.read_csv('data\weather.csv', parse_dates=['date'], infer_datetime_format=True, low_memory=False)

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

weather.to_csv('data/parsed_weather.csv', index=False)