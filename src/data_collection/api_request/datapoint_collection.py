"""!
@brief This class serves as data collection for different Datapoints.
It uses APIs and simple Webcrawling
@file Datapoint Collection preprocessing and raw
@author Max Putz, Aron Endres
@date 25.06.2020
"""

import csv
import os
import json
from datetime import datetime
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup  # pylint: disable=import-error

logging.basicConfig(level=logging.DEBUG)

# change the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# API URL
SIX_AVG_URL = 'https://www.seattleix.net/statistics/agg_avg_daily.txt'
SIX_MAX_URL = 'https://www.seattleix.net/statistics/agg_max_daily.txt'
MSKIX_URL = 'https://www.msk-ix.ru/data/json/traffic/ix.all/yearly/\
?0.615278690833298'
LINX_URL = "https://portal.linx.net/api/lans/throughput?start=\
1498305600000&end=1592990400000"
PEERING_CZ_URL = "https://web-api.peering.cz/graphql"
RESOURC_PATH = '../../../res/ix'
RESOURC_PATH_RAW = '../../../res/ix/raw'
RESOURC_PATH_PROC = '../../../res/ix/processed'


def get_six_avg_raw():
    """! @brief getting the data from SIX the average usage"""

    # getting data from website
    source_avg = requests.get(SIX_AVG_URL).text

    # data handler
    soup_avg = BeautifulSoup(source_avg, 'lxml')

    # get the data from the first paragraph
    result_avg = soup_avg.p.text

    # split the data into different days
    result_avg = result_avg.split('\n')

    # save results
    save_path = os.path.abspath(os.path.join(
        RESOURC_PATH, 'raw', 'seattleix_avg.csv'))
    with open(save_path, 'w') as result_file__avg:
        writer_avg = csv.writer(result_file__avg, delimiter='\t')
        for line in result_avg:
            writer_avg.writerow(line.split('\t'))


def get_six_max_raw():
    """! @brief getting the data from SIX the max usage"""

    # getting data from website
    source_max = requests.get(SIX_MAX_URL).text

    # data handler
    soup_max = BeautifulSoup(source_max, 'lxml')

    # get the data from the first paragraph
    result_max = soup_max.p.text

    # split the data into different days
    result_max = result_max.split('\n')

    # save results
    save_path = os.path.abspath(os.path.join(
        RESOURC_PATH, 'raw', 'seattleix_max.csv'))
    with open(save_path, 'w') as result_file_max:
        writer_max = csv.writer(result_file_max, delimiter='\t')
        for line in result_max:
            writer_max.writerow(line.split('\t'))


def get_mskix_raw():
    """! @brief getting data from MSK-IX Average and Max"""

    # getting data from website
    source = requests.get(MSKIX_URL)

    # data handler
    result_dict = source.json()

    # save average
    save_path = os.path.abspath(os.path.join(
        RESOURC_PATH, 'raw', 'mskix_avg.csv'))
    with open(save_path, 'w') as file_avg:
        avg_writer = csv.writer(file_avg, delimiter='\t')
        for line in result_dict['AVERAGE']:
            avg_writer.writerow(line)

    # save max
    save_path = os.path.abspath(os.path.join(
        RESOURC_PATH, 'raw', 'mskix_max.csv'))
    with open(save_path, 'w') as file_max:
        max_writer = csv.writer(file_max, delimiter='\t')
        for line in result_dict['MAX']:
            max_writer.writerow(line)


def get_raw():
    """! @brief is getting and saving all the raw data"""
    get_mskix_raw()
    get_six_avg_raw()
    get_six_max_raw()


def get_six_pre():
    """!
    @brief  This method is to standardize the datasets
            and add the feature of which datapoint it is
    @return preprocessed df
    """
    # get raw data
    df_six_avg = pd.read_csv(
        os.path.abspath(os.path.join(
            RESOURC_PATH, 'raw/seattleix_avg.csv')), sep='\t', header=0)
    df_six_max = pd.read_csv(
        os.path.abspath(os.path.join(
            RESOURC_PATH, 'raw/seattleix_max.csv')), sep='\t', header=0)

    # standardize header
    df_six_avg.columns = ['Timestamp', 'Date', 'bitrate']
    df_six_max.columns = ['Timestamp', 'Date', 'bitrate']

    # append IX
    df_six_avg['IX'] = 'six'
    df_six_max['IX'] = 'six'
    df_six_avg['type'] = 'avg'
    df_six_max['type'] = 'max'

    # delet last row
    df_six_avg.drop(df_six_avg.tail(1).index, inplace=True)
    df_six_max.drop(df_six_max.tail(1).index, inplace=True)

    # convert Timestamp
    df_six_avg = df_timestamp_floor(df_six_avg)
    df_six_max = df_timestamp_floor(df_six_max)

    # save preprocessed
    save_dataframe(path=RESOURC_PATH_PROC, name='seattleix_avg',
                   data=df_six_avg)
    save_dataframe(path=RESOURC_PATH_PROC, name='seattleix_max',
                   data=df_six_max)
    return df_six_avg, df_six_max


