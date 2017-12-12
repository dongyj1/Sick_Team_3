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
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

df = pd.read_csv('./processed/7_4.csv',header =0,index_col=0)
print(df.head())
#X = pd.concat([df['ValidRead'],df['ValidDim']], axis=1)
X = np.array(df.drop(['LFT','Irreg','MultiRead','ValidDim'],1))
#X = np.array(df.drop(['ValidDim','Irreg'],1))
#X = np.array(df.drop(['oga','owi','ohe','oa','ole','obv','otve','speed','owe','ValidRead'],1))

#X = np.array(df.drop(['LFT','MultiRead','TooBig','ValidDim'],1))
#X=np.array((df['ValidRead'],df['ValidDim'])).T
#X = pd.concat(df['ValidDim'], df['Irreg'])
#X_prime = np.array(df['Gap'], df['TooBig'])
y = np.array(df['LFT'])
#X[:,0]=X[:,0].astype(int)
#X[174][0]=40
X=preprocessing.scale(X)
print(len(X),len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""
Logistic Regression
"""
clf_logistic = linear_model.LogisticRegression(C=1e5)
clf_logistic.fit(X_train, y_train)
accuracy = clf_logistic.score(X_test, y_test)
y_score = clf_logistic.decision_function(X_test)
#print('Logistic Regression Score: ', accuracy)
# print('Ligistic Regression Score: ', y_score)


average_precision = average_precision_score(y_test, y_score)

#print('Logistic average precision-recall score: {0:0.2f}'.format(average_precision))

precision, recall, _ = precision_recall_curve(y_test, y_score)

plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
plt.fill_between(recall, precision, step='post', alpha=0.2,
                 color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Logistic Precision-Recall curve: AP={0:0.2f}'.format(
          average_precision))

a = clf_logistic.predict(X_test)
print('F1 score for logistic regression: ',f1_score(y_test, a, average='macro'))




"""
Random Forest
"""
clf_RF = RandomForestClassifier(n_jobs=2, random_state=0)
clf_RF.fit(X_train, y_train)
accuracy = clf_RF.score(X_test, y_test)
#print('Random Forest Score', accuracy)
print('This is the importances of different features: ',clf_RF.feature_importances_)

a = clf_RF.predict(X_test)

print('F1 score for Random Forest: ',f1_score(y_test, a, average='macro'))

"""
SVM
"""
clf_SVM = svm.SVC()
clf_SVM.fit(X_train, y_train)
accuracy = clf_SVM.score(X_test, y_test)
#print('SVM Score: ', accuracy)
a = clf_SVM.predict(X_test)

print('F1 score for SVM: ',f1_score(y_test, a, average='macro'))
"""
AdaBoost
"""
clf_AB = AdaBoostClassifier()
clf_AB.fit(X_train, y_train)
accuracy = clf_AB.score(X_test, y_test)
#print('AdaBoost Score: ', accuracy)
a = clf_AB.predict(X_test)

print('F1 score for AdaBoost: ',f1_score(y_test, a, average='macro'))
"""
MLP
"""
clf_MLP = MLPClassifier(alpha=1e-5, hidden_layer_sizes=(10, 5, 3), random_state=1)
clf_MLP.fit(X_train, y_train)
accuracy = clf_MLP.score(X_test, y_test)
#print('MLP Score: ', accuracy)
a = clf_MLP.predict(X_test)

print('F1 score for MLP: ',f1_score(y_test, a, average='macro'))
