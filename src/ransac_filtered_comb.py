from sklearn.linear_model import RANSACRegressor
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = RANSACRegressor()
model_name = 'ransac_filtered_comb3'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=3)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=3)
    print 'Output generated.'
else:
    print 'No output generated'