from dask.distributed import Client
import dask.bag as db
import tables
import os
import glob
import json
import s3fs
import time
import numpy as np
import pandas as pd
import multiprocessing
from os import listdir
from os.path import isfile, join
from flatten_json import flatten
from pandas.io.json import json_normalize


nmah_items = []
json_flatten_df = pd.DataFrame()

# dir_path = './nmah_files/'
dir_path = '/Users/stan/Python/nmah_files_ex/'
object_list = []
all_json_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(".json")]
start_num = 0
appended_data = []

for file in all_json_files:
	while start_num < len(all_json_files):
		for _ in range(start_num,len(all_json_files)):
			file = all_json_files[start_num]
			print(file)
			with open(file, 'r') as input_file:
				for line in input_file:
					nmah_items.append(json.loads(line))

				json_flatten = (flatten(d) for d in nmah_items)

				json_flatten_df = pd.DataFrame(json_flatten)

				appended_data.append(json_flatten_df)

				start_num = start_num + 1

				print("done with " + file)

				break		
	print("concating!")
	nmah_df_all = pd.concat(appended_data, axis=0, ignore_index=True).reset_index(drop=True)
	print("pickling!")
	nmah_df_all.to_pickle("./nmah_df_all_ex.pkl")
	print("done with all!")
	break



##works for example folder
# nmah_items = []
# json_flatten_df = pd.DataFrame()

# # dir_path = './nmah_files/'
# dir_path = '/Users/stan/Python/nmah_files/'
# object_list = []
# all_json_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(".json")]
# start_num = 0

# for file in all_json_files:
# 	while start_num < len(all_json_files):
# 		for _ in range(start_num,len(all_json_files)):
# 			file = all_json_files[start_num]
# 			print(file)
# 			with open(file, 'r') as input_file:
# 				for line in input_file:
# 					nmah_items.append(json.loads(line))

# 				json_flatten = (flatten(d) for d in nmah_items)

# 				json_flatten_df = pd.DataFrame(json_flatten)

# 				nmah_df_all = json_flatten_df.append(json_flatten_df)

# 				print(nmah_df_all.shape)

# 				start_num = start_num + 1

# 				print("done with " + file)

# 				break		
# 	print("pickling!")
# 	nmah_df_all.to_pickle("./nmah_df_all.pkl")
# 	print("done with all!")
# 	break




##WORKS FOR ONE

# nmah_items = []

# for line in open('./nmah_files/001.json', 'r'):
# 	nmah_items.append(json.loads(line))

# print(nmah_items)
# # json_flatten = flatten(json_file)

# json_flatten = (flatten(d) for d in nmah_items)

# json_flatten_df = pd.DataFrame(json_flatten)

# json_flatten_df.to_csv('json_flatten_df_example.csv', index=False)
