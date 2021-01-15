from dask.distributed import Client
import dask.bag as db
import json
import s3fs
import time
import numpy as np
import pandas as pd

fs = s3fs.S3FileSystem(anon=True)
# print(fs.ls('smithsonian-open-access/metadata/edan/'))

client = Client(processes=False)

# 'nmnhanthro', 
# 'nmnhbirds', 
# 'nmnhbotany', 
# 'nmnheducation', 
# 'nmnhento', 
# 'nmnhfishes', 
# 'nmnhherps', 
# 'nmnhinv', 
# 'nmnhmammals', 
# 'nmnhminsci', 
# 'nmnhpaleo', 

museumcodes = [
'aaa', 
'acah', 
'acm', 
'cfchfolklife', 
'chndm', 
'fbr', 
'fs', 
'fsa', 
'fsg', 
'hac', 
'hmsg', 
'hsfa', 
'naa', 
'nasm', 
'nmaahc', 
'nmafa', 
'nmah', 
'nmai', 
'npg', 
'npm', 
'nzp', 
'saam', 
'si', 
'sia', 
'sil'
]

for i in range(0,len(museumcodes)): 
    museumid = museumcodes[i]

    b = db.read_text('s3://smithsonian-open-access/metadata/edan/' + museumid + '/*.txt',
                    storage_options={'anon': True}).map(json.loads)

    # nmah_example = b.take(1)[0]
    # with open('nmah_metadata_example.json','w') as json_out:
    # 	json.dump(nmah_example, json_out, indent=2)

    def flatten_new(record):
        flattened_record = dict()
        flattened_record['unitCode'] = record['unitCode']
        flattened_record['record_ID'] = record['content']['descriptiveNonRepeating']['record_ID']

        dates = record['content'].get('indexedStructured',{}).get('date',[])
        if len(dates):
            flattened_record['date'] = '|'.join(dates)
            

        obj_set = record['content'].get('freetext',{}).get('setName',[])
        if len(obj_set):
            try:
                flattened_record['setName'] = obj_set[0]['content']
            except KeyError:
                flattened_record['setName'] = "N/A"

        id_set = record['content'].get('freetext',{}).get('identifier',[])
        if len(id_set):
            try:
                flattened_record['identifier'] = id_set[0]['content']
            except KeyError:
                flattened_record['identifier'] = "N/A"


        # flattened_record['guid'] = record['content']['descriptiveNonRepeating']['guid']
        guid = record['content'].get('descriptiveNonRepeating',{}).get('guid',{})
        if len(guid):
            try:
                flattened_record['guid'] = guid
            except KeyError:
                flattened_record['guid'] = "N/A"

        # flattened_record['title_sort'] = record['content']['descriptiveNonRepeating']['title_sort']
        title_sort = record['content'].get('descriptiveNonRepeating',{}).get('title_sort',{})
        if len(title_sort):
            try:
                flattened_record['title_sort'] = title_sort
            except KeyError:
                flattened_record['title_sort'] = "N/A"

        if 'freetext' in record['content']:
            if 'objectType' in record['content']['freetext']:
                for obtype in record['content']['freetext']['objectType']:
                    if obtype['label'] == 'Type':
                        flattened_record['object_type'] = obtype['content']
            if 'physicalDescription' in record['content']['freetext']:
                for phys in record['content']['freetext']['physicalDescription']:
                    if phys['label'] == 'Medium':
                        flattened_record['medium'] = phys['content']
            if 'date' in record['content']['freetext']:
                for date in record['content']['freetext']['date']:
                    if date['label'] == 'Date':
                        flattened_record['date'] = str(date['content'])

        return flattened_record



    nmah_json = b.map(flatten_new).compute()
    nmah_df = pd.DataFrame(nmah_json)
    nmah_df.to_csv("./" + str(museumid) + ".csv", mode='a')
    # nmah_df.to_pickle("./nmah_df_test.pkl")


    # #original flatten
    # def flatten(record):
    #     """Take a single SAAM metadata record, and pulls out specific pieces of data.

    #     Parameters
    #     ----------
    #     record : dict
    #         A single SAAM metadata record in highly-nested dictionary format.

    #     Returns
    #     -------
    #     flattened_record: dict
    #         An un-nested dictionary that only contains the record id, unit code,
    #         object title, media_count, media_id, topic list, object type, and
    #         object medium.
    #     """
    #     flattened_record = dict()
    #     flattened_record['id'] = record['id']
    #     flattened_record['unitCode'] = record['unitCode']
    #     flattened_record['title'] = record['title']
    #     media_count = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('mediaCount',np.nan)
    #     flattened_record['media_count'] = float(media_count)
    #     media = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('media',[])   
    #     if len(media):
    #         try: 
    #         	flattened_record['media_id'] = media[0]['idsId']
    #         except KeyError:
    #         	flattened_record['media_id'] = "N/A"
            
    #     topics = record['content'].get('indexedStructured',{}).get('topic',[])
    #     if len(topics):
    #         flattened_record['topics'] = '|'.join(topics)
        
    #     if 'freetext' in record['content']:
    #         if 'objectType' in record['content']['freetext']:
    #             for obtype in record['content']['freetext']['objectType']:
    #                 if obtype['label'] == 'Type':
    #                     flattened_record['object_type'] = obtype['content']
    #         if 'physicalDescription' in record['content']['freetext']:
    #             for phys in record['content']['freetext']['physicalDescription']:
    #                 if phys['label'] == 'Medium':
    #                     flattened_record['medium'] = phys['content']
    #         if 'name' in record['content']['freetext']:
    #             for name in record['content']['freetext']['name']:
    #                 if name['label'] == 'Artist':
    #                     flattened_record['artist'] = name['content']
    #         if 'date' in record['content']['freetext']:
    #             for date in record['content']['freetext']['date']:
    #                 if date['label'] == 'Date':
    #                     flattened_record['date'] = str(date['content'])
                
    #     return flattened_record




    ##My first iteration of the flatten_new
    ##the freetext names did not capture all of the names
    # def flatten_new(record):
    #     flattened_record = dict()
    #     flattened_record['id'] = record['id']
    #     flattened_record['unitCode'] = record['unitCode']
    #     flattened_record['title'] = record['title']
    #     flattened_record['record_ID'] = record['content']['descriptiveNonRepeating']['record_ID']
    #     flattened_record['title_sort'] = record['content']['descriptiveNonRepeating']['title_sort']
    #     flattened_record['guid'] = record['content']['descriptiveNonRepeating']['guid']
    #     media_count = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('mediaCount',np.nan)
    #     flattened_record['media_count'] = float(media_count)
    #     media = record['content'].get('descriptiveNonRepeating', {}).get('online_media',{}).get('media',[])   
    #     if len(media):
    #         try: 
    #             flattened_record['media_id'] = media[0]['idsId']
    #         except KeyError:
    #             flattened_record['media_id'] = "N/A"

    #     topics = record['content'].get('indexedStructured',{}).get('topic',[])
    #     if len(topics):
    #         flattened_record['topics'] = '|'.join(topics)

    #     obj_set = record['content'].get('freetext',{}).get('setName',[])
    #     if len(obj_set):
    #         try:
    #             flattened_record['setName'] = obj_set[0]['content']
    #         except KeyError:
    #             flattened_record['setName'] = "N/A"


    #     if 'freetext' in record['content']:
    #         if 'name' in record['content']['freetext']:
    #             for name in record['content']['freetext']['name']:
    #                 if name['label'] == 'associated person':
    #                     flattened_record['associated person'] = name['content']

    #     return flattened_record