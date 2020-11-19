# README for the IX dataset

## Data origin
The data comes from the web pages of various IX providers that publicly provide their data throughput statistics. 
The list of IX points we tried to scrape can be found in the [IX list file](../../src/data_collection/api_request/ix_list.xlsx).

## Code for obtaining and preprocessing
The code for scraping and preprocessing can be found [here](../../src/data_collection/api_request/datapoint_collection.py). 

## Info about the dataset

- 20230 Data samples 
- Features
    - Timestamp
    - Date
    - bitrate
    - IX (Internet Exchange)
    - type (average or maximum)
- Only IX and type are categorical everything else is numeric
- Of every IX we have a time series of data flux 