def get_mskix_pre():
    """!
    @brief This method is to standardize the datasets
            and add the feature of which datapoint it is
    @return preprocessed df
    """
    # get raw data
    df_mskix_avg = pd.read_csv(
        os.path.abspath(os.path.join(
            RESOURC_PATH, 'raw/mskix_avg.csv')), sep='\t', names=['Timestamp', 'bitrate'])
    df_mskix_max = pd.read_csv(
        os.path.abspath(os.path.join(
            RESOURC_PATH, 'raw/mskix_max.csv')), sep='\t', names=['Timestamp', 'bitrate'])

    # convert Timestamp
    # df_mskix_avg.iloc[:, 0] = df_mskix_avg.iloc[:, 0]/1000
    # df_mskix_max.iloc[:, 0] = df_mskix_max.iloc[:, 0]/1000

    # floor Timestamps
    df_mskix_avg = df_timestamp_floor(df_mskix_avg)
    df_mskix_max = df_timestamp_floor(df_mskix_max)

    # Gbit -> bit
    df_mskix_avg.iloc[:, 1] = df_mskix_avg.iloc[:, 1]*1e9
    df_mskix_max.iloc[:, 1] = df_mskix_max.iloc[:, 1]*1e9

    # ADD IX to feature
    df_mskix_avg['IX'] = 'mskix'
    df_mskix_max['IX'] = 'mskix'
    df_mskix_avg['type'] = 'avg'
    df_mskix_max['type'] = 'max'

    # Add feature Date
    df_mskix_avg.insert(1, "Date", 0)
    df_mskix_max.insert(1, "Date", 0)

    # get values of Date
    for idx, date in enumerate(df_mskix_avg['Timestamp']):
        df_mskix_avg.iloc[idx, 1] = datetime.fromtimestamp(date).date()
    for idx, date in enumerate(df_mskix_max['Timestamp']):
        df_mskix_max.iloc[idx, 1] = datetime.fromtimestamp(date).date()

    # save data
    save_dataframe(data=df_mskix_avg, name='mskix_avg', path=RESOURC_PATH_PROC)
    save_dataframe(data=df_mskix_max, name='mskix_max', path=RESOURC_PATH_PROC)
    return df_mskix_avg, df_mskix_max


def df_timestamp_floor(df_conv):
    """!
    @brief floor Timestamps
    @param dataframe that has Timestamps that should be converted
    @return preprocessed df
    """
    try:
        df_conv['Timestamp']
    except KeyError:
        logging.warning('Dataframe does not have a Feature called Timestamp. \n\
                        Return old Dataframe')
        return df_conv
    else:
        # select Timestamp conv. from float to pd.Timestamp
        for idx, stamp in enumerate(df_conv['Timestamp']):
            # stamp = pd.Timestamp.fromtimestamp(stamp)
            # stamp = stamp.floor(freq='D')
            if stamp > 1000000000000:
                stamp = pd.Timestamp(stamp, unit='ms')
                stamp = stamp.floor(freq='D')
                df_conv['Timestamp'][idx] = stamp.timestamp()
            else:
                stamp = pd.Timestamp(stamp, unit='s')
                stamp = stamp.floor(freq='D')
                df_conv['Timestamp'][idx] = stamp.timestamp()
            # logging.debug(pd.Timestamp(stamp, unit='s').date())
            # logging.debug(stamp)
    # logging.debug(df_conv['Timestamp'])
    return df_conv


def get_linx():
    """!
    @brief This method is to get from LINX
    @return preprocessed df
    """
    # get data from API
    response = get_request_json(LINX_URL)
    throughput = response['throughput']

    # create final Frame
    data_linx = pd.DataFrame()

    # get all datacentre in a list
    items = throughput.keys()

    # iterate through all datacentres
    for ix_x in items:

        # create pandasframe with all values
        ix_centre = throughput[ix_x]['bitrate']['in']
        data_new = pd.DataFrame(ix_centre,
                                columns=['Timestamp', 'bitrate'])
        data_new['IX'] = ix_x
        data_new['type'] = 'avg'

        # concat data from all datacentres
        data_linx = pd.concat([data_linx, data_new], ignore_index=True)

    # bring timestamps from millieseconds to seconds
    data_linx.iloc[:, 0] = data_linx.iloc[:, 0] / 1000

    # Add feature Date
    data_linx.insert(1, "Date", 0)

    # get values of Date
    for idx, date in enumerate(data_linx['Timestamp']):
        data_linx.iloc[idx, 1] = datetime.fromtimestamp(date).date()

    # save data
    save_dataframe(data_linx, 'linx', RESOURC_PATH_PROC)
    return data_linx


