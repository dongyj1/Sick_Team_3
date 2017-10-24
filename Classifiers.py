#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:58:16 2017

@author: changlongjiang
"""
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

df = pd.read_table('data_test.txt',sep=',')
X = np.array(df.drop(['LFT','MultiRead','TooBig','ValidDim'],1))
y = np.array(df['LFT'])
#X[:,0]=X[:,0].astype(int)
#X[174][0]=40
X=preprocessing.scale(X)
print(len(X),len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""
Linear Regeression
"""
clf_linear = linear_model.LinearRegression()
clf_linear.fit(X_train, y_train)
accuracy = clf_linear.score(X_test, y_test)
#print('Linear Regression Score: ', accuracy)
"""
Ligistic Regression
"""
clf_ligistic = linear_model.LogisticRegression(C=1e5)
clf_ligistic.fit(X_train, y_train)
accuracy = clf_ligistic.score(X_test, y_test)
print('Ligistic Regression Score: ', accuracy)
"""
Random Forest
"""
clf_RF = RandomForestClassifier(n_jobs=2, random_state=0)
clf_RF.fit(X_train, y_train)
accuracy = clf_RF.score(X_test, y_test)
print('Random Forest Score', accuracy)
print('This is the importances of different features: ',clf_RF.feature_importances_)

"""
SVM
"""
clf_SVM = svm.SVC()
clf_SVM.fit(X_train, y_train)
accuracy = clf_SVM.score(X_test, y_test)
print('SVM Score: ', accuracy)
"""
AdaBoost
"""
clf_AB = AdaBoostClassifier()
clf_AB.fit(X_train, y_train)
accuracy = clf_AB.score(X_test, y_test)
print('AdaBoost Score: ', accuracy)
"""
MLP
"""
clf_MLP = MLPClassifier(alpha=1e-5, hidden_layer_sizes=(10, 5, 3), random_state=1)
clf_MLP.fit(X_train, y_train)
accuracy = clf_MLP.score(X_test, y_test)
print('MLP Score: ', accuracy)