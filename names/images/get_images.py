import urllib
import urllib.request
import pandas as pd

#Import your text data to pandas dataframe for sentiment analysis
csv_data = pd.read_csv('nmah_names_imgs.csv', encoding = 'utf-8')

for i in range(0,len(csv_data.index)): #loops through dataframe total rows
	file_ID = csv_data.loc[csv_data.index[i], 'name_ID']
	url = csv_data.loc[csv_data.index[i], 'image_url']
	filename =  str(file_ID) + '.jpg'
	print(filename)

	urllib.request.urlretrieve(url, filename)

	print(file_ID)