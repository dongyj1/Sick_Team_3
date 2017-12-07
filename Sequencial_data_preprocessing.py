#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:33:44 2017

@author: changlongjiang
"""
from pandas import read_csv
dataset = read_csv('Object data/object8.15.csv')
dataset = dataset.drop(['devicename','deviceid','incr', 'tokenid', 'seqnb','timestamp1','otl','otl_Unit','tt','tt_Unit'], axis=1)
dataset = dataset.drop(['devicelist','Clipping','PeError'], axis=1)
k = 0
for i in dataset['oga_Unit']:
    
    if i != 'inch':
        #print(i,dataset['oga'][k])
        dataset.at[k, 'oga'] = 0
        #dataset.set_value('oga', str(k), 0)
        #print('1',i,dataset['oga'][k])
    k+=1
k = 0 
c = 0
for i in dataset['speed_Unit']:
    if i != 'ft/min':
        k+=1
        #print(dataset['speed'][c])
        dataset.at[c, 'speed'] = dataset['speed'][c]*0.19685
        #print(dataset['speed'][c])
        #print(k,dataset.loc[c])
    c+=1
dataset = dataset.drop(['oga_Unit'], axis=1)
dataset = dataset.drop(['orv','orv_Unit'], axis=1)
dataset = dataset.drop(['oa_Unit','obv_Unit'], axis=1)
dataset = dataset.drop(['otve_Unit'], axis=1)
dataset = dataset.drop(['owe_Unit'], axis=1)
dataset = dataset.drop(['speed_Unit'], axis=1)
dataset = dataset.drop(['size_Unit'], axis=1)
dataset.set_index('timestamp', inplace=True) 

'''
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

dataset['LFT'].plot()
plt.legend()
plt.show()
'''
dataset.to_csv('processed/8_15.csv', header = True)