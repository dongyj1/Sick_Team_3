# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 02:45:43 2017

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


datalist = ["timestamp"]
obj_time_data = transferTime(readDataTop(filename[1],datalist))
heart_time_data = transferTime(readDataTop(heart_filename[1],datalist))
df = pd.read_csv(heart_filename[1])
idx = 0
counter = 0
for j in range(len(obj_time_data)):
    try:
        print("heart time" + str(heart_time_data.loc[idx,"timestamp"]))
        print("obj time" + str(obj_time_data.loc[j,"timestamp"]))
        
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
df.to_csv(heart_filename[1])
#print("+++++++++++++++++++++")
