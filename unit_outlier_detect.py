import pandas as pd
import numpy as np 
import csv, os, math

print('start running')

count_speed_unit = 0
count_otl_unit = 0
count_tt_unit = 0
count_oga_unit = 0
count_size_unit = 0
count_obv_unit = 0
count_orv_unit = 0
count_otve_unit = 0
count_owe_unit = 0

for filename in os.listdir('Objectdata'):
	try:
		print(filename)
		df = pd.read_csv('./Objectdata/'+filename, sep=',' , quoting=csv.QUOTE_ALL,  dtype=str)
		d = df['speed_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'ft/min' :
				count_speed_unit += d[i]

		d = df['otl_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'inch' :
				count_otl_unit += d[i]

		d = df['tt_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'ms' :
				count_tt_unit += d[i]

		d = df['oga_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'inch' :
				count_oga_unit += d[i]

		d = df['size_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'inch':
				count_size_unit += d[i]

		d = df['oa_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'degree/10' :
				count_oa_unit += d[i]

		d = df['obv_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'inch3/10' :
				count_obv_unit += d[i]

		d = df['orv_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'inch3/10' :
				count_orv_unit += d[i]

		d = df['otve_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'mm/sec' :
				count_otve_unit += d[i]

		d = df['owe_Unit'].value_counts().to_dict()
		for i in d:
			if i != 'LB':
				count_owe_unit += d[i]

		# print('count_speed_unit', count_speed_unit)
		# print('count_otl_unit', count_otl_unit)
		# print('count_tt_unit', count_tt_unit)
		# print('count_oga_unit', count_oga_unit)
		# print('count_size_unit', count_size_unit)
		# print('count_obv_unit', count_obv_unit )
		# print('count_orv_unit', count_orv_unit)
		# print('count_otve_unit', count_otve_unit) 
		# print('count_owe_unit', count_otve_unit)
	except pd.io.common.EmptyDataError:
		pass
print('count_speed_unit', count_speed_unit)
print('count_otl_unit', count_otl_unit)
print('count_tt_unit', count_tt_unit)
print('count_oga_unit', count_oga_unit)
print('count_size_unit', count_size_unit)
print('count_obv_unit', count_obv_unit )
print('count_orv_unit', count_orv_unit)
print('count_otve_unit', count_otve_unit) 
print('count_owe_unit', count_otve_unit)