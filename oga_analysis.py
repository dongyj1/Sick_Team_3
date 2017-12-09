#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 01:10:59 2017

@author: xogoss
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score


filelist = ["object7.4.csv","object7.5.csv"]
x = pd.DataFrame()
x_t = pd.DataFrame()
y = []

for file in filelist:
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
    '''
    for time in temp_time:
        cur_date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
        time_datetime.append(cur_date)
        time_interval.append((cur_date - time_datetime[len(time_datetime)-2]).total_seconds())
    temp['timestamp'] = pd.Series(time_datetime)
    temp['sub_time'] = pd.Series(time_interval)
    temp = temp.drop(0)
    '''
    x = x.append(temp)
    x_t = x_t.append(temp_t)

plt.title("y = gap, x = oga")
plt.plot(x['oga'],x['gap'],'ro')
plt.axis([-1,20,-1,1])
plt.show()

plt.title("y = gap, x = oga")
plt.plot(x['oga'],x['gap'],'ro')
plt.axis([12,17,-1,1])
plt.show()

plt.title("y = gap, x = sub_time")
plt.plot(x['sub_time'],x['gap'],'ro')
plt.axis([-1,20,-1,1])
plt.show()

plt.title("correlation between oga and time interval")
plt.ylabel('oga')
plt.xlabel('time_interval')
plt.plot(x['sub_time'],x['oga'],'yo')
plt.axis([-1,20,-100,1500])
plt.show()

plt.title("y = negative oga, x = sub_time")
plt.plot(x_t['sub_time'],x_t['oga'],'ro')
plt.axis([-1,20,-2000,500])
plt.show()


#=======================================#

x_training = np.array(x['oga'])
y_training = np.array(x['gap'])

x_interval_training = np.array(x['sub_time'])
x_2_training = np.array([x['sub_time'], x['oga']]).T

X_train, X_test, Y_train, Y_test = train_test_split(x_training.reshape(-1,1), y_training.reshape(len(x['gap']),), test_size = 0.2, random_state = 42)

LogReg = LogisticRegression(penalty = 'l1', C = 1)
LogReg.fit_intercept = True
LogReg.fit(X_train, Y_train)
y_pred = LogReg.predict(X_test)
print("the accuracy of it is:", accuracy_score(Y_test, LogReg.predict(X_test)))
from sklearn.metrics import classification_report
print(classification_report(Y_test, LogReg.predict(X_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(Y_test, y_pred)
print(confusion_matrix)

print("coef: ", LogReg.coef_)
print("intercept: ",LogReg.intercept_)

#=======time interval & gap=============#
print("========================================")
y_training_oga = np.array(x['oga'])
X_time_train, X_time_test, Y_time_train, Y_time_test = train_test_split(x_interval_training.reshape(-1,1), y_training_oga.reshape(len(x['gap']),), test_size = 0.2, random_state = 42)
from sklearn.metrics import mean_squared_error, r2_score


LogReg_time = LinearRegression()
LogReg_time.fit(X_time_train, Y_time_train)
y_time_pred = LogReg_time.predict(X_time_test)
err = mean_squared_error(Y_time_test, y_time_pred)
r2_score(Y_time_test, y_time_pred)
print("err:", err)
print("variance:", r2_score)
print("coef: ", LogReg_time.coef_)
print("intercept: ",LogReg_time.intercept_)

plt.scatter(X_time_test, Y_time_test,  color='black')
plt.plot(X_time_test, y_time_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()

'''
by = LogReg_time.coef_ * X_time_train
plt.plot(by,[-1, 20],'b-',label='Decision Boundary')
plt.legend()
plt.axis([-1,1400,-1, 20])
'''
#========subtime & oga=================#
print("========================================")
'''
X_2_train, X_2_test, Y_2_train, Y_2_test = train_test_split(x_2_training, y_training.reshape(len(x['gap']),), test_size = 0.2, random_state = 42)


LogReg_2 = LogisticRegression(solver = 'sag',multi_class = 'multinomial', penalty = 'l2', C = 1)
LogReg_2.fit_intercept = True
LogReg_2.fit(X_2_train, Y_2_train)
y_2_pred = LogReg_2.predict(X_2_test)
print("the accuracy of it is:", accuracy_score(Y_2_test, LogReg_2.predict(X_2_test)))
from sklearn.metrics import classification_report
print(classification_report(Y_2_test, LogReg_2.predict(X_2_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix_2 = confusion_matrix(Y_2_test, y_2_pred)
print(confusion_matrix_2)

print("coef: ", LogReg_2.coef_)
print("intercept: ",LogReg_2.intercept_)
'''

