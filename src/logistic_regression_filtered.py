from sklearn.linear_model import LogisticRegression
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

logreg = LogisticRegression()
model_name = 'logistic_regression_filtered'

logreg, X_test, y_test = train_model(logreg, model_name, filtered=True)

if raw_input('Training done. Make prediction? [y/n]') == 'y':
    make_prediction(logreg, model_name)
    print 'Output generated.'
else:
    print 'No output generated'