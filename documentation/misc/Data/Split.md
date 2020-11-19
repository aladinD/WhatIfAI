# Background
_____________________________________________________________________________________________________________________________________________________________________________________
As discussed within the ML readme, data is split into two separate sets:
- One pre-Covid-19 set, with the intent to predict baseline markers
- And one post Covid-19 set, with the intent to predict error margins

Both sets contain timeseries data on Covid-19 indicators and markers.


# Challenge
_____________________________________________________________________________________________________________________________________________________________________________________
The challenge with time series data is the inability to split data into a useful training/testing set.
This is due to the fact that learning time series data requires some form of process with memory.

As such, the datasets remain unsplit.