import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from run_kfold import run_kfold
import os

def train_model(model, model_name, filtered=False):
    
    print "EXECUTING: "+ model_name
    print "Reading dataset..."       
    if filtered:
        train = pd.read_csv('data/trips_train_final_filtered.csv', low_memory=False)
    else:
        train = pd.read_csv('data/trips_train_final.csv', low_memory=False)     
       
    X_all = train.drop("duration", axis=1)
    y_all = train['duration']
    print "Dataset read"
    
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
    
    print
    print 'Train CheckScore (%):'
    print (model.score( X_train , y_train)*100)
    print (model.score( X_test , y_test  )*100)
    run_kfold(model, X_all, y_all)
    return model, X_test, y_test

def make_prediction(model, model_name):
    
    print "Reading test dataset..."
    test = pd.read_csv('data/trips_test_final.csv', low_memory=False)
    ids = test['trip_id']
    X_test = test.drop('trip_id', axis=1)
    print "Test dataset read. Predicting test..."
    
    predictions = model.predict(X_test)
    
    output = pd.DataFrame({ 'id' : ids, 'duration': predictions })
    os.chdir('predictions')
    print "Generating output..."
    output[['id','duration']].to_csv(model_name+'.csv',index=False)
    os.chdir('..')
    