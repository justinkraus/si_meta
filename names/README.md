# Defining Culture
## Background
Methodology for preparing [three data visualizations](https://justinkraus.github.io/si_meta/) using the [Smithsonian’s Open Access](https://www.si.edu/openaccess) data as part of the Parson’s MSc Data Visualization Major Studio course. These visualizations were created primarily with data analysis in Python and visualized in Javascript.

## Process Overview
Highlevel process and tools used

**Obtaining Data** - AWS S3 bucket with Python (Dask and Pandas)

**Data Prep and Analysis** - Python (Pandas), Excel, Tableau, Gephi

**Visualization** - HTML and D3.js

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

### Final Data Pulls
The previous exploration enabled me to revisit my initial data pulls from the AWS S3 bucket around certain endpoints with better data populations. Essentially instead of pulling all available fields, I edited my script to only target fields with better data populations. While the overall metadata population at the time of these analyses isn't great for Smithsonian Open Access records, it was enough to work with for the data visualizations. Overview of these fields

#### [Example of accessing this data](https://github.com/justinkraus/siopenaccess/tree/master/saam_CL_python)

#### NMAH Names
[Data Profile of Records](https://justinkraus.github.io/si_meta/names/NMAH_Metadata_Profile.html)  
[NMAH Names Data Pull Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/nmah_names_datapull.py). 
Targets endpoints around names and categorical labels at the NMAH
1.3 million records  
Names: ~50% populated, 40k distinct  
Category: 100% populated, 200 distinct  

#### Cultural Topics
[Data Profile](https://justinkraus.github.io/si_meta/topics/SI_Combined_Profile.html)  
[Cultural Topics Data Pull Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_topics_datapull.py)  
Targets endpoints for topics tagged to items at Smithsonian Cultural Institutions (not natural history museums)  
2.1 million records  
Topics: ~50% populated, 86k distinct  

#### Decades of Culture
[Data Profile](https://justinkraus.github.io/si_meta/years/SI_Combined_Profile.html)  
[Decades of Culture Data Pull Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_years_datapull.py)  
Targets endpoints for dates of origination tagged to items at Smithsonian Cultural Institutions (not natural history museums)  
1.6 million records  
Dates: ~40% populated, 26k distinct  

## Data Prep and Analysis
#### Data Structuring
Topics had been concatenated into single fields, separated items to individual rows by splitting.  
[Data Structuring Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/names/nmah_pandas.py)  

#### Filtering
Objective of the analysis is to determine which people are associated with the most objects. As shown in the data profile above, the initial dataset includes non-person entities like companies and government agencies within the "name" endpoint. It appears there is a large portion of coins and other US currency within the collection. The primary filter of the analysis removes non-person entities by targeting items that did not contain a comma as all people had a comma separating first and last names. Additional entities removed through select keywords.  

Additional aggregation was done to bucket categorical classifications into more general groups shown in the final visualization, discussed through iteration process.  

#### Iteration 1
<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/names/siNames1.png" height="66%" width="75%">  

[Tableau Public Gallery](https://public.tableau.com/profile/justin.k7646#!/vizhome/NMAH_VIZ_1/Sheet12)  
Clearly work needs to be done to combine categories and standardize colors. An additional filter was implemented to remove people below the average item count of 5.

#### Iteration 2
<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/names/siNames2.png" height="66%" width="75%">  

[Tableau Public Gallery](https://public.tableau.com/profile/justin.k7646#!/vizhome/NMAH_Viz_1_topics_treemap/Dashboard1)  
Reflects more general categories but also realized the top and bottom portions of the graph aren't adding much value. Decided to focus on the packed bubble chart view for the final Iteration.  

#### Supplemental Info with Google Knowledge Graph
As the final visualization would focus on individuals, I decided to see what images I could get back from the Google Knowledge Graph API. The [Google Knowledge Graph](https://blog.google/products/search/introducing-knowledge-graph-things-not/) are the summary boxes shown for certain search results with information sourced from Wikipedia. As all of the individuals in this analysis represent some historical significance it seemed like a valid approach.  

[Google Knowledge API Script](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/names/google_knowledge_api.py)  

Effectively this script Google searches the names of individuals in my analysis and returns summary information and an image location. As shown in the final analysis, not a lot of images were returned, the most comprehensive results tended to be male politicians from recent times.

## Visualization
[Final Visual](https://justinkraus.github.io/si_meta/names/)  
D3 force directed bubble chart, additional work done to:
 - Improve the calculations of the X and Y positions
 - Add images to SVG's
 - Tooltip with hover over-info and links to Google Search and Smithsonian website

In the future I'd consider removing the animation entirely and embedding links within the webpage.