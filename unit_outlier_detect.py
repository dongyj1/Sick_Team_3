import pandas as pd
import numpy as np 
import csv, os

print('start running')
u_cols = ['speed_Unit']
count = 0

for filename in os.listdir('Objectdata'):
	try:
		print(filename)
		df = pd.read_csv('./Objectdata/'+filename, sep=',' , quoting=csv.QUOTE_ALL, usecols=u_cols, dtype=str)
		d = df['speed_Unit'].value_counts().to_dict()
		if('mm/sec' in d):
			count += d['mm/sec']
	except pd.io.common.EmptyDataError:
		pass
print(count)