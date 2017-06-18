from sklearn.linear_model import OrthogonalMatchingPursuit
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = OrthogonalMatchingPursuit()
model_name = 'orthogonal_matching_pursuit_filtered'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name)
    print 'Output generated.'
else:
    print 'No output generated'