"""!@brief Script to create work packages for the Docker containers.

Scrapes all available countries from Socialblade, then also scrapes the respective top 250 channel lists from the site.
Reads the user input on how many work packages should be created, splits the link list accordingly and creates the
necessary folders.
@file Work packages creator script file.
@author Martin Schuck
@date 25.6.2020
"""

import json
import os
import math
import time
import glob
import random
import shutil
from sb_scraper import SBScraper


PATH = os.path.join(os.path.abspath(""))


def assemble_work_packages(url_list, n_packages):
    """!@brief Assembles a list of URLs into work packages.

    Work packages are saved at work_packages/package_xx.
    @param url_list List of url strings that have to be scraped.
    @param n_packages Number of packages to divide the url list into.
    """
    shutil.rmtree(os.path.join(PATH, 'work_packages'))
    package_size = math.ceil(len(url_list) / n_packages)
    work_packages = [url_list[x:x + package_size] for x in range(0, len(url_list), package_size)]
    for idx, package in enumerate(work_packages):
        os.makedirs(os.path.join(PATH, 'work_packages', 'package_' + str(idx)))
        with open(os.path.join(PATH, 'work_packages', 'package_' + str(idx), 'job.json'), 'w') as f:
            json.dump(package, f)
    with open(os.path.join(PATH, 'work_packages', 'results.json'), 'w') as f:  # Save the deleted results file again.
        json.dump(url_list, f)


def load_country_results(result_file='results.json'):
    """!@brief Loads the list of countries available on socialblade from a json file.

    @param result_file Filename of the save file located under work_packages.
    @return Returns the list of list of all country main page urls for socialblade.
    """
    channel_url_list = list()
    with open(os.path.join(PATH, 'work_packages', result_file), 'r') as f:
        country_list = json.load(f)
        for country_dict in country_list:
            for key in country_dict.keys():
                channel_url_list.extend(country_dict[key])
    return channel_url_list


def clear_dictionaries():
    """!@brief Clears all dictionaries below the work packages folder.
    """
    work_packages_path = os.path.join(PATH, "work_packages")
    for directory in [d for d in os.listdir(work_packages_path) if os.path.isdir(os.path.join(work_packages_path, d))]:
        r_files = glob.glob(os.path.join(work_packages_path, directory) + '/*')
        for f in r_files:
            print(f)
            os.remove(f)
        os.rmdir(os.path.join(work_packages_path, directory))
    r_files = glob.glob(os.path.join(work_packages_path, '*'))
    for f in r_files:
        os.remove(f)


def show_dialogue(dialogue_nr=0):
    """!@brief Prints dialogue options to the console and processes input.

    Dialogue options are called via their dialogue number. Convenient way to store all prints into a single function.
    @param dialogue_nr Number of the dialogue and input check to perform.
    @return Returns the parsed and processed user input. Differs in between different dialogue numbers.
    """
    if dialogue_nr == 0:
        print('##########################################################')
        print('###   You are about to assemble new working packages   ###')
        print('### ALL DATA IN THE WORK PACKAGES FOLDERS WILL BE LOST ###')
        print('###               Please confirm! (yes/no)             ###')
        print('##########################################################')
        rsp = (input().lower() == 'yes')
        if rsp:
            print('\n##########################################################')
            print('###                    Confirmed                       ###')
            print('##########################################################')
        else:
            print('\n##########################################################')
            print('###                     Aborted                        ###')
            print('##########################################################')
        return rsp
    if dialogue_nr == 1:
        print('########################################')
        print('###      Finished country scrape     ###')
        print('###  Create new packages (yes/no)?   ###')
        print('########################################')
        rsp = (input().lower() == 'yes')
        if rsp:
            print('\n##########################################################')
            print('###                    Confirmed                       ###')
            print('##########################################################')
        else:
            print('\n##########################################################')
            print('###                     Aborted                        ###')
            print('##########################################################')
        return rsp
    if dialogue_nr == 2:
        print('##################################################################')
        print('### Enter the number of working packages do you want to create ###')
        print('##################################################################')
        rsp = int(input())
        return rsp
    return False


def write_fails(fails):
    """!@brief Writes a list of urls into a fails.json file.

    @param fails List of failed urls."""
    with open(os.path.join(PATH, 'work_packages', 'fails.json'), 'w') as f:
        json.dump(fails, f)


def write_results(results):
    """!@brief Writes dictionary of results into a results.json file.

    @param results Result dictionary to write."""
    with open(os.path.join(PATH, 'work_packages', 'results.json'), 'w') as f:
        json.dump(results, f)


def main():
    """!@brief Main function for the script.

    Controls the dialogue flow, sets parameters accordingly, starts the scraping and saves the results and fails into
    the respective files.
    """
    confirm = show_dialogue(dialogue_nr=0)
    if confirm:
        clear_dictionaries()

        failed_urls = list()
        results = list()

        sb_scraper = SBScraper()
        country_url_list = sb_scraper.get_all_country_urls()
        tot_len = len(country_url_list)
        while country_url_list:
            country_url = country_url_list.pop()
            country_channels = sb_scraper.get_channels_by_country(country_url)
            if not country_channels:
                print('### WARNING: SCRAPING COUNTRY FAILED ###')
                failed_urls.append(country_url)
            else:
                print('Scraping at {:.2f}%'.format((1 - len(country_url_list) / tot_len) * 100))
                results.append(country_channels)
            time.sleep(random.uniform(2., 3.))
        if failed_urls:
            write_fails(failed_urls)
        if results:
            write_results(results)
    confirm = show_dialogue(dialogue_nr=1)
    if confirm:
        channel_urls = load_country_results()
        n_packages = show_dialogue(dialogue_nr=2)
        assemble_work_packages(channel_urls, n_packages=n_packages)
        print('Working packages assembled.')


if __name__ == '__main__':
    main()
