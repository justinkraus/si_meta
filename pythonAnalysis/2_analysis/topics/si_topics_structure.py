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
from itertools import combinations


#create combined df with just museum and topics
df = pd.read_csv("./si_combined.csv")
print("done reading!")

df = df.drop(columns=['id',
				'title',
				'record_ID',
				'title_sort',
				'guid',
				'media_count',
				'media_id',
				'name_label',
				'name_content',
				'artist',
				'object_type',
				'medium',
				'date'])
print("done dropping!")

# #data frame info
print(df.info(verbose=True, null_counts=True))

# df_g =df.groupby(['name_label','name_content','topics','setName']).size().sort_values(ascending=False)

#split topics into individual rows
df['topics']=df['topics'].str.split("|")
df_t = df.explode('topics').reset_index(drop=True)

print(df_t['topics'].head(20))

df_g =df_t.groupby(['unitCode','topics']).size().to_frame('count').reset_index().sort_values(by=['count'],ascending=False)
print("done grouping!")
##Filters
#remove counts below 45
df_g = df_g[df_g['count'] > 45]

##Remove anthropology museum codes
df_g = df_g[df_g['unitCode'] != 'NMNHANTHRO']

#add numbered column
df_g['ID'] = np.arange(len(df_g)) 

print(df_g.head(20))
df_g.to_csv('df_g_nodesf.csv', mode='a')

def combine(batch):
    """Combine all products within one batch into pairs"""
    return pd.Series(list(combinations(set(batch), 2)))

edges = df_g.groupby('topics')['ID'].apply(combine).value_counts()
edges = edges.reset_index()
edges = pd.concat([edges, edges['index'].apply(pd.Series)], axis=1)
edges.drop(['index'], axis=1, inplace=True)
print(edges.head(20))
edges.columns = 'Weight','Source','Target'

print(edges.head(20))
edges.to_csv('df_g_edgesf.csv', mode='a')


#pivot data and add combinations of 



#save to csv
# df_g.to_csv('df_g_topics.csv', mode='a')
# print(df_g.head(20))

###############################################
#attempt at reading pkl
# df = pd.read_pickle("./df_test.pkl")

# print(df.info(verbose=True, null_counts=True))

# print(df['topics'].value_counts())

#attempt at converting pickle to csv
# your_pickle_obj = pickle.loads(open('./df_test.pkl', 'rb').read())
# with open('df_test.csv', 'a', encoding='utf8') as csv_file:
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

