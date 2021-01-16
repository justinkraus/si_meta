# Defining Culture - Cultural Connections
## Background
Methodology for preparing [Cultural Connections](https://justinkraus.github.io/si_meta/topics/) using the [Smithsonian’s Open Access](https://www.si.edu/openaccess) data as part of the Parson’s MSc Data Visualization Major Studio course. This visualization is an exploratory analysis around common topics tagged to items in the Smithsonian's cultural collections (collections excluding Natural History).

## Process Overview
Highlevel process and tools used

**Obtaining Data** - AWS S3 bucket with Python (Dask and Pandas)

**Data Prep and Analysis** - Python (Pandas), Gephi

**Visualization** - Gephi and Sigma.js

## Obtaining Data
The Smithsonian's Open Access data is information about objects in the collections of the 19 institutions that comprise the Smithsonian Institution group of museums. The data is in the form of both physical descriptors and supporting contextual information as well as digital images of the objects. 

There are multiple ways to access the Smithsonian's Open Access data. The most direct route is via API queries which functions similar to standard text search while enabling specification on certain endpoints (field names) within the Open Access dataset. The API is a functional solution for those with predefined searches to the dataset but as I was not previously familiar with the Smithsonian's data, I elected to take a different approach that would return all data available at the endpoints. 

### Access Amazon S3 Data Store with Dask
Through calls with the Smithsonian's data science team, I was made aware that the housed all data on an AWS S3 bucket. The S3 bucket organizes data by institution and stores data as line-delimited JSON files. As these files are managed by institution the data is not standardized, making for a high number of keys/fields. 

<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_aws_s3.png" height="25%" width="50%">

Combined with the large number of records for institution, processing the data was not possible with pandas (my preferred Python library). Dask was used to address this as it's [parallel processing](https://blog.dask.org/2017/01/24/dask-custom) is efficient for data of this type and it has [native support for accessing Amazon S3 buckets](https://docs.dask.org/en/latest/remote-data-services.html).

<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/grid_search_schedule.gif" height="66%" width="75%">  
Animated example of parallel processing from article above.

### Data Exploration
Initial explorations focused on understanding what metadata endpoints are available in the Smithsonian dataset. For the first visualization I looked at data available in the National Museum of American History (NMAH), this Python script downloads all of the NMAH JSON files available in the NMAH S3 bucket:

[Python Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_API_2.py)

As there are hundreds of the JSON files, I [flattened](https://github.com/amirziai/flatten) a sample of these files into tabular formats to understand which endpoints have metadata populations.

[Python Flatten Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_flatten.py)  
[Flat CSV Example](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/json_flatten_df_example.csv)

The CSV shows a portion of the files, but of note is that there are 500+ endpoints that could be accessed. Using this as a baseline for analysis was useful as it enabled me to get an understanding of which metadata records are maintained by the Smithsonian.

### Final Data Pull
The previous exploration enabled me to revisit my initial data pulls from the AWS S3 bucket around certain endpoints with better data populations. Essentially instead of pulling all available fields, I edited my script to only target fields with better data populations. While the overall metadata population at the time of these analyses isn't great for Smithsonian Open Access records, it was enough to work with for the data visualizations.  

[Dataset Profile](https://justinkraus.github.io/si_meta/topics/SI_Combined_Profile.html)  
[Cultural Topics Data Pull Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_topics_datapull.py)  
Targets endpoints for topics tagged to items at Smithsonian Cultural Institutions (not natural history museums)  
2.1 million records  
Topics: ~50% populated, 86k distinct  


## Data Prep and Analysis
