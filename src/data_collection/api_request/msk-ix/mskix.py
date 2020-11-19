"""!
@brief getting the raw data avgerage from MSKIX
@file MSKIX_AVG
@author Aron Endres
@date 20.06.2020
"""
import csv
import requests
# from bs4 import BeautifulSoup # pylint: disable=import-error

# Website
URL = 'https://www.msk-ix.ru/data/json/traffic/ix.all/yearly/?0.615278690833298'

# gettiing Website
source = requests.get(URL)

# save Website in json
result_dict = source.json()
# print(result_dict['AVERAGE'][0])

# save data in file
with open('mskix_avg.csv', 'w') as file_avg:
    csv.writer = csv.writer(file_avg)
    for line in result_dict['AVERAGE']:
        csv.writer.writerow(line)
