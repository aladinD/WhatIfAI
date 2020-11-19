"""here goes the proxy"""

import os
import datetime as dt
import pandas as pd

from parameter import Parameter


class DataMerger():
    '''
    Class that handels the merging of the different Dataframes.
    '''
    def __init__(self):
        '''Constructor of DataMerger'''
        self.params = Parameter.get_instance()
        # make a list containing all paths to processed data
        folders = self.params.folders

        # join the paths structure ~ ./res/'folder_name'/processed
        path_to_res = os.path.join('.', 'res')
        self.path_to_processed = []

        for folder in folders:
            path = os.path.join(path_to_res, folder, 'processed')
            self.path_to_processed.append(path)

        # init other attributes
        self.frame = pd.DataFrame()

    def get_all_data(self, save_data=True):
        '''
        Method that merges all dataframes from res/processed/*
        @param save_data : Boolean value set True if you want to save the frame
        '''
        start = self.params.start_date_data
        end = self.params.end_date_data
        self.frame = get_date_frame(start, end)

        for folder in self.path_to_processed:
            dirs = os.listdir(folder)
            for file in dirs:
                if file.endswith('.csv'):
                    path_processed_data = os.path.join(folder, file)
                    try:
                        df_tmp = pd.read_csv(path_processed_data)
                        df_tmp['Date'] = pd.to_datetime(df_tmp['Date'], utc=True)
                        self.frame = self.frame.merge(df_tmp, how='left', on='Date')
                    except Exception as exep:  # pylint: disable=broad-except
                        print('Something is wrong with the data stored in {}'.format(path_processed_data))
                        print(exep)

        if save_data:
            path = os.path.join('.', 'res', 'all_raw.csv')
            self.frame.to_csv(path)

        return self.frame

    def get_all_paths(self):
        '''Returns all file paths where we read data from '''
        return self.path_to_processed


def get_date_frame(start, end):
    """ Generate list of all dates between start and end date"""
    date_list = [start + dt.timedelta(days=x) for x in range(0, (end - start).days)]
    frame = pd.DataFrame(date_list)
    frame.columns = ['Date']
    frame['Date'] = pd.to_datetime(frame['Date'], utc=True)
    return frame


def test():
    '''Dummy'''
    da_me = DataMerger()
    da_me.get_all_data()


if __name__ == '__main__':
    test()
