
# Defining Culture - Cultural Connections
## Background
Methodology for preparing [Cultural Connections](https://justinkraus.github.io/si_meta/topics/) using the [Smithsonian’s Open Access](https://www.si.edu/openaccess) data as part of the Parson’s MSc Data Visualization Major Studio course. This visualization is an exploratory analysis around common topics tagged to items in the Smithsonian's cultural collections (cultural collections are all Smithsonian museums excluding Natural History). The purpose of this is to better understand what types of subjects are in museums as well how objects of cultural significance are described.

## Process Overview
High-level process and tools used

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

[Python Script: download full JSON files in S3 bucket](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_API_2.py)

As there are hundreds of the JSON files, I [flattened](https://github.com/amirziai/flatten) a sample of these files into tabular formats to understand which endpoints have metadata populations.

[Python Script: Flatten](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_flatten.py)  
[Flat CSV Example](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/json_flatten_df_example.csv)

The CSV shows a portion of the files, but of note is that there are 500+ endpoints that could be accessed. Using this as a baseline for analysis was useful as it enabled me to get an understanding of which metadata records are maintained by the Smithsonian.

### Final Data Pull
The previous exploration enabled me to revisit my initial data pulls from the AWS S3 bucket around certain endpoints with better data populations. Essentially instead of pulling all available fields, I edited my script to only target fields with better data populations. While the overall metadata population at the time of these analyses isn't great for Smithsonian Open Access records, it was enough to work with for the data visualizations.  

[Dataset Profile](https://justinkraus.github.io/si_meta/topics/SI_Combined_Profile.html)  
[Python Script: download cultural topics with select endpoints](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_topics_datapull.py)  
Targets endpoints for topics tagged to items at Smithsonian Cultural Institutions (not natural history museums)  
2.1 million records  
Topics: ~50% populated, 86k distinct  


## Data Prep and Analysis
### Standardization - Library of Congress Classification
Topics tagged to objects at the Smithsonian are largely at the curators discretion, making for high-cardinality (uncommon or unique values) within the topics dataset. Through working with the Smithsonian I learned they leverage the [Library of Congress Classification](https://en.wikipedia.org/wiki/Library_of_Congress_Classification) where possible to standardize topics based on this classification hierarchy. Special thanks to the Smithsonian team for providing this information that allowed me to map some of the unique topics used by individual museums into more general values comparable across institutions.


<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/topics/locexample.jpeg" height="25%" width="50%">  
**Library of Congress Example Hierarchy**  
Shows high-level example of how specific topics map into higher-level topics,[image source](https://kimon.hosting.nyu.edu/physical-electrical-digital/items/show/1379).  

[Python Script: Standardize topics](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/topics/si_topics_standardize.py)  

### Restructuring by Topic
Knowledge graph's require two tables for visualizing: one which lists the nodes (circles) and a second that lists the edges (lines connecting each circle) between nodes. The second table is based on the graph theory concept of an [adjacency matrix](https://www.wikiwand.com/en/Adjacency_matrix), a basic example shown here:

<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/topics/adjMatrix.jpeg" height="66%" width="75%">  
[source](https://www.geeksforgeeks.org/graph-and-its-representations/)  
The table on the right defines if a line occurs between each node, a version of this is needed to visualize in gephi.

As the initial dataset is structured around museums and objects with corresponding topic tags, there was no relationships connecting the topics. To define the relationships between topics, the data needed to be restructured so that topics were the primary focus and museums defined the relationships.
**Initial Dataset**
| Museum |Topic  |
|--|--|
|Museum#1|Topic#1|
|Museum#2|Topic#1|

**Restructured Dataset**
| Topic | Source| Target |
|--|--|--|
|Topic#1|Museum#1 | Museum#2|

I used Pandas to accomplish this, essentially grouping by topics and adding columns for each museum as a source and target for line. The python script to accomplish this is found here:

[Python Script: filter and restructure data](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/topics/si_topics_structure.py)  

## Visualization
[Gephi](https://gephi.org/) was used to position and style the network graph. In each of these select earlier iterations its easy to see the split of distinct smaller topics used only by an individual institution versus the larger topics present at multiple. 
**Early Iteration**  
<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/topics/deathstar.png" height="66%" width="75%">  
The [final version](https://justinkraus.github.io/si_meta/topics/) was exported to a standalone html and javascript  page with [sigma.js](http://sigmajs.org/).
