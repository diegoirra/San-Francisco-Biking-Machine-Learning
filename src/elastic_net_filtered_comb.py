from sklearn.linear_model import ElasticNet
from my_machine_learning import train_model, make_prediction
import os
os.chdir('..')

model = ElasticNet()
model_name = 'elastic_net_filtered_comb1'

print "EXECUTING: "+ model_name
model, X_test, y_test = train_model(model, model_name, filtered=True, reduction=1)

if raw_input('Training done. Make prediction? [y/n]: ') == 'y':
    make_prediction(model, model_name, reduction=1)
    print 'Output generated.'
else:
    print 'No output generated'