#encoding: utf-8

from sklearn import preprocessing
import pandas as pd
import os
os.chdir('..')


def initialize_df():
    train = pd.read_csv('data/trips_train_with_stationweather.csv', low_memory=False)
    train_filtered = pd.read_csv('data/trips_train_with_stationweather_filtered.csv', low_memory=False)
    test = pd.read_csv('data/trips_test_with_stationweather.csv', low_memory=False)
    return train, train_filtered, test

def pct_rank_qcut(series, n):
    edges = pd.Series([float(i) / n for i in range(n + 1)])
    f = lambda x: (edges >= x).argmax()
    return series.rank(pct=1).apply(f)

def discretizar(df):
    group_names = ['1', '2', '3', '4', '5']
    df['mean_temperature_f'] = pd.qcut(df['mean_temperature_f'], 5, labels=group_names)
    group_names = ['1', '2', '3', '4']
    df['mean_dew_point_f'] = pd.qcut(train['mean_dew_point_f'], 4, labels=group_names)
    df['mean_humidity'] = pd.qcut(df['mean_humidity'], 4, labels=group_names)
    df['mean_sea_level_pressure_inches'] = pd.qcut(df['mean_sea_level_pressure_inches'], 4, labels=group_names)
    df['mean_wind_speed_mph'] = pd.qcut(df['mean_wind_speed_mph'], 4, labels=group_names)
    group_names = ['1', '2', '3', '4', '5', '6']
    df['max_gust_speed_mph'] = pd.qcut(df['max_gust_speed_mph'], 6, labels=group_names)
    df['wind_dir_degrees'] = pd.qcut(df['wind_dir_degrees'], 6, labels=group_names)
    '''CHEAQUEAR ESTO'''
    df['mean_visibility_miles'] = df['mean_visibility_miles'].astype(float) 
    df['mean_visibility_miles'] = pct_rank_qcut(df.mean_visibility_miles, 5)
    
'''FALTAN LOS FEATURES'''
def encode_features(df_train, df_test):
    features = ['season', 'subscription_type', 'mean_temperature_f', 'mean_dew_point_f',  'mean_humidity', 'mean_sea_level_pressure_inches', 'mean_visibility_miles', 'mean_wind_speed_mph', 'max_gust_speed_mph', 'precipitation_inches', 'events',  'wind_dir_degrees']

    df_combined = pd.concat([df_train[features], df_test[features]])
    
    for feature in features:
        le = preprocessing.LabelEncoder()
        le = le.fit(df_combined[feature])
        df_train[feature] = le.transform(df_train[feature])
        df_test[feature] = le.transform(df_test[feature])
    return df_train, df_test


train, train_filtered, test = initialize_df()

discretizar(train)
discretizar(train_filtered)
discretizar(test)

train_encoded, test2 = encode_features(train, test)
train_encoded_filtered, test_encoded = encode_features(train_filtered, test)
    

train_encoded.to_csv('data/trips_train_final.csv', index=False)
train_encoded_filtered.to_csv('data/trips_train_final_filtered', index=False)
test_encoded.to_csv('data/trips_test_final.csv', index=False)