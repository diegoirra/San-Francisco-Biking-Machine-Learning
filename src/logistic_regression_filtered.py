from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

logreg = LogisticRegression()
model_name = 'logistic_regression_filtered'

logreg, X_test, y_test = train_model(logreg, model_name, filtered=True)
'''Revisar evaluacion, also in my_machine_learning.py'''
print '----------------------------'
predictions = logreg.predict(X_test)
print (accuracy_score(y_test, predictions))
print

if raw_input('Training done. Make prediction? [y/n]') == 'y':
    make_prediction(logreg, model_name)
    print 'Output generated.'
else:
    print 'No output generated'