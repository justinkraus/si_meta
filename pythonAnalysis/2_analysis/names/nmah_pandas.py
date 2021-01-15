from dask.distributed import Client
import dask.bag as db
import json
import s3fs
import time
import numpy as np
import pandas as pd
import pickle
import base64
import csv

# #saam
# saam_df = pd.read_pickle("./saam_df.pkl")

# print(saam_df.info())

#nmah create df
nmah_df = pd.read_csv("./nmah_df_test1.csv")

# #data frame info
# print(nmah_df.info(verbose=True, null_counts=True))

# nmah_df_g =nmah_df.groupby(['name_label','name_content','topics','setName']).size().sort_values(ascending=False)

#split topics into individual rows
nmah_df['topics']=nmah_df['topics'].str.split("|")
nmah_df_t = nmah_df.explode('topics').reset_index(drop=True)

print(nmah_df_t['topics'].head(20))

nmah_df_g =nmah_df_t.groupby(['name_label','name_content','topics','setName']).size().sort_values(ascending=False)

nmah_df_g.to_csv('nmah_df_g_topics.csv', mode='a')
print(nmah_df_g.head(20))


#attempt at reading pkl
# nmah_df = pd.read_pickle("./nmah_df_test.pkl")

# print(nmah_df.info(verbose=True, null_counts=True))

# print(nmah_df['topics'].value_counts())

#attempt at converting pickle to csv
# your_pickle_obj = pickle.loads(open('./nmah_df_test.pkl', 'rb').read())
# with open('nmah_df_test.csv', 'a', encoding='utf8') as csv_file:
#     wr = csv.writer(csv_file, delimiter='|')
#     pickle_bytes = pickle.dumps(your_pickle_obj)            # unsafe to write
#     b64_bytes = base64.b64encode(pickle_bytes)  # safe to write but still bytes
#     b64_str = b64_bytes.decode('utf8')          # safe and in utf8
#     wr.writerow(['id',
# 				'unitCode',
# 				'title',
# 				'record_ID',
# 				'title_sort',
# 				'guid',
# 				'media_count',
# 				'topics',
# 				'setName',
# 				'associated person',
# 				'media_id', 
# 				b64_str])

