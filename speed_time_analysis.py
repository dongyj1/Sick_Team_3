import pandas as pd 
import csv, os
import numpy as np
import matplotlib.pyplot as plt

print('start running')
u_cols = ['timestamp', 'speed', 'speed_Unit']


# f, axarr = plt.subplots(4)
counter = 0
means = []
variances = []
for filename in os.listdir('./Objectdata/'):
    try:
        timeline = []
        speeds = []
        df = pd.read_csv('./Objectdata/'+filename, sep=',', quoting=csv.QUOTE_ALL, usecols=u_cols, dtype=str)
        
        df['speed'] = df['speed'].apply(pd.to_numeric)
        df[np.isnan(df['speed'])] = 0
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S.%f")

        for idx, row in df.iterrows():
            if(row['speed_Unit'] != 'ft/min'):
                row['speed'] = row['speed'] / 5.08
            speeds.append(row['speed'])
            timeline.append(row['timestamp'])
        # axarr[counter].plot(timeline, speeds)
        counter+=1
        # print('mean', np.mean(speeds), filename)
        # print('var', np.var(speeds), filename)
        means.append(np.mean(speeds))
        variances.append(np.var(speeds))
    except Exception as e:
        print(e)

plt.plot(means, color='r', label='mean')
plt.plot(variances, color='b', label='variance')
plt.show()



