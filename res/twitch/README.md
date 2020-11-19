# README for the Twitch statistics dataset


## Data origin
The data for this data set was scraped from [twitchtracker](https://twitchtracker.com/statistics), a website that tracks
statistics for number of viewers, total viewtime etc. We thought this data might be interesting as we expected a steep 
increase in live streaming due to the Corona crisis.


## Code for scraping
Scraping the data was pretty straightforward, as all of it could be scraped with a single request to the website.
The code for scraping is directly integrated into the processing of the data, see [Code for preprocessing](#Code-for-preprocessing).

## Code for preprocessing

Proprocessing was done by simply reading the raw data into a pandas frame. The website had exceptionally well managed data points, 
so there was no need to do extensive preprocessing.
The source code for preprocessing is located in the [twitch_processing.py](../../src/data_management/twitch_processing.py) file.