"""
This class serves as the interface between the data selection CLI and the necessary
data collection APIS.
"""
import os
import json
import time
from abc import ABCMeta, abstractmethod
import pandas as pd


from requests import get
from matplotlib import pyplot as plot
import matplotlib.dates as dates

from alpha_vantage.timeseries import TimeSeries
from parameter import Parameter


class ICollector(metaclass=ABCMeta):
    """
    Simple interface to define basic functions.
    """
    def __init__(self, path_name):
        self.source = None
        self.path_to_raw = None
        self.path_to_processed = None
        self.csv_name = None
        self.name = path_name
        _ = self.__get_paths(path_name)
        self.params = Parameter.get_instance()

    def __get_paths(self, name):
        """
        Sets the paths to the raw and processed folders.
        Input should be a string similar to the naming in the res folder e.g 'pornhub'
        """
        # check if name object is string
        if isinstance(name, str):
            path_to_res = os.path.join('.', 'res')
            self.path_to_raw = os.path.join(path_to_res, str(name), 'raw')
            self.path_to_processed = os.path.join(path_to_res, str(name), 'processed')

            # create folders if they does not exist
            if not os.path.exists(self.path_to_raw):
                os.makedirs(self.path_to_raw)
            if not os.path.exists(self.path_to_processed):
                os.makedirs(self.path_to_processed)

        else:
            raise Exception('ICollector : get_paths name is no valid string')

        return self.path_to_raw, self.path_to_processed

    def __load_data(self):
        """
        Method loads the data from the raw folder if this file does
        not exist we can download the file from the internet.
        """
        # first we try to download the data
        # commented out since method wasn't implemented yet

        if not os.path.exists(self.path_to_raw):
            self.download_data()

        if os.path.exists(self.path_to_raw):
            frame = pd.read_csv(self.path_to_raw)
            frame = self.process_data(frame)
            frame.to_csv(self.path_to_processed, index=False)

        else:
            raise Exception('There is no {}'.format(self.path_to_raw))

    def get_data(self):
        """
        Method returns the processed frame saved in res/'name'/processed/???.csv
        """
        if not os.path.exists(self.path_to_processed) and not os.path.exists(self.path_to_raw):
            frame = self.download_data()
            frame.to_csv(self.path_to_raw)

        # first check if raw exist and processed not and handle this
        if not os.path.exists(self.path_to_processed) and os.path.exists(self.path_to_raw):
            self.__load_data()
            steam_frame = pd.read_csv(self.path_to_processed)

        # if the processed file exist we read it
        elif os.path.exists(self.path_to_processed):
            steam_frame = pd.read_csv(self.path_to_processed)

        else:
            raise Exception('There is no processed or raw file {} in  folder {}'.format(self.csv_name, self.name))

        return steam_frame

    def plot(self, frame):
        """
        Method plots the data to get a first impression
        """
        if not frame.empty:
            frame.plot(x_compat=True, kind='line', title=self.name)
            plot.gca().xaxis.set_major_locator(dates.DayLocator())
            plot.gca().xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))
            plot.show()

        else:
            raise Exception('plot frame is empty')

    @staticmethod
    def download_data():
        """
        Download data from API or somewhere else
        """
        # raise Exception('{} : load_data there is no raw data'.format(self.__class__.__name__))  # # noqa: F821
        return pd.DataFrame()

    @abstractmethod
    def process_data(self, frame_raw):
        """
        This is an abstract method!!
        Simple processing of the raw data e.g drop null values.
        Returns the processed dataframe.
        """
        raise NotImplementedError


class SteamCollector(ICollector):
    """
    Class handles the datacollection of the worldwide Steam data.
    Example sage:
    STEAM = SteamCollector()
    stframe = STEAM.get_data()
    STEAM.plot(stframe)
    """
    def __init__(self):
        ICollector.__init__(self, 'steam')  # add arguements if req
        self.source = None
        self.csv_name = 'steam_user_3y.csv'

        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        """
        Simple preprocessing of the steam dataset. Drop null values and set Date as index.
        """
        # set index & date
        frame_raw.columns = ['Date', 'Users', 'In-Game']
        frame_raw['Date'] = pd.to_datetime(frame_raw['Date'], utc=True)

        # drop rows with no entry
        frame_raw.dropna(subset=['Users', 'In-Game'], inplace=True)
        return frame_raw


class CovidCollector(ICollector):
    """
    Class that handels the collection of the Covid data
    """
    def __init__(self):
        ICollector.__init__(self, 'covid')  # add arguements if req
        self.source = 'https://corona-api.com/timeline'
        self.csv_name = 'covid.csv'
        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

        if not os.path.exists(self.path_to_raw):
            self.download_data()

    def download_data(self):
        """
        Download corona data from api
        """
        covid_request = get(self.source)
        if covid_request.status_code == 200:

            data = json.loads(covid_request.text)
            data = data['data']
            # frame = pd.json_normalize(covid_request.text['data'])
            frame = pd.json_normalize(data)
            _ = frame.to_csv(self.path_to_raw, index=False)
        else:
            raise Exception('Invalid request status code : {}'.format(covid_request.status_code))

    def process_data(self, frame_raw):
        """
        Processes the pandas data frame by converting to datetime and dropping columns.
        """
        frame_raw = frame_raw.drop(columns=['updated_at', 'is_in_progress'])
        frame_raw = frame_raw.rename(columns={"date": "Date"})
        frame_raw['Date'] = pd.to_datetime(frame_raw['Date'], utc=True)
        return frame_raw


