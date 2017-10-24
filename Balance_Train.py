#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 21:30:00 2017

@author: changlongjiang
"""
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

df_NotLFT = pd.read_table('NotLFT.txt',sep=',')
df = pd.read_table('data_test.txt',sep=',')
X = np.array(df.drop(['LFT'],1))
y = np.array(df['LFT'])
X = X[:900]
y=y[:900]
X_NotLFT = np.array(df_NotLFT.drop(['LFT'],1))
y_NotLFT = np.array(df_NotLFT['LFT'])
X_NotLFT=preprocessing.scale(X_NotLFT)
X=np.concatenate((X, X_NotLFT), axis=0)
y=np.concatenate((y, y_NotLFT), axis=0)

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