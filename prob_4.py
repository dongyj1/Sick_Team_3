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
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
import csv
import datetime

def transferTime(timestamp):
    pass

def readDataTonp(filename):
    oga = []
    Irreg = []
    MultiRead = []
    TooBig = []
    sqnb = []
    timestamp = []
    with open(filename) as ob_file:
        reader = csv.reader(ob_file)
        for row in reader:
            oga.append(row[11])
            TooBig.append(row[30])
            Irreg.append(row[34])
            MultiRead.append(row[33])
            sqnb.append(row[5])
            timestamp.append(row[2])
        del oga[0]
        del TooBig[0]
        del Irreg[0]
        del MultiRead[0]
        del sqnb[0]
        del timestamp[0]
    oga = np.asarray(oga,dtype=np.float32)
    Irreg = np.asarray(Irreg,dtype=np.int32)
    MultiRead = np.asarray(MultiRead,dtype=np.int32)
    TooBig = np.asarray(TooBig,dtype=np.int32)
    sqnb = np.asarray(sqnb,dtype=np.float32)
    timestamp = np.asarray(timestamp)
    return oga,Irreg,MultiRead,TooBig,sqnb,timestamp

oga,Irreg,MultiRead,TooBig,sqnb,timestamp = readDataTonp("Object data/object7.4.csv")

tmpIdx1 = np.where(oga == -1)[0]
tmpIdx2 = np.where(oga < -100)[0]
minOneIdx = []
negaIdx = []
for i in tmpIdx1:
    minOneIdx.append(sqnb[i])
for i in tmpIdx2:
    negaIdx.append(sqnb[i])

plt.plot(oga)
#return minOneIdx[0],negaIdx[0]

#plt.plot(Irreg_np)
#plt.plot(MultiRead_np)
#plt.plot(TooBig_np)
    
