from dask.distributed import Client
import dask.bag as db
import json
import s3fs
import time
import numpy as np
import pandas as pd

fs = s3fs.S3FileSystem(anon=True)
# print(fs.ls('smithsonian-open-access/metadata/edan/nmah'))

client = Client(processes=False)

b = db.read_text('s3://smithsonian-open-access/metadata/edan/nmah/*.txt',
                storage_options={'anon': True}).map(json.loads)

def flatten_new(record):
    flattened_record = dict()
    flattened_record['id'] = record['id']
    flattened_record['unitCode'] = record['unitCode']
    flattened_record['title'] = record['title']
    flattened_record['record_ID'] = record['content']['descriptiveNonRepeating']['record_ID']
    flattened_record['title_sort'] = record['content']['descriptiveNonRepeating']['title_sort']
    flattened_record['guid'] = record['content']['descriptiveNonRepeating']['guid']
    media_count = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('mediaCount',np.nan)
    flattened_record['media_count'] = float(media_count)
    media = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('media',[])   
    if len(media):
        try: 
            flattened_record['media_id'] = media[0]['idsId']
        except KeyError:
            flattened_record['media_id'] = "N/A"

    topics = record['content'].get('indexedStructured',{}).get('topic',[])
    if len(topics):
        flattened_record['topics'] = '|'.join(topics)

    obj_set = record['content'].get('freetext',{}).get('setName',[])
    if len(obj_set):
        try:
            flattened_record['setName'] = obj_set[0]['content']
        except KeyError:
            flattened_record['setName'] = "N/A"

    name = record['content'].get('freetext', {}).get('name',{})
    if len(name):
        try:
            for i in range(len(name)):
                flattened_record['name_label'] = name[i]['label']
                flattened_record['name_content'] = name[i]['content']
        except KeyError:
            flattened_record['name_label'] = "N/A"
            flattened_record['name_label'] = "N/A"

    return flattened_record



nmah_json = b.map(flatten_new).compute()
nmah_df = pd.DataFrame(nmah_json)
nmah_df.to_csv("./nmah_df_test1.csv", mode='a')
