from sklearn.linear_model import SGDRegressor
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = SGDRegressor()
model_name = 'stochastic_gradient_descend_filtered_comb7'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=7)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=7)
    print 'Output generated.'
else:
    print 'No output generated'