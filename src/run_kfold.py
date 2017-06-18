from sklearn.cross_validation import KFold
from sklearn.metrics import explained_variance_score
#from sklearn.metrics import explained_variance_score
#from sklearn.metrics import mean_absolute_error
#from sklearn.metrics import mean_squared_error
#from sklearn.metrics import median_absolute_error
#from sklearn.metrics import r2_score
import numpy as np

def run_kfold(classifier, X_all, y_all):
    
    kf = KFold(X_all.shape[0], n_folds=10)
    outcomes = []
    fold = 0
    print
    print "Evaluating kfolds..."
    print "KFold Score (%):"
    for train_index, test_index in kf:       
        fold += 1
        X_train, X_test = X_all.values[train_index], X_all.values[test_index]
        y_train, y_test = y_all.values[train_index], y_all.values[test_index]
        classifier.fit(X_train, y_train)        
        predictions = classifier.predict(X_test)
        accuracy = explained_variance_score(y_test, predictions)
        #accuracy = classifier.score(X_test, y_test)
        outcomes.append(accuracy)
        mean = np.mean(outcomes)
        print("Fold {0} accuracy: {1}".format(fold, accuracy*100))
    
    print
    print("Mean accuracy: {0}".format(mean*100))
    print "---------------------------------------------------"
    