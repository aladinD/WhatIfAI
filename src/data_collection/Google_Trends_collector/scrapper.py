"""!@brief scrapper script. gets the Google Trends Data for certain keywords.
@author HEnrique Frutuoso
@date 24.6.2020
"""

import os
from pytrends.request import TrendReq
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()


def get_keywords(keywords_file):
    """
    !@brief Opens and extracts the keywords to search for in the keywords.txt
    @param name of the file to search for
    @return Returns the keywords as a list
    """
    kw_file = open(keywords_file)
    keywords = []
    for line in kw_file:
        # "#" are supposed to be comments on txt file
        if line[0] != '#':
            keywords.append(line[:-1])
    print(keywords)
    return keywords


def get_interest_over_time(kw_list):
    """
    !@brief Uses the Pytrends library to search for the keywords
    saves the in a csv file in pandas dataframe format
    @param  A list with all the keywords to search for
    @return Saves the data in csv file for each keyword
    """
    pytrend = TrendReq()
    # Interest by Region
    counter = 1

    for keyword in kw_list:
        pytrend.build_payload(kw_list=[keyword])
        trends_df = pytrend.interest_over_time()
        trends_df.index.names = ["Date"]
        trends_df.drop("isPartial", 1, inplace=True)
        trends_df.index = pd.to_datetime(trends_df.index, utc=True)
        trends_df.to_csv("{}/Data/{}.csv".format(dir_path, keyword))
        counter += 1


def get_data():
    """
    !@brief Run to get all the data and save them into a csv
    @param  None
    @return None
    """
    kw_list = get_keywords("{}/keywords.txt".format(dir_path))
    get_interest_over_time(kw_list)
