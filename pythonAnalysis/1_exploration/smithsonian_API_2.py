from dask.distributed import Client
import dask.bag as db
import os
import glob
import json
import s3fs
import time
import numpy as np
import pandas as pd
from flatten_json import flatten
from pandas.io.json import json_normalize

# file_list = []

# #gets array of file list
# fs = s3fs.S3FileSystem(anon=True)
# # file_list.append(fs.ls('smithsonian-open-access/metadata/edan/nmah'))
# file_list = fs.ls('smithsonian-open-access/metadata/edan/nmah')
# print(file_list)


# #attempt to read with pandas
# b = pd.read_json('s3://smithsonian-open-access/metadata/edan/nmah/*.txt',
#                 storage_options={'anon': True}).map(json.loads)

# nmah_example = b.take(1)[0]
# with open('nmah_metadata_example.json','w') as json_out:
# 	json.dump(nmah_example, json_out, indent=2)


# temp = pd.DataFrame()

# dfs = []

# for file in file_list:
#     data = pd.read_json(file, lines=True)
#     dfs.append(data)

# temp = pd.concat(dfs, ignore_index=True)

# temp.to_pickle("./nmah_df1.pkl")

client = Client(processes=False)

b = db.read_text('s3://smithsonian-open-access/metadata/edan/nmah/*.txt',
                storage_options={'anon': True}).map(json.loads)

print("bag to textfiles")

b.map(json.dumps).to_textfiles('./nmah_files/*.json')

print("done")

# nmah_example = b.take(1)[0]
# with open('nmah_metadata_example.json','w') as json_out:
# 	json.dump(nmah_example, json_out, indent=2)


# nmah_json = b.map(flatten_new).compute()
# nmah_df = pd.DataFrame(nmah_json)
# nmah_df.to_pickle("./nmah_df1.pkl")