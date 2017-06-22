from sklearn.linear_model import Lars
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = Lars()
model_name = 'lars_filtered_comb5'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=5)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=5)
    print 'Output generated.'
else:
    print 'No output generated'