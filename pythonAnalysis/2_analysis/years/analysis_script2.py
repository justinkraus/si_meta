import pandas as pd


df = pd.read_csv("./si_combinedv1.csv")

print("done reading!")

print(df.info(verbose=True))

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
#convert decade to string without decimal
df_t['decade'] = df_t['decade'].astype(str).replace('\.0', '', regex=True)
# df_t['decade'] = (10 * (df_t['year_date'] // 10)).astype(str) + 's'

df_t = df_t.drop(columns=[
	'date',
	'year_regex',
	'dated',
	'year_date',
	'Unnamed: 0',
	'Unnamed: 0.1'])

#filter
#remove na's
df_t = df_t[df_t['decade'].notna()]
#remove smithsonian gardens
df_t = df_t[df_t['unitCode'] != 'HAC']

#for getting the n-largest by groups used function here: https://stackoverflow.com/questions/50028727/getting-the-n-largest-values-for-groups

#group and get top 10 names
#remove numbers and 
df_t['name_content'] = df_t['name_content'].str.replace('[^a-zA-Z ]', '')
#replace spaces with +
# df_t['name_content'] = df_t['name_content'].str.replace(' ', '%20')

#group and count items
df_n = df_t.groupby(['unitCode','decade','name_content']).size().to_frame('count').reset_index().sort_values(by=['count'],ascending=False)

#determine the 10 largest topics by unitcode and decade
df_n = df_n.groupby(['unitCode', 'decade']).apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)
# df_n = df_n.groupby(['unitCode', 'decade']).apply(lambda x: x.nlargest(5, 'count').sum()).reset_index(drop=True)
# df_n = df_n.groupby(['unitCode', 'decade']).agg({'name_content': 'sum'}).reset_index(drop=True)
## this is correct but not split
# df_n = df_n.groupby(['unitCode', 'decade'])['name_content'].sum()
##adds search url in front of name
df_n['name_url'] = '<a href="https://www.si.edu/search/all?edan_q=' + df_n['name_content'].astype(str) + '&edan_fq%5Bdate%5D=date%3A%22' + df_n['decade'].astype(str) + 's%22">' + df_n['name_content'] + '</a>'
df_n = df_n.replace({'unitCode': {'AAA': 'Archives of American Art', 
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

df_n = df_n.groupby(['unitCode', 'decade']).agg({'name_url': '<br/>'.join})


df_n.to_csv('agg_top_5_names_decade.csv')
print("done with aggregating names!")



#split topics
df_t['topics']=df_t['topics'].str.split("|")
df_t = df_t.explode('topics').reset_index(drop=True)

print(df_t['topics'].head(20))

#group and count items
df_g = df_t.groupby(['unitCode','decade','topics']).size().to_frame('count').reset_index().sort_values(by=['count'],ascending=False)

#determine the 10 largest topics by unitcode and decade
df_g = df_g.groupby(['unitCode', 'decade']).apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)

df_g['topic_url'] = '<a href="https://www.si.edu/search/all?edan_fq%5Btopic%5D=topic%3A%22' + df_g['topics'] + '%22&edan_fq%5Bdate%5D=date%3A%22' + df_g['decade'].astype(str) + 's%22&edan_fq%5Bunit_code%5D=unit_code%3A' + df_g['unitCode'] + '">' + df_g['topics'] + '</a>'
df_g = df_g.replace({'unitCode': {'AAA': 'Archives of American Art', 
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

df_g = df_g.groupby(['unitCode', 'decade']).agg({'topic_url': '<br/>'.join})

df_g.to_csv('agg_top_5_topics_decade.csv')
print("done with aggregating topics!")


# print(df_g.head(20))
# print(df_g.info(verbose=True))