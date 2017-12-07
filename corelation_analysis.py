import pandas as pd 
import csv, os
import numpy as np
import matplotlib.pyplot as plt

print('start running')
u_cols = ['timestamp', 'speed', 'speed_Unit', 'LFT']

# df = pd.read_csv('object7.4.csv', quoting=csv.QUOTE_ALL, usecols=u_cols, dtype=str)

# for idx, row in df.iterrows():
#     if(row['speed_Unit'] != 'ft/min'):
#         print(row['speed_Unit'])
#         row['speed'] = str(float(row['speed']) / 5.08)

# df = df.drop('speed_Unit', 1)

# df[['speed','LFT']] = df[['speed','LFT']].apply(pd.to_numeric)

corelations = []
for filename in os.listdir('./Objectdata/'):
    try:
        df = pd.read_csv('./Objectdata/'+filename, sep=',', quoting=csv.QUOTE_ALL, usecols=u_cols, dtype=str)
        for idx, row in df.iterrows():
            if(row['speed_Unit'] != 'ft/min'):
                # print(row['speed_Unit'])
                row['speed'] = str(float(row['speed']) / 5.08)
        df = df.drop('speed_Unit', 1)
        df[['speed','LFT']] = df[['speed','LFT']].apply(pd.to_numeric)
        corelation = df['speed'].corr(df['LFT'], method='pearson', min_periods=1)
        corelations.append(corelation)
    except pd.io.common.EmptyDataError:
        pass 

plt.plot(corelations)
plt.ylabel('corelation')
plt.xlabel('days')
plt.show()