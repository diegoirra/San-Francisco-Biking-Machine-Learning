from sklearn.linear_model import ARDRegression
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = ARDRegression()
model_name = 'ard_filtered_comb'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=0)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=0)
    print 'Output generated.'
else:
    print 'No output generated'