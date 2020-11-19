# README for the Steam dataset

## Data origin
The data was downloaded from the [steam database website](https://steamdb.info/app/753/graphs/).

## Code for obtaining and preprocessing
The code can be found in the [SteamCollector](/src/data_management/data_collection.py) class.

## Data
The processed data contains the attributes :
  - Date
  - number of Users
  - number of players In-Game

We hope that the data will give us insight into the social behaviour of people. It can be assumed that the number of players will increase from the time of the lockdown. It is conceivable that the increase in players correlates with the number of unemployed. 