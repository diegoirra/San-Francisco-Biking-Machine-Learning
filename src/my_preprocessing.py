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
    group_names = ['one', 'two', 'three', 'four', 'five']
    
    df['mean_temperature_f'].fillna(df['mean_temperature_f'].dropna().median(), inplace=True)
    df['mean_temperature_f'] = pd.cut(df['mean_temperature_f'], 5, labels=group_names)
    
    group_names = ['one', 'two', 'three', 'four']
    
    df['mean_dew_point_f'].fillna(df['mean_dew_point_f'].dropna().median(), inplace=True)
    df['mean_dew_point_f'] = pd.cut(df['mean_dew_point_f'], 4, labels=group_names)
    
    df['mean_humidity'].fillna(df['mean_humidity'].dropna().median(), inplace=True)
    df['mean_humidity'] = pd.cut(df['mean_humidity'], 4, labels=group_names)
    
    df['mean_sea_level_pressure_inches'].fillna(df['mean_sea_level_pressure_inches'].dropna().median(), inplace=True)
    df['mean_sea_level_pressure_inches'] = pd.cut(df['mean_sea_level_pressure_inches'], 4, labels=group_names)
    
    df['mean_wind_speed_mph'].fillna(df['mean_wind_speed_mph'].dropna().median(), inplace=True)
    df['mean_wind_speed_mph'] = pd.cut(df['mean_wind_speed_mph'], 4, labels=group_names)

    group_names = ['one', 'two', 'three', 'four', 'five', 'six']
    
    df['max_gust_speed_mph'].fillna(df['max_gust_speed_mph'].dropna().median(), inplace=True)
    df['max_gust_speed_mph'] = pd.cut(df['max_gust_speed_mph'], 6, labels=group_names)

    df['wind_dir_degrees'].fillna(df['wind_dir_degrees'].dropna().median(), inplace=True)
    df['wind_dir_degrees'] = pd.cut(df['wind_dir_degrees'], 6, labels=group_names)
    
    df['mean_visibility_miles'].fillna(df['mean_visibility_miles'].dropna().median(), inplace=True)
    df['mean_visibility_miles'] = df['mean_visibility_miles'].astype(float) 
    df['mean_visibility_miles'] = pct_rank_qcut(df.mean_visibility_miles, 5)
    return df
    

def encode_features(dataset):

    dataset['season'] = dataset['season'].map( {'summer': 0, 'autumn': 1, 'winter':2, 'spring':3} ).astype(int)
    dataset['subscription_type'] = dataset['subscription_type'].map( {'Subscriber': 0, 'Customer': 1} ).astype(int)
    dataset['events'] = dataset['events'].map( {'Clear': 0, 'Fog': 1, 'Fog-Rain': 2, 'Rain': 3, 'Rain-Thunderstorm': 4} ).astype(int)
    dataset['mean_temperature_f'] = dataset['mean_temperature_f'].map( {'one': 0, 'two': 1, 'three': 2, 'four': 3, 'five': 4} ).astype(int)

    features_with_4 = ['mean_dew_point_f',  'mean_humidity', 'mean_sea_level_pressure_inches', 'mean_wind_speed_mph']
    features_with_6 = ['max_gust_speed_mph','wind_dir_degrees']
    
    for feature in features_with_4:        
        dataset[feature] = dataset[feature].map( {'one': 0, 'two': 1, 'three': 2, 'four': 3} ).astype(int)

    for feature in features_with_6:        
        dataset[feature] = dataset[feature].map( {'one': 0, 'two': 1, 'three': 2, 'four': 3, 'five': 4, 'six': 5} ).astype(int)

    le = preprocessing.LabelEncoder()
    le = le.fit(dataset['precipitation_inches'])
    dataset['precipitation_inches'] = le.transform(dataset['precipitation_inches'])
    return dataset


train, train_filtered, test = initialize_df()

train = discretizar(train)
train_filtered = discretizar(train_filtered)
test = discretizar(test)

train_encoded = encode_features(train)
train_encoded_filtered = encode_features(train_filtered)
test_encoded = encode_features(test)

train_encoded.to_csv('data/trips_train_final.csv', index=False)
train_encoded_filtered.to_csv('data/trips_train_final_filtered.csv', index=False)
test_encoded.to_csv('data/trips_test_final.csv', index=False)



