"""!@brief SBScaper class. Scrapes Socialblade for Youtube data.
@details Class gets used for all scraping requests to Socialblade. Error handling and IP masking has to be done
externally!
@file SBScaper class file.
@author Martin Schuck
@date 18.6.2020
"""


import threading
import time
import logging
import cloudscraper
from bs4 import BeautifulSoup
import js2xml

logging.basicConfig(level=logging.INFO)


class SBScraper:
    """!@brief SBScaper class to expose simple functions for scraping Socialblade data.

    This class is essentially a wrapper around the cloudscraper module fitted to the Socialblade Youtube section.
    Provides functions to get urls to all supported countries for the Socialblades Youtube section, all top 250
    channel urls of a given country url, and a function to scrape the data off a specific channel url. Also converts the
    scraped data from js into a usable format.

    @note Currently only supports Socialblade Youtube links.
    @see https://socialblade.com/
    """

    def __init__(self):
        self.request_thread = None
        self.html_response = False

    def get_all_country_urls(self, proxies=None):
        """!@brief Uses the Socialblade top 100 Youtube channel website to get the urls of all available countries
        top 250 channel lists.

        Country urls are constructed with the extracted ISO 3166 tags and not scraped directly!

        @param proxies Proxy to be used for the request. Used exactly as in pythons requests library.
        @return Returns the url list in case of success or False in case of failure.
        @warning Won't work anymore if Socialblade changes the structure of its country's top channels urls!
        """
        html_rsp = self._get_url_wrapper('https://socialblade.com/youtube/top/100', proxies=proxies)
        if not html_rsp:
            return False
        country_id_list = self._extract_country_ids(html_rsp)
        url_list = list()
        for country_id in country_id_list:
            url_list.append('https://socialblade.com/youtube/top/country/' + country_id)
        return url_list

    def get_channels_by_country(self, url, proxies=None):
        """!@brief Uses the provided url to scrape the links to all 250 top channels.

        Channel urls are constructed with the extracted channel names and not scraped directly!

        @param url url to the country's top 250 channels list.
        @param proxies Proxy to be used for the request. Used exactly as in pythons requests library.
        @return Returns a dictionary with the country ID as key and the list of urls as value in case of success or
        False in case of failure.
        @warning Won't work anymore if Socialblade changes the structure of its channel details urls!
        """
        country_id = url.split('/')[-1]  # The country id iso code is always last on sb country urls.
        html_rsp = self._get_url_wrapper(url, proxies=proxies)
        if not html_rsp:
            return False
        channel_list = self._extract_channels_from_sb_country(html_rsp)
        return {country_id: channel_list}

    def get_channel_data(self, url, proxies=None):
        """!@brief Uses the provided url to scrape the data of this specific channel.

        Channel website gets scraped with cloudscraper. The data itself is stored in several javascripts. Function calls
        a custom pipeline to convert js to xml and extract the data.

        @param url url to the channel's statistics page.
        @param proxies Proxy to be used for the request. Used exactly as in pythons requests library.
        @return Returns a dictionary with the table names as keys and the list of contents in case of success or
        False in case of failure.
        @note Some sites contain more tables than others. Dictionary will have variable length of elements, typically 4
        or 6. Might also have only 2 keys.
        @warning Won't work anymore if Socialblade changes the structure of its js nodes!
        """
        html_rsp = self._get_url_wrapper(url, proxies=proxies)
        if not html_rsp:
            return False
        data_dict = self._extract_channel_data(html_rsp)
        data_dict['channel_url'] = url
        return data_dict

    def _get_url_wrapper(self, url, proxies=None):
        """!@brief Wrapper for the _get_url function.

        _get_url results in most of the errors. Sometimes, requests also get stuck indefinitely. Wrapper starts a
        timeout to deal with this.
        @param url Url to scrape from.
        @param proxies Proxy to be used for the request. Used exactly as in pythons requests library.
        @return Returns the HTML page in case of success and False in case of failure.
        """
        self.request_thread = threading.Thread(target=self._get_url,
                                               kwargs={'url': url, 'proxies': proxies}, daemon=True)
        self.request_thread.start()
        t_start = time.time()
        t_diff = 0
        while self.request_thread.is_alive() and t_diff < 10:
            time.sleep(0.5)
            t_diff = time.time() - t_start
            # logging.info('Timeout running...')
        if t_diff >= 10:
            logging.info('### RAN INTO TIMEOUT ###')
            return False
        logging.info('Nominal execution')
        return self.html_response

    def _get_url(self, url, proxies=None):
        """!@brief Scrapes the specified url.

        Uses the cloudscraper module to scrape Socialblade despite Cloudflare protection. Cloudscraper imitates the
        required js response for accessing Socialblade. For more information,
        @see https://pypi.org/project/cloudscraper.
        The HTML document gets stored in self.html_response to transfer the web page to the wrapper.

        @param url url to the channel's statistics page.
        @param proxies Proxy to be used for the request. Used exactly as in pythons requests library.
        """
        scraper = cloudscraper.create_scraper()
        try:
            html_rsp = scraper.get(url, proxies=proxies).text
            if html_rsp is None:
                logging.info('Error in SBScraper._get_url with url %s and proxy %s.', url, proxies)
                logging.info('Web response had NoneType.')
                self.html_response = False
                return
            self.html_response = html_rsp
            return
        # General exception as there are lots of errors with cloudflare. Every exception is handled via return values.
        except Exception as err:  # pylint: disable=broad-except
            logging.info('Error in SBScraper._get_url with url %s and proxy %s.', url, proxies)
            logging.info('Error message was: %s', err)
            self.html_response = False
            return

    @staticmethod
    def _extract_country_ids(html_rsp):
        """!@brief Extracts all country IDs from an HTML string.

        Uses BeautifulSoup to identify all options with only 2 chars. All options on relevant Socialblade links are
        confirmed to be country IDs.

        @param html_rsp The website's HTML as a string.
        @return Returns the list of available country IDs.
        """
        soup = BeautifulSoup(html_rsp, 'html.parser')
        country_id_list = list()
        for option in soup.find_all('option'):
            c_id = option.get('value')
            # Only country ids have len 2 on this website. Filter out non values to avoid errors.
            if c_id is not None and len(c_id) == 2 and c_id not in country_id_list:
                country_id_list.append(c_id)
        return country_id_list

    @staticmethod
    def _extract_channels_from_sb_country(html_rsp):
        """!@brief Extracts all country's top 250 channel urls from an HTML string.

        Uses BeautifulSoup to identify all links. If the links contain the '/youtube/user' keyword, they are added to
        the list. Links are edited to directly access the detailed statistics page of a channel.

        @param html_rsp The website's HTML as a string.
        @return Returns the list of channel urls.
        """
        soup = BeautifulSoup(html_rsp, 'html.parser')
        channel_list = list()
        for link in soup.find_all('a'):
            url = link.get('href')
            if '/youtube/user/' in url:
                channel_list.append('https://socialblade.com' + url + '/monthly')  # Get the detailed statistics page.
        return channel_list

    def _extract_channel_data(self, html_rsp):
        """!@brief Extracts all channel statistics from an HTML string.

        Uses BeautifulSoup to identify all scripts. Filters the scripts until only the script containing the data
        for the graphs remains. Parses the script and zips all data into a data dictionary.

        @param html_rsp The website's HTML as a string.
        @return Returns the dictionary with processed table names as keys and the data as values.
        """
        soup = BeautifulSoup(html_rsp, 'html.parser')
        script = self._filter_scripts(soup.find_all('script'))
        data_dict = self._parse_js(script)
        return data_dict

    @staticmethod
    def _filter_scripts(scripts):
        """!@brief Filters the data script from a list of js scripts.

        A somewhat heuristic search. Data scripts are the largest script on the website. Therefore we filter the largest
        script and return it.

        @param scripts A list of scripts scraped from the website with BeautifulSoup.
        @return Returns the first script larger than 1000 chars.
        """
        top_idx = 0
        top_len = 0
        for idx, script in enumerate(scripts):
            if script.contents:  # Empty script entries have no contents attribute.
                if len(script.contents[0]) > top_len:
                    top_idx = idx
                    top_len = len(script.contents[0])
        return scripts[top_idx].contents[0] if scripts[top_idx].contents else False

    def _parse_js(self, script):
        """!@brief Parses a javascript for charts data.

        Converts js to a xml tree. Uses the highchart identifier and Socialblade's script structure to navigate to the
        relevant data. Also does basic processing on the data and keys.

        @param script A javascript as string.
        @return Returns a dictionary of all processed chart descriptions and their data.
        """
        if script:
            parsed = js2xml.parse(script)
            # Find all highchart identifiers and their data in the xml'ified js tree.
            categories = [c.xpath('./../../../../arguments/string')
                          for c in parsed.xpath("//identifier[@name='Highcharts']")]
            data = [d.xpath("./array/array/number/@value") for d in parsed.xpath("//property[@name='data']")]
            # Remove empty arrays from bad relative paths, access string content, strip unnecessary parts.
            categories = self._process_categories(categories)
            data = self._process_data(data)
            return dict(zip(categories, data))
        logging.info('INVALID DATA RETURNED')
        return {'Invalid_data': [0, 0]}

    @staticmethod
    def _process_categories(categories):
        """!@brief Processes the extracted categories.

        Removes empty category entries and strips unnecessary descriptions.

        @param categories List of raw extracted categories.
        @return Returns a list of processed and valid categories.
        """
        categories = [c[0].text for c in categories if c and 'graph' in c[0].text]
        for bad_str in ['graph-youtube-', '-container']:
            categories = [c.replace(bad_str, '') for c in categories]
        return categories

    @staticmethod
    def _process_data(data):
        """!@brief Processes the extracted data.

        Sometimes, the time axis of the arrays is decreasing instead of increasing. In this case, the whole data set
        gets reversed while keeping each time stamp at its respective data point.

        @param data List of raw extracted data.
        @return Returns a list of data ordered with increasing time scale.
        """
        for array in data:
            # Check if time is inverted. If so, reverse array while keeping the time/data structure.
            if array and len(array) > 2 and array[0] > array[2]:
                buff_1 = array[::2][::-1]
                buff_2 = array[1::2][::-1]
                array[::2] = buff_1
                array[1::2] = buff_2
        return data
