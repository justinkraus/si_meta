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


#create combined df with just museum and date
df = pd.read_csv("./si_combined.csv")
print("done reading!")

df = df.drop(columns=[
				'record_ID',
				'title_sort',
				'identifier',
				'guid',
				'object_type',
				'medium'])
print("done dropping!")

# #data frame info
print(df.info(verbose=True, null_counts=True))

# df_g =df.groupby(['name_label','name_content','date','setName']).size().sort_values(ascending=False)

#split date into individual rows
df['date']=df['date'].str.split("|")
df_t = df.explode('date').reset_index(drop=True)
print(df_t['date'].head(20))

#date conversions
df_t['date'] = df_t['date'].str.rstrip('s')
#regex to extract first 4 digits (year)
df_t['year_regex'] = df_t['date'].str.extract(r'(\b\d{4}\b)')

# df_t.to_csv('pre_dates.csv', mode='a')

#datetime conversions
df_t['dated'] = pd.to_datetime(df_t['year_regex'], infer_datetime_format=True, errors='coerce')
# ##convert date to year
df_t['year_date'] = df_t['dated'].dt.year

#convert year to decade
df_t['decade'] = (10 * (df_t['year_date'] // 10))
# df_t['decade'] = (10 * (df_t['year_date'] // 10)).astype(str) + 's'

df_t = df_t.drop(columns=[
	'setName',
	'date',
	'year_regex',
	'dated',
	'year_date',
	'Unnamed: 0'])

#filter
#remove na's
df_t = df_t[df_t['decade'].notna()]
#remove smithsonian gardens
df_t = df_t[df_t['unitCode'] != 'HAC']
#map new unit code name values
df_t = df_t.replace({'unitCode': {'AAA': 'Archives of American Art', 
'ACAH': 'Archives of American History', 
'ACM': 'Anacostia Community Museum', 
'CFCHFOLKLIFE': 'Ralph Rinzler Folklife Archives and Collections', 
'CHNDM': 'Cooper Hewitt, Smithsonian Design Museum', 
'FBR': 'Smithsonian Field Book Project', 
'FSA': 'Freer Sackler Archives', 
'FSG': 'Freer Gallery of Art and Arthur M Sackler Gallery', 
'HAC': 'Smithsonian Gardens', 
'HMSG': 'Hirshhorn Museum and Sculpture Garden', 
'HSFA': 'Human Studies Film Archives', 
'NAA': 'National Anthropological Archives', 
'NASM': 'National Air and Space Museum', 
'NMAAHC': 'National Museum of African American History and Culture', 
'NMAfA': 'National Museum of African Art', 
'NMAH': 'National Museum of American History', 
'NMAI': 'National Museum of the American Indian', 
'NPG': 'National Portrait Gallery', 
'NPM': 'National Postal Museum', 
'SAAM': 'Smithsonian American Art Museum', 
'SIA': 'Smithsonian Institution Archives', 
'SIL': 'Smithsonian Libraries', 
}})

print(df_t.head(20))

# good overview on crosstabs maniupulation here: 
# https://dfrieds.com/data-analysis/crosstabs-python-pandas.html
# https://stackoverflow.com/questions/42371655/how-to-calculate-of-row-and-of-column-for-a-python-pivot-with-row-and-column

df_pivot = pd.crosstab(df_t.decade, df_t.unitCode, normalize='columns').applymap(lambda x: "{0:.0f}".format(100*x))

print(df_pivot)

#stack the normalized data into two columns and then repeat the index values (decade) based on the normalized frequencies
#answer from here: https://stackoverflow.com/questions/57861649/reverse-a-cross-tabulation-or-frequency-table
s = df_pivot.stack()
df_repeat = s.index.repeat(s).to_frame().reset_index(drop=True)

print(df_repeat)

#pivot to re-add unitcode as columns
#https://stackoverflow.com/questions/40327503/pandas-how-to-create-simple-cross-tab-without-aggregation
df_repivot = df_repeat.pivot(columns = 'unitCode', values ='decade')
print(df_repivot)

#drop NA's, move cells up 
#https://stackoverflow.com/questions/43119503/how-to-remove-blanks-nas-from-dataframe-and-shift-the-values-up
df_repivot_nas = df_repivot.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
print(df_repivot_nas)

df_repivot_nas.to_csv('test.csv')
# #sensible groupby
# df_g = df_t.groupby(['unitCode','decade']).size().to_frame('count').reset_index().sort_values(by=['count'],ascending=False)
#grouby for ridgeline data
df_g = df_t.groupby(['unitCode','decade']).size().to_frame('count').reset_index().sort_values(by=['count'],ascending=False)
#dataframe reshape where unitCode is the column taken from:
#https://stackoverflow.com/questions/39323002/convert-pandas-groupby-group-into-columns
df_gg = df_g.set_index(['unitCode','decade']).unstack(level=0)

print("done grouping!")
