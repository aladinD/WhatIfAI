"""!
@brief getting the raw data max from MSKIX
@file MSKIX_MAX
@author Aron Endres
@date 20.06.2020
"""
import csv
import requests
# from bs4 import BeautifulSoup # pylint: disable=import-error

# Website
URL = 'https://www.msk-ix.ru/data/json/traffic/ix.all/yearly/?0.615278690833298'

# get Website
source = requests.get(URL)

# save website in json
result_dict = source.json()
# print(result_dict['AVERAGE'][0])

# save raw in file
with open('mskix_max.csv', 'w') as file_max:
    csv.writer = csv.writer(file_max)
    for line in result_dict['MAX']:
        csv.writer.writerow(line)
