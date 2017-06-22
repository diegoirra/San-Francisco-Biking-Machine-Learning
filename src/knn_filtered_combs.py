from sklearn.neighbors import  KNeighborsRegressor
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = KNeighborsRegressor(n_neighbors=3, algorithm='kd_tree')
model_name = 'K_neighbors_regressor_filtered_comb8'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=8)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=8)
    print 'Output generated.'
else:
    print 'No output generated'