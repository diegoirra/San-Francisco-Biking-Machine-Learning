from sklearn.linear_model import Perceptron
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = Perceptron()
model_name = 'perceptron'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=False)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name)
    print 'Output generated.'
else:
    print 'No output generated'