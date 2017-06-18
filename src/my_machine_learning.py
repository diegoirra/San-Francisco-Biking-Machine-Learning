import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import os.path

def train_model(model, model_name, filtered=False):
    
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
        model.fit(X_train, y_train)
        print "Model fit. Joblibbing model..."
        joblib.dump(model, path_joblib)  
    
    print
    print 'Score:'
    print (model.score( X_train , y_train)*100 +'%')
    print (model.score( X_test , y_test  )*100 +'%')
    return model, X_test, y_test

def make_prediction(model, model_name):
    
    print "Reading test dataset..."
    test = pd.read_csv('data/trips_test_final.csv', low_memory=False)
    ids = test['trip_id']
    X_test = test.drop('trip_id', axis=1)
    print "Test dataset read. Predicting test..."
    
    predictions = model.predict(X_test)
    
    output = pd.DataFrame({ 'trip_id' : ids, 'duration': predictions })
    path = 'predictions/'+ model_name + '.csv'
    print "Generating output..."
    output.to_csv(path,index=False)
    