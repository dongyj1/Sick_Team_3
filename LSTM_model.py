#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:43:10 2017

@author: changlongjiang
"""


import numpy as np
from matplotlib import pyplot
import pandas as pd
import os
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras.backend as K

def matthews_correlation(y_true, y_pred):
    """Matthews correlation metric.
    +# Aliases
  
    It is only computed as a batch-wise average, not globally.

    Computes the Matthews correlation coefficient measure for quality
    of binary classification problems.
    """
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos

    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos

    tp = K.sum(y_pos * y_pred_pos)
    tn = K.sum(y_neg * y_pred_neg)

    fp = K.sum(y_neg * y_pred_pos)
    fn = K.sum(y_pos * y_pred_neg)

    numerator = (tp * tn - fp * fn)
    denominator = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    return numerator / (denominator + K.epsilon())


def precision(y_true, y_pred):
    """Precision metric.

    Only computes a batch-wise average of precision.

     Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    """Recall metric.

    Only computes a batch-wise average of recall.

    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fbeta_score(y_true, y_pred, beta=1):
    """Computes the F score.

    The F score is the weighted harmonic mean of precision and recall.
    Here it is only computed as a batch-wise average, not globally.

    This is useful for multi-label classification, where input samples can be
    classified as sets of labels. By only using accuracy (precision) a model
    would achieve a perfect score by simply assigning every class to every
    input. In order to avoid this, a metric should penalize incorrect class
    assignments as well (recall). The F-beta score (ranged from 0.0 to 1.0)
    computes this, as a weighted mean of the proportion of correct class
    assignments vs. the proportion of incorrect class assignments.

    With beta = 1, this is equivalent to a F-measure. With beta < 1, assigning
    correct classes becomes more important, and with beta > 1 the metric is
    instead weighted towards penalizing incorrect class assignments.
    """
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score


def fmeasure(y_true, y_pred):
    """Computes the f-measure, the harmonic mean of precision and recall.

    Here it is only computed as a batch-wise average, not globally.
    """
    return fbeta_score(y_true, y_pred, beta=1)

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

path = "./processed" #文件夹目录  
files= os.listdir(path)
files = files[1:]
s=[]
for i in files:
    k = read_csv('./processed/'+i, header=0, index_col=0)
    s.append(k)
dataset = pd.concat(s)

#dataset = read_csv('7_4.csv', header=0, index_col=0)

values = dataset.values
dataset.head()

values = values.astype('float32')


#Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

n_in = 10
n_out = 1
reframed = series_to_supervised(scaled, n_in, n_out)


reframed.head()
reframed.drop(reframed.columns[[-5, -2,-1]], axis=1, inplace=True) #drop some column I don't want to include
print(reframed.head())


#split train and test
values = reframed.values
#X = np.concatenate((values[:,:29],values[:,30:]),axis=1)
#y = values[:,29]
#train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.05)
n_train_hours = -50000
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

# split into input and outputs
input_col_index = -4
X = np.concatenate((train[:,:input_col_index], train[:,input_col_index+1:]), axis=1)
train_X = np.concatenate((train[:,:input_col_index], train[:,input_col_index+1:]), axis=1)
train_y = train[:, input_col_index]
test_X = np.concatenate((test[:,:input_col_index], test[:,input_col_index+1:]), axis=1)
test_y = test[:, input_col_index]

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
 
# design network
neurons = 10
epochs_number = 40
b_number = 32
model = Sequential()
model.add(LSTM(neurons, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='binary_crossentropy', optimizer='adam',metrics=[precision, recall, fmeasure])

# fit network
history = model.fit(train_X, train_y, epochs=epochs_number, batch_size=b_number, validation_data=(test_X, test_y), verbose=2, shuffle=False)

# plot history
image_name = str(n_in)+'days_'+str(neurons)+'n_'+str(b_number)+'b_'+str(epochs_number)+'e_'+'.png'
pyplot.plot(history.history['loss'], label='train_loss')
pyplot.plot(history.history['val_loss'], label='test_loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend()
pyplot.savefig('./images/loss_' + image_name)
pyplot.show()
pyplot.plot(history.history['fmeasure'], label='train_f1')
pyplot.plot(history.history['val_fmeasure'], label='test_f1')
pyplot.ylabel('f1 score')
pyplot.xlabel('epoch')
pyplot.legend()
pyplot.savefig('./images/f1_' + image_name)
pyplot.show()

pyplot.plot(history.history['precision'], label='train_p')
pyplot.plot(history.history['val_precision'], label='test_p')
pyplot.plot(history.history['recall'], label='train_r')
pyplot.plot(history.history['val_recall'], label='test_r')
pyplot.ylabel('percentage')
pyplot.xlabel('epoch')
pyplot.legend()
pyplot.savefig('./images/pr_' + image_name)
pyplot.show()


