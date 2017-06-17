import pandas as pd
import os
os.chdir('..')


def initialize_df():
    train = pd.read_csv('data/trips_train_final.csv', low_memory=False)
    train_filtered = pd.read_csv('data/trips_train_final_filtered.csv', low_memory=False)
    X_test = pd.read_csv('data/trips_test_final.csv', low_memory=False)
    
    X_all = train.drop("duration", axis=1)
    X_all_filtered = train_filtered.drop("duration", axis=1)
    y_all = train['duration']
    
    return X_all, X_all_filtered, X_test, y_all
