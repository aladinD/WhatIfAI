"""!
@brief try to get data from AMS-IX
@file AMS-IX datacollection
@author Aron Endres
@date 20.06.2020
"""
import requests
from bs4 import BeautifulSoup  # pylint: disable=import-error

source = requests.get('https://www.ams-ix.net/ams/documentation/total-stats').text

soup = BeautifulSoup(source, 'lxml')

# match = soup.find('div',class_='highcharts-label highcharts-tooltip highcharts-color-undefined')
# match = soup.find('div',class_='sc-eLExRp dLrpSX')
match = soup.find('div', id='root')
match = match.find('div', class_='sc-eLExRp dLrpSX')
match = match.find('div', class_='sc-fjhmcy gAGeuq')
match = match.find('section', class_='sc-hjRWVT iezjix')
match = match.find_all('section', class_='sc-gZMcBi kGMETM')[6]
match = match.find('div', class_='sc-fgfRvd bxWvfX')
match = match.find('section', class_='sc-jeCdPy gcAPnO')
match = match.find('div', class_='sc-jtRlXQ cmuAPi')
match = match.find('div', class_='sc-kTUwUJ iqyaVk')
match = match.find('div', id='highcharts-rs10op6-48')

# match = match.find('div',id='highcharts-rs10op6-48')
# match = match.find('div',class_='highcharts-label highcharts-tooltip highcharts-color-undefined')
print(match)

# with open('test.txt','w') as file:
#     file.write(txt)
