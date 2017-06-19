from sklearn.tree import DecisionTreeRegressor
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = DecisionTreeRegressor()
model_name = 'decision_tree_filtered_comb2'

model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=2)

if raw_input('Training done. Make prediction? [y/n]') == 'y':
    make_prediction(model, model_name, reduction=2)
    print 'Output generated.'
else:
    print 'No output generated'