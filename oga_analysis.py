#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:12:53 2017

@author: xogoss
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 15:54:02 2017

@author: xogoss
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LogisticRegression, LinearRegression, RANSACRegressor
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
import os

#path = "/Users/xogoss/Documents/boston/CS542/project/Sick_Team_3-master/Object data" #文件夹目录  
#fileslist= os.listdir(path)
#fileslist = fileslist[1:]
fileslist = ['object7.4.csv', 'object7.5.csv','object7.6.csv','object7.7.csv','object7.8.csv','object7.10.csv','object7.11.csv','object7.12.csv','object7.13.csv','object7.14.csv','object7.15.csv','object7.16.csv','object7.17.csv','object7.18.csv','object7.19.csv','object7.20.csv','object7.21.csv','object7.22.csv','object7.23.csv','object7.26.csv','object7.27.csv','object7.28.csv','object7.29.csv','object7.30.csv','object7.31.csv','object8.1.csv','object8.2.csv','object8.3.csv','object8.4.csv','object8.5.csv','object8.6.csv','object8.7.csv','object8.8.csv','object8.9.csv','object8.11.csv','object8.12.csv','object8.14.csv','object8.15.csv']
#fileslist = ['object7.4.csv']
x = pd.DataFrame()
x_t = pd.DataFrame()
y = []

for file in fileslist:
    df = pd.read_csv(file)
    #print(df.columns)
    temp = pd.DataFrame()
    temp_t = pd.DataFrame()
    oga = []
    oga_t = []
    gap = []
    gap_t = []
    time_datetime = []
    time_interval = []
    time_datetime_t = []
    time_interval_t = []
    last_date = 0
    for i in range(len(df['oga'])):
        cur_date = datetime.datetime.strptime(df['timestamp'][i], "%Y-%m-%dT%H:%M:%S.%f")
        if i == 0:
            interval = 0
        else:
            interval = (cur_date - last_date).total_seconds()

        if df['oga'][i] > 0:
            oga.append(df['oga'][i])
            gap.append(df['Gap'][i])
            time_datetime.append(cur_date)
            time_interval.append(interval)
            last_date = cur_date

        else:
            oga_t.append(df['oga'][i])
            gap_t.append(df['Gap'][i])
            time_datetime_t.append(cur_date)
            time_interval_t.append(interval)
            last_date = cur_date
            
    temp['oga'] = pd.Series(oga)
    temp_t['oga'] = pd.Series(oga_t)
    
    temp['gap'] = pd.Series(gap)
    temp_t['gap'] = pd.Series(gap_t)
    
    temp['timestamp'] = pd.Series(time_datetime)
    temp_t['timestamp'] = pd.Series(time_datetime)
    
    temp['sub_time'] = pd.Series(time_interval)
    temp_t['sub_time'] = pd.Series(time_interval)
    
    time_datetime = []
    time_interval = []

    x = x.append(temp)
    x_t = x_t.append(temp_t)
    
#########################################
#########################################
#########################################
x_training = np.array(x['oga'])
y_training = np.array(x['gap'])
X_train, X_test, Y_train, Y_test = train_test_split(x_training.reshape(-1,1), y_training.reshape(len(x['gap']),), test_size = 0.2, random_state = 42)

X = X_train
y = Y_train

pos = np.array([X[i] for i in range(X.shape[0]) if y[i] == 1])
neg = np.array([X[i] for i in range(X.shape[0]) if y[i] != 1])
pos = pos.flatten()
neg = neg.flatten()
#pos = np.hstack((pos, np.zeros((len(pos), 1))))
#neg = np.hstack((neg, np.zeros((len(neg), 1))))
pos_y = np.ones(len(pos))
neg_y = np.zeros(len(neg))

#X = np.r_[pos, neg]
#Y = np.array([0] * len(neg) + [1] * len(pos))
print(X.shape, y.shape)
clf = svm.SVC(kernel='linear')
clf.fit(X, y)
threshold = (-clf.intercept_/clf.coef_).flatten()[0]
print(-clf.intercept_/clf.coef_)

outlier = []
pos_no_outlier = pos.tolist()
pos_max = np.amax(pos)
neg_min = np.amin(neg)
for mm in pos:
    if(mm > neg_min):
        outlier.append(mm)
        pos_no_outlier.remove(mm)
        
pos_no_max = max(pos_no_outlier)
#print(pos_no_max, neg_min)
print("number of outliers", len(outlier))
def plot_data():
    plt.figure(figsize=(10,6))
    plt.plot(pos,pos_y,'k+',label='Positive Sample')
    plt.plot(neg,neg_y,'yo',label='Negative Sample')
    plt.plot([threshold,threshold],[-1,2],'b-',label='Decision Boundary')
    plt.axis([-.8,200,-1,3])
    plt.xlabel('oga')
    plt.ylabel('Gap')
    plt.legend()
    plt.grid(True)
    
plot_data()
