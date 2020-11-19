"""!@brief Twitch statistics processing file. Acquires raw data, processes it with pandas and saves it into csv files.
@details Data is obtained via the requests module from the twitch statistics page, parsed with BeautifulSoup and then
sorted into a pandas data frame.
@file Twitch stats preprocessing script file.
@author Martin Schuck
@date 26.6.2020
"""


from pathlib import Path, PurePath
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup


def get_twitch_stats():
    """!@brief Requests the HTML from the twitch stats website and parses it.

    Looks for all 'td' tags within the website, which contain the data for all stats available.
    @return Returns both the data points and the html as a text file.
    """
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    data_points = soup.find_all('td')
    return data_points, html.text


def read_twitch_stats():
    """!@brief Reads the HTML from the twitch stats raw folder and parses it.

    Looks for all 'td' tags within the website, which contain the data for all stats available.
    @return Returns both the data points and the html as a text file.
    """
    try:
        with open(PurePath.joinpath(PATH, 'raw', 'twitch_stats.html'), 'r') as f:
            html = json.load(f)
        soup = BeautifulSoup(html, 'html.parser')
        data_points = soup.find_all('td')
    except FileNotFoundError as error:
        print('Failed to execute data_management.twitch_processing.read_twitch_stats. No raw HTML saved in the folder.')
        print('Error message was: {}'.format(error))
        return None, None
    return data_points, html


def read_stats_to_pandas(data_points):
    """!@brief Reads the data points into a pandas data frame.

    @param data_points The unprocessed data points from the soup parsing.
    @return Returns a complete pandas data frame containing all stats.
    """
    data_dict = {'Date': [pd.to_datetime(date.text, utc=True) for date in data_points[0::5]],
                 'av_conc_viewers': [int(views.text) for views in data_points[1::5]],
                 'av_conc_channels': [int(channels.text) for channels in data_points[2::5]],
                 'time_watched': [(int(''.join(c for c in watch_time.text if c.isdigit())))
                                  for watch_time in data_points[3::5]],
                 'active_streamers': []
                 }
    for n_streamers in data_points[4::5]:
        if n_streamers.text == 'n/a':
            data_dict['active_streamers'].append(0)
        else:
            data_dict['active_streamers'].append(int(n_streamers.text))
    return pd.DataFrame(data_dict)


def save_raw_data(html):
    """!@brief Saves the raw HTML document to res/twitch/raw.

    File is saved as 'twitch_stats.html'.
    @param html The raw HTML as text.
    """
    with open(PurePath.joinpath(PATH, 'raw', 'twitch_stats.html'), 'w') as f:
        json.dump(html, f)


def save_processed_data(data_frame):
    """!@brief Saves the processed data frame to res/twitch/processed.

    File is saved as 'twitch_stats.csv'.
    @param data_frame The pandas data frame object.
    """
    data_frame.to_csv(PurePath.joinpath(PATH, 'processed', 'twitch_stats.csv').as_posix(),
                      encoding='utf-8', index=False)


def plot_data_frame(data_frame):
    """!@brief Plots the individual data columns of the data frame against the time axis.

    Creates 4 plots, one for each category. Uses the seaborne line plot.
    @param data_frame The pandas data frame object.
    """
    for key in ['av_conc_viewers', 'av_conc_channels', 'time_watched', 'active_streamers']:
        _, axis = plt.subplots(figsize=(10, 10))
        sns.lineplot(data_frame['Date'],
                     data_frame[key],
                     color='purple')
        axis.set(xlabel='Date',
                 ylabel=key,
                 title=key)
        plt.show()


def main():
    """!@brief Requests, processes and saves the data from twitchtracker.com.
    """
    print('Getting stats..')
    # data_points, html = get_twitch_stats()
    data_points, html = read_twitch_stats()
    if data_points is None:
        print('Error with data extraction. Exiting...')
        return
    print('Converting to data frame.')
    data_frame = read_stats_to_pandas(data_points)
    print('Saving data.')
    save_raw_data(html)
    save_processed_data(data_frame)
    print('Plotting data for inspection.')
    plot_data_frame(data_frame)


if __name__ == '__main__':
    PATH = PurePath.joinpath(Path(__file__).resolve().parents[2], 'res', 'twitch')
    URL = 'https://twitchtracker.com/statistics'
    main()
