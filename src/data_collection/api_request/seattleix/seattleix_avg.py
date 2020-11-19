"""!
@brief getting the raw data avgerage from Seattleix
@file SEATTLEIX_AVG
@author Aron Endres
@date 20.06.202
"""
import csv
import requests
from bs4 import BeautifulSoup  # pylint: disable=import-error

# Website
URL = 'https://www.seattleix.net/statistics/agg_avg_daily.txt'

# getting Website
source = requests.get(URL).text
soup = BeautifulSoup(source, 'lxml')

# save content
result = soup.p.text

# divde information to be saved
result = result.split('\n')

# test = result[0].split('\t')

# save data in file
with open('seattleix_avg.csv', 'w') as result_file:
    csv.writer = csv.writer(result_file, delimiter='\t')
    for line in result:
        csv.writer.writerow(line.split('\t'))
