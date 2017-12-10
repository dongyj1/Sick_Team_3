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
import time
from sklearn.neural_network import MLPClassifier

def transferTime(timestamp): 
    #to transfer timestamp to datetime type
    #where timestamp is pandas dataframe
    for i in range(len(timestamp)):
        temp = datetime.strptime(timestamp.loc[i,"timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        timestamp.loc[i,"timestamp"] = time.mktime(temp.timetuple())
    return timestamp

def readDataTop(filename,datalist):
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


def calculate_throughput(object_data,heart_data):
    #calculate throughput of one day and write them into heartbeat data
    datalist = ["timestamp"]
    obj_time_data = transferTime(readDataTop(object_data,datalist))
    heart_time_data = transferTime(readDataTop(heart_data,datalist))
    df = pd.read_csv(heart_data)
    idx = 0
    counter = 0
    for j in range(len(obj_time_data)):
        try:
            #print("heart time" + str(heart_time_data.loc[idx,"timestamp"]))
            #print("obj time" + str(obj_time_data.loc[j,"timestamp"]))
            
            if(int(obj_time_data.loc[j,"timestamp"]) <= int(heart_time_data.loc[idx,"timestamp"]) and int(obj_time_data.loc[j,"timestamp"]) > int(heart_time_data.loc[idx,"timestamp"])-60):
                counter += 1
            else:
                heart_time_data.loc[idx,"throughput"] = counter
                counter = 1
                idx += 1
        except:
            counter += 1
    heart_time_data.loc[idx,"throughput"] = counter
    for i in range(len(heart_time_data)):
        if (str(heart_time_data.loc[i,"throughput"])  == "nan"):
            heart_time_data.loc[i,"throughput"] = 0
    heart_time_data = heart_time_data.loc[: , "throughput"]
    df = pd.concat([df, heart_time_data], axis=1, join_axes=[df.index])
    df.to_csv(heart_data)
#print("+++++++++++++++++++++")
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

heart_filename = ["Heartbeat data/heartbeat7.4.csv",
            "Heartbeat data/heartbeat7.5.csv",
            "Heartbeat data/heartbeat7.6.csv",
            "Heartbeat data/heartbeat7.7.csv",
            "Heartbeat data/heartbeat7.8.csv",
            "Heartbeat data/heartbeat7.9.csv",
            "Heartbeat data/heartbeat7.10.csv",
            "Heartbeat data/heartbeat7.11.csv",
            "Heartbeat data/heartbeat7.12.csv",
            "Heartbeat data/heartbeat7.13.csv",
            "Heartbeat data/heartbeat7.14.csv",
            "Heartbeat data/heartbeat7.15.csv",
            "Heartbeat data/heartbeat7.16.csv",
            "Heartbeat data/heartbeat7.17.csv",
            "Heartbeat data/heartbeat7.18.csv",
            "Heartbeat data/heartbeat7.19.csv",
            "Heartbeat data/heartbeat7.20.csv",
            "Heartbeat data/heartbeat7.21.csv",
            "Heartbeat data/heartbeat7.22.csv",
            "Heartbeat data/heartbeat7.23.csv",
            "Heartbeat data/heartbeat7.24.csv",
            "Heartbeat data/heartbeat7.25.csv",
            "Heartbeat data/heartbeat7.26.csv",
            "Heartbeat data/heartbeat7.27.csv",
            "Heartbeat data/heartbeat7.28.csv",
            "Heartbeat data/heartbeat7.29.csv",
            "Heartbeat data/heartbeat7.30.csv",
            "Heartbeat data/heartbeat7.31.csv",
            "Heartbeat data/heartbeat8.1.csv",
            "Heartbeat data/heartbeat8.2.csv",
            "Heartbeat data/heartbeat8.3.csv",
            "Heartbeat data/heartbeat8.4.csv",
            "Heartbeat data/heartbeat8.5.csv",
            "Heartbeat data/heartbeat8.6.csv",
            "Heartbeat data/heartbeat8.7.csv",
            "Heartbeat data/heartbeat8.8.csv",
            "Heartbeat data/heartbeat8.9.csv",
            "Heartbeat data/heartbeat8.10.csv",
            "Heartbeat data/heartbeat8.11.csv",
            "Heartbeat data/heartbeat8.12.csv",
            "Heartbeat data/heartbeat8.13.csv",
            "Heartbeat data/heartbeat8.14.csv",
            "Heartbeat data/heartbeat8.15.csv",]

pileDf = pd.DataFrame()#inital dataframe
allDf = pd.DataFrame()#inital dataframe
datalist = [ 'oga' , 'seqnb' , 'Irreg' , 'MultiRead' , 'TooBig' , 'Gap']
for i in range(len(filename)):
    try:
        tmpDf = readDataTop(filename[i], datalist)
        #calculate_throughput(filename[i],heart_filename[i])
        print("processing " + str(filename[i]) + " and " + str(heart_filename[i]))
    except:
        pass
    findSideBySide(tmpDf)# sutract all the features we needs
    
    pileDf = subtractFeature(tmpDf)
    addPileUpLabel(tmpDf,pileDf)
    allDf = allDf.append(tmpDf)
    
allDf = allDf.loc[: , [  'Irreg' , 'MultiRead' , 'TooBig' , 'pileUp']]



#================================training==============================

X = np.array(allDf.loc[: , [  'Irreg' , 'MultiRead' , 'TooBig' ]])
y = np.array(allDf['pileUp'])
#X[:,0]=X[:,0].astype(int)
#X[174][0]=40
X=preprocessing.scale(X)
print("+++++++++++++++++++++++++++++++++")
print(len(X),len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


"""
#Ligistic Regression
"""
clf_ligistic = linear_model.LogisticRegression(C=100,solver = 'lbfgs')

clf_ligistic.fit(X_train, y_train)
accuracy = clf_ligistic.score(X_test, y_test)
y_score = clf_ligistic.predict(X_test)
print("f1 score of pridiction is ", f1_score(y_test,y_score,average = 'macro'))
#print('Ligistic Regression Score: ', accuracy)
print('Ligistic Regression param: ', clf_ligistic.get_params(deep=True))
#n_classes = y.shape[1]

"""
#SVM
"""
clf_SVM = svm.SVC(C = 2, gamma = 100)
clf_SVM.fit(X_train, y_train)
accuracy = clf_SVM.score(X_test, y_test)
y_score1 = clf_SVM.predict(X_test)
print("f1 score of pridiction is ", f1_score(y_test,y_score1,average = 'macro'))
#print('Random Forest Score', accuracy)
#print('This is the importances of different features: ',clf_RF.feature_importances_)
print('Random Forest param: ', clf_SVM.get_params(deep=True))

"""
#MLP
"""
mlp = MLPClassifier(hidden_layer_sizes=(20,), max_iter=30, alpha=1e-4,
                    solver='sgd', verbose=10, tol=1e-4, random_state=1,
                    learning_rate_init=.1)
mlp.fit(X_train, y_train)
y_score1 = mlp.predict(X_test)
print("f1 score of pridiction is ", f1_score(y_test,y_score1,average = 'macro'))
#print('Random Forest Score', accuracy)
#print('This is the importances of different features: ',clf_RF.feature_importances_)
print('Random Forest param: ', mlp.get_params(deep=True))