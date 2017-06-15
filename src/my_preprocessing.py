#encoding: utf-8

from sklearn import preprocessing
import pandas as pd
import os
os.chdir('..')


def initialize_df():
    train = pd.read_csv('data/trips_train_with_stationweather.csv', low_memory=False)
    train_filtered = pd.read_csv('data/trips_train_with_station_filtered.csv', low_memory=False)
    test = pd.read_csv('data/trips_test_with_stationweather.csv', low_memory=False)
    return train, train_filtered, test

def discretizar(df):
    pass

'''FALTAN LOS FEATURES'''
def encode_features(df_train, df_test):
    features = []
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