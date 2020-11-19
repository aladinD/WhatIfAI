"""!
@brief getting the raw data max from Seattleix
@file SEATTLEIX_MAX
@author Aron Endres
@date 20.06.202
"""

import csv
import requests
from bs4 import BeautifulSoup  # pylint: disable=import-error

# getting Website
source = requests.get('https://www.seattleix.net/statistics/agg_max_daily.txt').text
soup = BeautifulSoup(source, 'lxml')

# save content
result = soup.p.text

# divide data to be saved
result = result.split('\n')

# save data in file
with open('seattleix_max.csv', 'w') as result_file:
    csv.writer = csv.writer(result_file, delimiter='\t')
    for line in result:
        csv.writer.writerow(line.split('\t'))