def get_peering_cz(start_time=1498305600, end_time=1592990400):
    """!
    @brief This method extracts data form peering.cz
    @param from when until when in Timestamp format in milliseconds
    @return saves and returns preprocessed data from linx datapoint
    """
    # intialise variables
    data_pee = pd.DataFrame()
    time_list = list()
    data_list = list()

    # get data from API
    body = json.dumps(
        {"operationName": "traffics", "variables": {"timestampRanges": [{"since": start_time, "until": end_time}]},
         "query": "query traffics($timestampRanges: [TimestampRangeInput!]!) \
         {\n  traffics(timestampRanges: $timestampRanges) \
         {\n    timestamp\n    traffic\n    __typename\n  }\n}\n"})
    response = requests.post(PEERING_CZ_URL, body)
    json_response = response.json()

    # prepair extracted dataset
    throughput = json_response['data']['traffics'][0]

    # fit dataset in pandasframe
    for x_throu in throughput:
        data_list.append(x_throu['traffic'])
        time_list.append(x_throu['timestamp'])
    data_pee = pd.DataFrame(list(zip(time_list, data_list)),
                            columns=['Timestamp', 'bitrate'])

    # Add missing features
    data_pee['IX'] = 'peering.cz'
    data_pee['type'] = 'avg'

    # Add feature Date
    data_pee.insert(1, "Date", 0)

    # get values of Date
    for idx, date in enumerate(data_pee['Timestamp']):
        data_pee.iloc[idx, 1] = datetime.fromtimestamp(date).date()

    # save data
    save_dataframe(data_pee, 'peering_cz', RESOURC_PATH_PROC)
    return data_pee


def get_ficix():
    """!
    @brief This method extracts data fro, the ficix csv
    @return saves and returns preprocessed data from linx datapoint
    """
    # read csv data
    data_ficix = pd.read_csv(
        os.path.abspath(os.path.join(
            RESOURC_PATH, 'raw/ficix.csv')), sep=',', names=['Timestamp', 'bitrate', 'del1', 'del2'])

    # delet unnessary data
    del data_ficix['del2']
    del data_ficix['del1']

    # convert Timestamp
    data_ficix.iloc[:, 0] = (data_ficix.iloc[:, 0] + 1)/1000

    # drop first row, since there are some artefacts from csv_read
    data_ficix.drop(data_ficix.head(1).index, inplace=True)

    # floor Timestamps
    data_ficix = df_timestamp_floor(data_ficix)

    # ADD IX to feature
    data_ficix['IX'] = 'ficix'
    data_ficix['type'] = 'avg'

    # Add feature Date
    data_ficix.insert(1, "Date", 0)

    # get values of Date
    for idx, date in enumerate(data_ficix['Timestamp']):
        data_ficix.iloc[idx, 1] = datetime.fromtimestamp(date).date()

# save data
    save_dataframe(data=data_ficix, name='ficix', path=RESOURC_PATH_PROC)
    return data_ficix


def create_date(concat):
    """!
    @brief Concat all pandaframes to output it as on big dataframe
    @param should be one dataframe put together (True) or seperated dataframes (False) be created
    """
    if concat:
        data_pee = get_peering_cz()
        data_linx = get_linx()
        data_mkix_avg, data_mkix_max = get_mskix_pre()
        data_six_avg, data_six_max = get_six_pre()
        data_ficix = get_ficix()
        data_all = pd.concat([data_linx, data_pee, data_mkix_avg, data_mkix_max, data_six_avg,
                              data_six_max, data_ficix], ignore_index=True)

        save_dataframe(data_all, 'all', RESOURC_PATH)
    else:
        get_peering_cz()
        get_linx()
        get_mskix_pre()
        get_six_pre()
        get_ficix()


def save_dataframe(data, name, path):
    """!
    @brief This method is to save the pandaframe.
    @param data dataframe that should be saved
    @param name under what name should the data be saved
    @param path where should the name be saved in absolute path
    """
    data.to_pickle(os.path.join(path, name + '.pkl'))
    data.to_csv(os.path.join(path, name + '.csv'), sep='\t')


def get_request_json(url):
    """!
    @brief This method makes "get" http request.
    @param url where to retrieve the data
    @return json response
    """
    response = requests.get(url)
    return response.json()


def main():
    """!
    This function is call Class method. So it is possible to generate dataset.
    """
    # create Dataset
    get_raw()
    create_date(concat=False)


if __name__ == '__main__':
    main()
