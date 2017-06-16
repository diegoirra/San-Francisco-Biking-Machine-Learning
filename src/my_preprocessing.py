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
    train['mean_temperature_f'] = pd.qcut(train['mean_temperature_f'], 5)
    train['mean_dew_point_f'] = pd.qcut(train['mean_dew_point_f'], 4)
    train['mean_humidity'] = pd.qcut(train['mean_humidity'], 4)
    train['mean_sea_level_pressure_inches'] = pd.qcut(train['mean_sea_level_pressure_inches'], 4)
    train['mean_wind_speed_mph'] = pd.qcut(train['mean_wind_speed_mph'], 4)
    train['max_gust_speed_mph'] = pd.qcut(train['max_gust_speed_mph'], 6)
    train['wind_dir_degrees'] = pd.qcut(train['wind_dir_degrees'], 6)
    '''CHEAQUEAR ESTO'''
    train['mean_visibility_miles'] = train['mean_visibility_miles'].astype(float) 
    train['mean_visibility_miles'] = pct_rank_qcut(train.mean_visibility_miles, 5)
    
    train_filtered['mean_temperature_f'] = pd.qcut(train_filtered['mean_temperature_f'], 5)
    train_filtered['mean_dew_point_f'] = pd.qcut(train_filtered['mean_dew_point_f'], 4)
    train_filtered['mean_humidity'] = pd.qcut(train_filtered['mean_humidity'], 4)
    train_filtered['mean_sea_level_pressure_inches'] = pd.qcut(train_filtered['mean_sea_level_pressure_inches'], 4)
    train_filtered['mean_wind_speed_mph'] = pd.qcut(train_filtered['mean_wind_speed_mph'], 4)
    train_filtered['max_gust_speed_mph'] = pd.qcut(train_filtered['max_gust_speed_mph'], 6)
    train_filtered['wind_dir_degrees'] = pd.qcut(train_filtered['wind_dir_degrees'], 6)
    '''CHEAQUEAR ESTO'''
    train_filtered['mean_visibility_miles'] = train_filtered['mean_visibility_miles'].astype(float)
    train_filtered['mean_visibility_miles'] = pct_rank_qcut(train_filtered.mean_visibility_miles, 5)

    test['mean_temperature_f'] = pd.qcut(test['mean_temperature_f'], 5)
    test['mean_dew_point_f'] = pd.qcut(test['mean_dew_point_f'], 4)
    test['mean_humidity'] = pd.qcut(test['mean_humidity'], 4)
    test['mean_sea_level_pressure_inches'] = pd.qcut(test['mean_sea_level_pressure_inches'], 4)
    test['mean_wind_speed_mph'] = pd.qcut(test['mean_wind_speed_mph'], 4)
    test['max_gust_speed_mph'] = pd.qcut(test['max_gust_speed_mph'], 6)
    test['wind_dir_degrees'] = pd.qcut(test['wind_dir_degrees'], 6)
    '''CHEAQUEAR ESTO'''
    test['mean_visibility_miles'] = test['mean_visibility_miles'].astype(float)
    test['mean_visibility_miles'] = pct_rank_qcut(test.mean_visibility_miles, 5)

'''FALTAN LOS FEATURES'''
def encode_features(df_train, df_test):
    features = ['season', 'subscription_type', 'mean_temperature_f', 'mean_dew_point_f',  'mean_humidity', 'mean_sea_level_pressure_inches', 
                            'mean_visibility_miles', 'mean_wind_speed', 'max_gust_speed', 'precipitation_inches', 'events',  'wind_dir_degrees']
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