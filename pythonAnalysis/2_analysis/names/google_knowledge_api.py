"""Example of Python client calling Knowledge Graph Search API."""
from __future__ import print_function
import json
import urllib
import urllib.request
import pandas as pd

#Import your text data to pandas dataframe for sentiment analysis
csv_data = pd.read_csv('nmah_names_d3.csv', encoding = 'utf-8')

#Create an empty list
output = []

for i in range(0,len(csv_data.index)): #loops through dataframe total rows
	Name = csv_data.loc[csv_data.index[i], 'Name']

	# api_key = open('.api_key').read()
	#NEED TO MOVE TO .env file before uploading to github!!!
	api_key = ''
	query = Name + "American"
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
	    'query': query,
	    'limit': 1,
	    'indent': True,
	    'key': api_key,
	    'types': 'Person'
	}
	url = service_url + '?' + urllib.parse.urlencode(params)
	print(url)
	response = json.loads(urllib.request.urlopen(url).read())
	for element in response['itemListElement']:
	  print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')
	  result = {
	  "name_orig": Name,
	  "name": element['result']['name'],
	  "brief_desc": element['result'].get('description'),
	  "image_url": element['result'].get('image', {}).get('contentUrl'),
	  "image_source": element['result'].get('image', {}).get('url'),
	  "detailed_desc": element['result'].get('detailedDescription', {}).get('articleBody'),
	  "desc_source": element['result'].get('detailedDescription', {}).get('url')
	  }
	  output.append(result.copy())
	  print(result)

df = pd.DataFrame(output) #save nested list to pandas data frame

df.to_csv('namh_names_output1.csv', encoding='utf-8')
