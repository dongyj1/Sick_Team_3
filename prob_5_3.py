#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 13:52:30 2017

@author: xogoss
"""

#prob_5 question_3#
import os
from pandas import read_csv
from pandas import DataFrame
import pandas as pd

path = "/Users/xogoss/Documents/boston/CS542/project/Sick_Team_3-master/Heartbeat data" #文件夹目录  
files= os.listdir(path)
files = files[1:]

count = [0,0,0,0,0,0]
for fff in files:
    print(fff)
    
    try:
        k = read_csv(path + '/' + fff, header = 0, index_col = 0)
        print(k['CAN1: Dev. 1numberoccur'][1])
        for i in range(2, len(k['CAN1: Dev. 1numberoccur'])):
            try:
                if(k['CAN1: Dev. 1numberoccur'][i] != k['CAN1: Dev. 1numberoccur'][i - 1]):
                    count[0] += 1
            except KeyError:
                pass
            try:
                if(k['CAN1: Dev. 2numberoccur'][i] != k['CAN1: Dev. 2numberoccur'][i - 1]):
                    count[1] += 1
            except KeyError:
                pass
            try:
                if(k['CAN1: Dev. 3numberoccur'][i] != k['CAN1: Dev. 3numberoccur'][i - 1]):
                    count[2] += 1
            except KeyError:
                pass
            try:
                if(k['CAN1: Dev. 4numberoccur'][i] != k['CAN1: Dev. 4numberoccur'][i - 1]):
                    count[3] += 1
            except KeyError:
                pass
            try:
                if(k['CAN1: Dev. 5numberoccur'][i] != k['CAN1: Dev. 5numberoccur'][i - 1]):
                    count[4] += 1
            except KeyError:
                pass
            try:
                if(k['CAN1: Dev. 6numberoccur'][i] != k['CAN1: Dev. 6numberoccur'][i - 1]):
                    count[5] += 1
            except KeyError:
                pass
    except pd.io.common.EmptyDataError:
        pass
        
print(count)