class PornhubCollector(ICollector):
    """
    This Colector handles the collection, and simple preprocessing of the pornhub dataset.

    Example usage:
    PORN = PornhubCollector()
    frame = PORN.get_data()
    PORN.plot(frame)
    PORN.show()
    """
    def __init__(self):
        ICollector.__init__(self, 'pornhub')  # add arguments if req
        self.source = 'http://www.pornhub.com/insights/coronavirus-update'
        self.csv_name = 'World.csv'
        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        """
        Preprocessing of the pornhub dataset.transformation of 10% -> 0.1.
        Set Date as Index.
        Input is the raw data as pandas frame.
        Returns the preprocessed dataset as pandas frame.
        """
        frame_raw.columns = ['Date', 'Traffic_inc']
        frame_raw['Date'] = pd.to_datetime(frame_raw['Date'], utc=True)

        # convert 10% to 0.1
        frame_raw['Traffic_inc'] = frame_raw['Traffic_inc'].str.rstrip('%').astype('float') / 100.0
        return frame_raw


class PSCollector(ICollector):
    """
    This Colector handles the collection of Playstation data.

    Example usage :
    PS = PSCollector()
    ps_frame = PS.get_data()
    PS.plot(ps_frame)
    """
    def __init__(self):
        ICollector.__init__(self, 'playstation')
        self.source = ''
        self.csv_name = 'ps_players.csv'

        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        """
        Processing the Playstation data.
        Input is the raw data as pandas frame.
        Returns the preprocessed dataset as pandas frame.
        """
        frame_raw.columns = ['Date', 'PS3', 'PS4', 'Vita']
        frame_raw['Date'] = pd.to_datetime(frame_raw['Date'], utc=True)

        return frame_raw


class FinanceCollector(ICollector):
    """
    This Colector handles the collection of Finance data.
    We use alpha vantage API for data collection.
    Example usage :
    fi = FinanceCollector()
    fi_frame = PS.get_data()
    fi.plot(fi_frame)
    """
    def __init__(self):
        ICollector.__init__(self, 'finance')
        self.source = ''
        self.csv_name = 'finance.csv'

        self.path_to_raw = os.path.join(self.path_to_raw, self.csv_name)
        self.path_to_processed = os.path.join(self.path_to_processed, self.csv_name)

    def process_data(self, frame_raw):
        """
        Processing the finance data.
        Input is the raw data as pandas frame.
        Returns the preprocessed dataset as pandas frame.
        """

        return frame_raw

    def download_data(self):
        """
        Download finance data from alpha vantage api.
        Code : https://github.com/RomelTorres/alpha_vantage/blob/
        91a93e6c988ee716e1f20621078dd000f9808fd7/alpha_vantage/timeseries.py#L10
        """
        companies = self.params.stock_companies

        frame = pd.DataFrame()
        time_series = TimeSeries(key='B47RKHB1ATHXLQRT', output_format='pandas')
        start_date = self.params.start_date_data

        counter = 0

        # iterate over list and load data
        for company in companies:
            counter += 1
            procent = int(100*(counter/len(companies)))
            print('\rDownload {} stock data alreday finished {} %             '.format(company, procent), end="")
            time.sleep(16)

            try:
                # prepare the frame
                loaded_data, _ = time_series.get_daily(company,  # pylint: disable=unbalanced-tuple-unpacking
                                                       outputsize='full')  # pylint: disable=unbalanced-tuple-unpacking
                loaded_data = pd.DataFrame(loaded_data)
                loaded_data.reset_index(level=0, inplace=True)

                # set names, date select dates bigger start date
                loaded_data = loaded_data.loc[:, loaded_data.columns.intersection(['date', '1. open'])]
                loaded_data.columns = ['Date', str(company)]
                loaded_data = loaded_data[loaded_data['Date'] > start_date]

            except Exception as inst:  # pylint: disable=broad-except
                print('Error during downloading stock data {}'.format(inst))
                print('Problems downloading {}'.format(company))

            # merge data frames
            if frame.empty:
                frame = loaded_data
            else:
                frame = pd.merge(frame, loaded_data, how='left', on='Date')

        # transform data ('date' --> 'Date' in utc format
        frame['Date'] = pd.to_datetime(frame['Date'], utc=True)
        return frame


def tests():
    """
    Quick check if functionality working.
    """
    co_c = CovidCollector()
    ps_c = PSCollector()
    st_c = SteamCollector()
    fi_c = FinanceCollector()

    frame_list = []

    col_list = [co_c, ps_c, st_c, fi_c]
    for col in col_list:
        frame_list.append(col.get_data())


if __name__ == '__main__':
    tests()
