# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 23:32:51 2017

@author: suyux
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from sklearn.metrics import roc_curve, auc


def transferTime(timestamp): 
    #to transfer timestamp to datetime type
    for i in range(len(timestamp)):
        time_data.loc[i,"timestamp"] = datetime.strptime(time_data.loc[i,"timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
    return timestamp

def readDataTonp(filename,datalist):
    df = pd.read_csv(filename)
    df = df.loc[: , datalist]

    return df

def findSideBySide(df):
    sidebyside = []
    for i in df['oga']:
        if (int(i) < -1000):
            sidebyside.append(1)
        else:
            sidebyside.append(0)
    df['sideBySide'] = sidebyside

def subtractFeature(df):
    tmpDf = pd.DataFrame()
    count = 0
    idx = df.index[df['sideBySide'] == 1]
    for i in idx:
        tmpDf = tmpDf.append(df.iloc[i-5:i+1])
        #tmpDf = df[df['sideBySide'] == 1]
    tmpDf2 = df[df['Gap'] == 1]
    for i in tmpDf2['seqnb']:
        #print(count - int(i))
        if(count - int(i) > 0 or count - int(i) < -5):
            tmpDf2 = tmpDf2[tmpDf2['seqnb'] != i]
            #print("1111")
        count = int(i)
    tmpDf = tmpDf.append(tmpDf2)
    tmpDf.sort_index(inplace=True)
        
    return tmpDf
    
def addPileUpLabel(allDf,pileDf):
    """
    add pileup label to dataframe
    
    """
    pileUp = []
    for i in allDf.index.values:
        if i in pileDf.index.values:
            pileUp.append(1)
        else:
            pileUp.append(0)
    allDf['pileUp'] = pileUp  


def initialize_parameters(n_x, n_h, n_y):

    np.random.seed(1)
    
    ### START CODE HERE ### (≈ 4 lines of code)
    W1 = np.random.randn(n_h,n_x) * 0.01
    b1 = np.zeros([n_h,1])
    W2 = np.random.randn(n_y,n_h) * 0.01
    b2 = np.zeros([n_y,1])
    ### END CODE HERE ###
    
    assert(W1.shape == (n_h, n_x))
    assert(b1.shape == (n_h, 1))
    assert(W2.shape == (n_y, n_h))
    assert(b2.shape == (n_y, 1))
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    
    return parameters    


def calculate_throughput(object_data_file, heartbeat_data):
    #calculate throughput of one day and write them into heartbeat data
    datalist = ["timestamp"]
    time_data = readDataTonp(object_data_file,datalist)
    initial_time = datetime.strptime(time_data.loc[0,"timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
    
    
    pass
#===============main=========================
filename = ["Object data/object7.4.csv",
            "Object data/object7.5.csv",
            "Object data/object7.6.csv",
            "Object data/object7.7.csv",
            "Object data/object7.8.csv",
            "Object data/object7.9.csv",
            "Object data/object7.10.csv",
            "Object data/object7.11.csv",
            "Object data/object7.12.csv",
            "Object data/object7.13.csv",
            "Object data/object7.14.csv",
            "Object data/object7.15.csv",
            "Object data/object7.16.csv",
            "Object data/object7.17.csv",
            "Object data/object7.18.csv",
            "Object data/object7.19.csv",
            "Object data/object7.20.csv",
            "Object data/object7.21.csv",
            "Object data/object7.22.csv",
            "Object data/object7.23.csv",
            "Object data/object7.24.csv",
            "Object data/object7.25.csv",
            "Object data/object7.26.csv",
            "Object data/object7.27.csv",
            "Object data/object7.28.csv",
            "Object data/object7.29.csv",
            "Object data/object7.30.csv",
            "Object data/object7.31.csv",
            "Object data/object8.1.csv",
            "Object data/object8.2.csv",
            "Object data/object8.3.csv",
            "Object data/object8.4.csv",
            "Object data/object8.5.csv",
            "Object data/object8.6.csv",
            "Object data/object8.7.csv",
            "Object data/object8.8.csv",
            "Object data/object8.9.csv",
            "Object data/object8.10.csv",
            "Object data/object8.11.csv",
            "Object data/object8.12.csv",
            "Object data/object8.13.csv",
            "Object data/object8.14.csv",
            "Object data/object8.15.csv",]


pileDf = pd.DataFrame()#inital dataframe
allDf = pd.DataFrame()#inital dataframe
datalist = [ 'oga' , 'seqnb' , 'Irreg' , 'MultiRead' , 'TooBig' , 'Gap']
for file in filename:
    try:
        tmpDf = readDataTonp(file, datalist)
    except:
        pass
    findSideBySide(tmpDf)# sutract all the features we needs
    
    pileDf = subtractFeature(tmpDf)
    addPileUpLabel(tmpDf,pileDf)
    allDf = allDf.append(tmpDf)

allDf = allDf.loc[: , [  'Irreg' , 'MultiRead' , 'TooBig' , 'pileUp']]
datalist = ["timestamp"]
time_data = readDataTonp(filename[0],datalist)


#================================training==============================
"""
X = np.array(allDf.loc[: , [  'Irreg' , 'MultiRead' , 'TooBig' ]])
y = np.array(allDf['pileUp'])
#X[:,0]=X[:,0].astype(int)
#X[174][0]=40
X=preprocessing.scale(X)
print("+++++++++++++++++++++++++++++++++")
print(len(X),len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


#Ligistic Regression

clf_ligistic = linear_model.LogisticRegression(C=1e5)
clf_ligistic.fit(X_train, y_train)
accuracy = clf_ligistic.score(X_test, y_test)
y_score = clf_ligistic.predict(X_test)
print("f1 score of pridiction is ", f1_score(y_test,y_score,average = 'macro'))
print('Ligistic Regression Score: ', accuracy)
#n_classes = y.shape[1]

#Random Forest

clf_RF = RandomForestClassifier(n_jobs=2, random_state=0)
clf_RF.fit(X_train, y_train)
accuracy = clf_RF.score(X_test, y_test)
y_score1 = clf_RF.predict(X_test)
print("f1 score of pridiction is ", f1_score(y_test,y_score1,average = 'macro'))
print('Random Forest Score', accuracy)
print('This is the importances of different features: ',clf_RF.feature_importances_)
"""