from sklearn.linear_model import Ridge
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = Ridge()
model_name = 'ridge_filtered'

model, X_test, y_test = train_model(model, model_name, filtered=True)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name)
    print 'Output generated.'
else:
    print 'No output generated'