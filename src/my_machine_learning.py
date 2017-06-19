import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from run_kfold import run_kfold
import os

def train_model(model, model_name, filtered=False, reduction=0):
    
    print "Reading dataset..."       
    if filtered:
        train = pd.read_csv('data/trips_train_final_filtered.csv', low_memory=False)
    else:
        train = pd.read_csv('data/trips_train_final.csv', low_memory=False)    
    print "Dataset read"
    
    if reduction:
        train = reducir_df(train, reduction)   
    X_all = train.drop("duration", axis=1)
    y_all = train['duration']
    
    num_test = 0.20
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=num_test, random_state=23)
    
    path_joblib = 'trained_models_joblibbed/'+ model_name+ '.pkl'
    if os.path.exists(path_joblib):        
        model = joblib.load(path_joblib)
        print "Joblibbed model loaded" 
    else:
        print "Fitting model..."
        print model.fit(X_train, y_train)
        print "Model fit. Joblibbing model..."
        os.chdir('trained_models_joblibbed')
        joblib.dump(model, model_name+'.pkl')
        os.chdir('..')
        
    print 'Train CheckScore (%):'
    run_kfold(model, X_all, y_all)
    return model, X_test, y_test

def make_prediction(model, model_name, reduction=0):
    
    print "Reading test dataset..."
    test = pd.read_csv('data/trips_test_final.csv', low_memory=False)
    ids = test['trip_id']
    X_test = test.drop('trip_id', axis=1)
    if reduction:
        X_test = reducir_df(X_test, reduction, test=1)
    print "Test dataset read. Predicting test..."
    
    predictions = model.predict(X_test)
    
    output = pd.DataFrame({ 'id' : ids, 'duration': predictions })
    os.chdir('predictions')
    print "Generating output..."
    output[['id','duration']].to_csv(model_name+'.csv',index=False)
    os.chdir('..')

def reducir_df(df, reduction_num, test=0):
    #reduction_num no puede ser 0
    print
    print ("Reduciendo dataset features comb{0}:".format(reduction_num))    
    combos_list =[['start_hour', 'day_of_week'], #comb1
                  ['start_hour', 'day_of_week', 'subscription_type'], #comb2
                  ['start_hour', 'day_of_week', 'subscription_type', 'season'], #comb3
                  ['day_of_week', 'season'], #comb4
                  ['day_of_week', 'season', 'subscription_type'], #comb5
                  ['start_hour','day_of_week','subscription_type','season','start_station_id'], #comb6
                  ['start_hour','day_of_week','subscription_type','season',
                   'start_station_id', 'end_station_id'], #comb7
                  ['start_hour', 'day_of_week', 'subscription_type','season',
                   'events', 'mean_temperature_f']] #comb8
    
    if not test:
        reduced = ['duration'] + combos_list[reduction_num-1]
    else:
        reduced = combos_list[reduction_num-1]
    print reduced
    print
    return df[reduced]
    
