# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 00:01:53 2018

Tractor Supply Co Predictive Model Generation

@author: Kyle Jiang
"""

# Tensorflow library and Keras API
import tensorflow as tf
#from tensorflow.contrib.session_bundle import exporter
from tensorflow import keras
#from keras import backend as K
#from keras.models import model_from_config

# Helper libraries
import flask
import numpy as np
import pandas
import random
#import os

sess = tf.Session()     # start a Tensorflow session
npa = lambda x: np.array(x)     # create Numpy array from selection
tot = lambda x: tf.convert_to_tensor(x)     # create tensor from selection
bts = lambda x: tf.saved_model.utils.build_tensor_info(x)       #build tensor info from selection

ff = 3      # frequency of farming pattern shift
datafile = "VandyHack/TSC Seasonal Sales/TSC_Sales_Seasonal.csv"    # data file
trnrt = 0.1     # ratio of training data to total data
mvers = 1       # file version

print("Tensorflow imported successfully.\nVersion: " + tf.__version__)

# contains the state abbreviations for indexing
stabv = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", 
    "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", 
    "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
    "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

# create vector of class names
# generate label and predictor Numpy arrays
print("Generating predictor and label vectors...")
df = pandas.read_csv(datafile)
nents = df.shape[0]
class_names = df.CATEGORY.unique().tolist()
labels = npa([class_names.index(c) for c in df.CATEGORY.values])
states = npa([stabv.index(s[: 2]) for s in df.STATE.values])
odates = npa([ff * int(ds.split('/')[0]) + int(ds.split('/')[1]) // (30 // ff + 1) for ds in df.ORDERDATE.values])
###weather = npa(df.WEATHER.values)

# randomize and define training and test datasets
print("Dividing datasets with a " + str(trnrt) + " training ratio...")
mark = int(trnrt * nents)
z = list(zip(labels, states, odates))
random.shuffle(z)
(labels, states, odates) = zip(*z)
(labels, states, odates) = npa((labels, states, odates))
(tr_labels, ts_labels) = (npa(labels[: mark]), npa(labels[mark: ]))
(tr_states, ts_states) = (npa(states[: mark]), npa(states[mark: ]))
(tr_odates, ts_odates) = (npa(odates[: mark]), npa(odates[mark: ]))
###(tr_weather, ts_weather) = (npa(weather[: mark]), npa(weather[mark: ]))

# specify Keras model
print("Setting up Keras model...")
model = keras.Sequential([
    keras.layers.Dense(20, activation = tf.nn.relu, input_dim = 2),
    keras.layers.Dense(32, activation = tf.nn.relu),
    keras.layers.Dense(len(class_names), activation = tf.nn.softmax)
])

# compile the model using an Adam optimizer
print("Compiling model...")
model.compile(loss = "categorical_crossentropy", 
#    optimizer = keras.optimizers.SGD(lr = 0.01, decay = 1E-6, momentum = 0.9, nesterov = True),
#    optimizer = tf.train.AdamOptimizer(),
    optimizer = keras.optimizers.Adam(),
    metrics = ["accuracy"]
)

# train the model
print("Training model on designated data...")
model.fit(npa([tr_states, tr_odates]).T, keras.utils.to_categorical(tr_labels), epochs = 5)

# finally, test the model...
print("Testing model...")
(ts_loss, ts_acc) = model.evaluate(npa([ts_states, ts_odates]).T, keras.utils.to_categorical(ts_labels))
print("Test accuracy: " + str(ts_acc))


#-------------------------------------------------------------------------------------------------------------------------#

# ...then export and save the model
#print("Exporting the protobuf graph of model...")
#exp_path = os.path.join(os.getcwd(), str(mvers))


#tf.saved_model.simple_save(sess, exp_path, inputs = {"inputs": tot(model.input)}, outputs = {"logits": tot(model.output)})


#K.set_learning_phase(0)  # all new operations will be in test mode from now on

# serialize the model and get its weights, for quick re-building
#config = model.get_config()
#weights = model.get_weights()

# re-build a model where the learning phase is now hard-coded to 0
#new_model = model_from_config(config)
#new_model.set_weights(weights)

#saver = tf.train.Saver(sharded = True)
#model_exporter = exporter.Exporter(saver)
#signature = exporter.classification_signature(input_tensor = model.input, 
#    scores_tensor = model.output)
#model_exporter.init(sess.graph.as_graph_def(), 
#    default_graph_signature = signature)
#model_exporter.export(exp_path, tf.constant(mvers), sess)


# instantiate flask 
app = flask.Flask(__name__)

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = {"success": False}

    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # if parameters are found, return a prediction
    if (params != None):
        s_ = stabv.index(str(params['s']))
        m_ = int(params['m'])
        d_ = int(params['d'])
        doy_ = ff * m_ + d_ // (30 // ff + 1)
###        w_ = int(params['w'])
        logits = model.predict(npa([[s_, doy_]])).tolist()[0]
        data["success"] = True
        idx = np.argsort(logits).tolist()
        data["topbuys"] = [class_names[idx[len(logits) - i - 1]] for i in range(len(logits))]
        data["probs"] = [logits[idx[len(logits) - i - 1]] for i in range(len(logits))]

    # return a response in json format
    return flask.jsonify(data)

# start the flask app, allow remote connections 
print("Starting web server...")
app.run(host = '127.0.0.1')