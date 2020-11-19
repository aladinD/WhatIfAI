"""!@brief Main script for scraping from Socialblade.

To get as much data as possible from the website, we look for the top 250 channels in more than 240 available
country options for a total of > 60.000 channels. These channels are the most successful ones in their respective
country, so we assume the data to be representative of the countries Youtube activities.

First, the scraper gets all available country top channel urls and assembles work packages from the results. Then docker
containers are used to connect to a VPN, each with a different IP to avoid blocking by Cloudflare. Each container gets
a work package assigned. Once all containers finished scraping for the urls of the top 250 channels per country, new
work packages are created and again assigned to docker containers with random IPs. After completion of all tasks, the
data gets assembled into a single data file.

@file Scrape main script file.
@author Niklas Landerer
@author Martin Schuck
@date 18.6.2020
"""

import json
import os
import time
import random
import requests
from sb_scraper import SBScraper


def load_channel_urls(package_id):
    """!@brief Loads the channel urls from the package directory.

    @param package_id ID of the work package. Specifies the folder to load.
    @return Returns the list of channel urls saved in the job.
    """
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    with open(os.path.join(work_package_path, 'job.json'), 'r') as f:
        channel_url_list = json.load(f)
    return channel_url_list


def load_quicksave(package_id):
    """!@brief Loads a quicksave from the package directory.

    @param package_id ID of the work package. Specifies the folder to load.
    @return Returns the quicksave dictionary.
    """
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    with open(os.path.join(work_package_path, 'quicksave.json'), 'r') as f:
        save = json.load(f)
    return save


def clear_dictionary(package_id):
    """!@brief Clears all files from the package directory.

    @param package_id ID of the work package. Specifies the folder to load.
    """
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    for filename in ['results.json', 'quicksave.json']:
        if os.path.isfile(os.path.join(work_package_path, filename)):
            os.remove(os.path.join(work_package_path, filename))


def write_results(results, package_id):
    """!@brief Writes the results to the package directory.

    @param results The result array that is to be saved.
    @param package_id ID of the work package. Specifies the folder to load.
    """
    with open(os.path.join(PATH, 'work_packages', 'package_' + str(package_id), 'results.json'), 'w') as f:
        json.dump(results, f)


def quicksave(channel_url_list, results, package_id):
    """!@brief Stores a quicksave to the package directory.

    @param channel_url_list The list of still unhandled urls.
    @param results The results array that was assembled so far.
    @param package_id ID of the work package. Specifies the folder to load.
    """
    save = {'channel_url_list': channel_url_list,
            'results': results}
    with open(os.path.join(PATH, 'work_packages', 'package_' + str(package_id), 'quicksave.json'), 'w') as f:
        json.dump(save, f)


def change_vpn(server):
    """!@brief Changes the connections VPN server.

    @warning We use NordVPN for our connection. This function will only work with the correct NordVPN setup and
    installations.

    @param server The NordVPN server address to connect to as string.
    """
    os.system('nordvpn disconnect')
    server = server.split('.')[0]
    os.system('nordvpn connect ' + server)


def get_vpn_servers():
    """!@brief Loads a list of available NordVPN servers.

    Server list is filtered to only include servers below 50% capacity and shuffled.

    @return Returns a list of available servers.
    """
    req = requests.get("https://api.nordvpn.com/v1/servers?limit=10000")  # Set limit to get more than 100 servers.
    vpn_list = []
    for server in req.json():
        if server["load"] < 50:
            vpn_list.append(server["hostname"])
    random.shuffle(vpn_list)
    print('VPN Server list has length: {}'.format(len(vpn_list)))
    return vpn_list


def main():
    """!@brief Main function of the docker scrape script.

    Uses the environment variables to scrape the assigned work package and takes care of scraping error handling.
    Scraping is done with quicksaves to be able to continue the work in case an unforeseen error appears.
    """
    if LOAD_SAVE:
        save = load_quicksave(PACKAGE_ID)
        channel_url_list = save['channel_url_list']
        results = save['results']
    else:
        channel_url_list = load_channel_urls(PACKAGE_ID)
        results = list()
    clear_dictionary(PACKAGE_ID)

    sb_scraper = SBScraper()
    # Connect to VPNs to avoid getting blocked by cloudflare.
    vpn_server_list = get_vpn_servers()
    while not vpn_server_list:
        vpn_server_list = get_vpn_servers()
    change_vpn(vpn_server_list.pop())

    tot_len = len(channel_url_list)
    it_cnt = 1
    err_cnt = 0
    while channel_url_list:
        channel_url = channel_url_list.pop()
        channel_data = sb_scraper.get_channel_data(channel_url)
        if not channel_data:
            print('### WARNING: SCRAPING CHANNEL FAILED ###')
            err_cnt += 1
            if err_cnt < 25:  # In case a bad link was passed, give up parsing after 25 tries.
                channel_url_list.append(channel_url)
            else:
                err_cnt = 0
            while not vpn_server_list:
                vpn_server_list = get_vpn_servers()
            change_vpn(vpn_server_list.pop())
            time.sleep(random.uniform(1., 2.))
        else:
            err_cnt = 0
            print('Scraping at {:.2f}%'.format((1 - len(channel_url_list)/tot_len)*100))
            results.append(channel_data)
        if not it_cnt % 50:
            print('Quicksaving...')
            quicksave(channel_url_list, results, PACKAGE_ID)
        it_cnt += 1
    if results:
        write_results(results, package_id=PACKAGE_ID)
    print('##################################')
    print('###  Finished working package  ###')
    print('### The scraper will now close ###')
    print('##################################')
    time.sleep(1)


if __name__ == '__main__':
    PATH = "/"
    PACKAGE_ID = os.environ['PACKAGE']
    LOAD_SAVE = os.environ['LOAD_FILE'] == "yes"
    main()
