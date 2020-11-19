# README for the Playstation dataset

## Data origin
The data was downloaded from the [gamestat website](https://gamstat.com/playstation/).

## Code for preprocessing
The code can be found in the [data collection file](/./src/data_management/data_collection.py) in the PSCollector class.

## Data structure
The processed data contains the attributes :
  - Date
  - number of PS3 players
  - number of PS4 players
  - number of Vita players

The number of daily Playstation players almost doubled from 9 March (88.09K players) to 24 March 2020 (168.29K) This is pretty much the start of the lockdown. We suspect that this high increase is related to the Corona related layoffs.