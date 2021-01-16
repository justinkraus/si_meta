
# Defining Culture - The Shape of Time
## Background
Methodology for preparing [The Shape of Time](https://justinkraus.github.io/si_meta/years/) using the [Smithsonian’s Open Access](https://www.si.edu/openaccess) data as part of the Parson’s MSc Data Visualization Major Studio course. This visualization explores when objects within the Smithsonian's Cultural Institutions were originated, i.e. created or used, by decade.

## Process Overview
Highlevel process and tools used

**Obtaining Data** - AWS S3 bucket with Python (Dask and Pandas)

**Data Prep and Analysis** - Python (Pandas), Excel, Tableau

**Visualization** - D3.js

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

[Python Script: Downloading files in S3 bucket with Dask](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_API_2.py)

As there are hundreds of the JSON files, I [flattened](https://github.com/amirziai/flatten) a sample of these files into tabular formats to understand which endpoints have metadata populations.

[Python Script: Flatten JSON to tabular structure](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/smithsonian_flatten.py)  
[Flat CSV Example](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/json_flatten_df_example.csv)

The CSV shows a portion of the files, but of note is that there are 500+ endpoints that could be accessed. Using this as a baseline for analysis was useful as it enabled me to get an understanding of which metadata records are maintained by the Smithsonian.

### Final Data Pull
The previous exploration enabled me to revisit my initial data pulls from the AWS S3 bucket around certain endpoints with better data populations. Essentially instead of pulling all available fields, I edited my script to only target fields with better data populations. While the overall metadata population at the time of these analyses isn't great for Smithsonian Open Access records, it was enough to work with for the data visualizations.  

[Raw Dataset Overview and Profile](https://justinkraus.github.io/si_meta/years/SI_Combined_Profile.html)  
[Python Script: Amazon S3 pull with specific endpoints](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/1_exploration/si_years_datapull.py)  
Targets endpoints for dates of origination tagged to items at Smithsonian Cultural Institutions (not natural history museums)  
1.6 million records  
Dates: ~40% populated, 26k distinct  

## Data Analysis and Structuring
### Data Analysis and Prep
With the raw data I set out to determine (1) if there are any observable patterns for each institution by decade; (2) who and what are the largest contributors to objects for each institution by decade. I did some data manipulation in this file:  
[Python Script: Data Standardization and Cleanup](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/years/analysis_script2.py)  

 - Extracts years from unstandardized date values in the original raw data
 - Groups those years by decade. 
 - Groups to determine the top 5 names and topics for each institution by decade
 - Concatenates those results to form [url patterns](https://github.com/justinkraus/si_meta/blob/master/years/text_array.js) for the clickable tooltip URLs.

Once this was done, I put the data into Tableau to see if there was a pattern across the years.

<img src="https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/years/tableauSIYears.png" height="66%" width="75%">  

[Tableau Public Gallery](https://public.tableau.com/profile/justin.k7646#!/vizhome/smithsonian_collections_years/Sheet1)  

Success! There is definitely a difference over the years. From here it is clear to see that the National Museum of American History has a significant majority of the total items in the Open Access collection. I revisited the earlier data standardization and cleanup script to normalize the values.

### Data Structuring for Ridgeline
Perhaps one of the most difficult data transformations I've needed to do, the [ridgeline plot](https://observablehq.com/@d3/ridgeline-plot) determines area plot size by frequency of the x-axis value. You can see in the [final csv](https://github.com/justinkraus/si_meta/blob/master/years/test.csv) this requires an unconventional structure where columns are the y-axis values and each cell contains an individually listed x-axis value. This structure is inefficient as we'd tend to aggregate these values into a high-level count when doing basic analysis.  

**Example of Final Data Structure**
|Archives of American Art| Cooper Hewitt, Smithsonian Design Museum |
|--|--|
| 1820 | 1680 |
| 1830 | 1690 |  

To accomplish this a series of crosstab, repivoting and groupby manipulations were done with pandas to convert the raw dataset to the final csv.  
[Python Script: Data Structure](https://github.com/justinkraus/si_meta/blob/master/pythonAnalysis/2_analysis/years/si_years_combine.py)  

## Visualization
The final visualization builds on a basic static ridgeline plot by adding interactivity:

 - On Hover with d3.select to highlight only that ridge area
 - Tooltip that contains the top names and topics with clickable URLs (see analysis section above)
 - d3 annotations to add observations from the analysis
 - Circle that traces the ridge outline

The final point took A LOT of adjusting for the final visual. D3 has many ways for [drawing a curve](http://bl.ocks.org/d3indepth/b6d4845973089bc1012dec1674d3aff8) some of which offer approximations to produce smoother results, however these don't necessarily intersect with the actual charted points. I've included two additional examples of options for calculating the curve [linear](https://justinkraus.github.io/si_meta/yearslinear/)  and [step basis](https://justinkraus.github.io/si_meta/yearsstep/).  

### Ridgeline Plot - Select Use only
I was set on using a ridgeline plot for this visual and as much as I like the final aesthetic it is something I'd probably advise against using in the future. The aforementioned data restructuring adds a considerable amount of time when using typical data sources. Additionally the overlapping aspect of the small multiple chart here is fine if the chart doesn't require interactivity, as the overlapping plots can interfere with each other. [Mike Bostock](https://twitter.com/mbostock/status/981961425454227461) shares this opinion and the horizon chart he suggests is less aesthetically appealing but more functional.