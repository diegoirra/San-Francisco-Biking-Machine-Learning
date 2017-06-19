from sklearn.neural_network import MLPRegressor
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = MLPRegressor()
model_name = 'mlp_filtered_comb8'

model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=8)

if raw_input('Training done. Make prediction? [y/n]') == 'y':
    make_prediction(model, model_name, reduction=8)
    print 'Output generated.'
else:
    print 'No output generated'