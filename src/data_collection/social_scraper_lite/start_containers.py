"""!@brief Script for starting Docker containers to work on specified work packages.

Docker containers are used to connect to a VPN, each with a different IP to avoid blocking by Cloudflare. Each container
scrapes the IPs defined in its respective work package. The precise location is assigned via the package ID argument.
The script starts all containers and exits. Results are written by the individual containers, health checks or progress
are not tracked and should be accessed by using the Docker dashboard.

@file Container spawner file.
@author Niklas Landerer
@date 25.6.2020
"""
import argparse
import os
import docker


PATH = os.path.abspath("")


def build_container(client):
    """!@brief Builds the docker image for the scraper containers.

    Build file and all necessary code is located in the docker subfolder.
    @param client The docker client obtained by calling docker.from_env().
    """
    client.images.build(path=os.path.join(os.path.abspath(""), "docker"), tag="scrape_light")


def start_container(client, work_package, load_saved):
    """!@brief Starts an individual container to scrape a work package.

    Wrapper around client.containers.run which adds the required arguments.
    @param client The docker client obtained by calling docker.from_env().
    @param work_package Package ID of the work package intended for the container.
    @param load_saved If set to true, will reload from quicksaves saved in the work package instead of from scratch.
    """
    package_path = os.path.join(PATH, "work_packages")

    client.containers.run(image="scrape_light",
                          environment=["PACKAGE="+work_package, "LOAD_FILE=" + load_saved,
                                       "USERNAME=patrick.kalmbach@tum.de", "PASSWORD=LA#kYs1#o:`Z"],
                          detach=True, tty=True, stdin_open=True,
                          sysctls={"net.ipv4.conf.all.rp_filter": 2},
                          privileged=True,
                          devices=["/dev/net/tun"],
                          name="scrape_" + str(work_package),
                          cap_add=["NET_ADMIN", "SYS_MODULE"],
                          volumes={package_path: {"bind": "/work_packages"}})


def main():
    """!@brief Main function of the script.

    Parses arguments, registers the client and starts containers for all jobs that were specified.
    """
    client = docker.from_env()
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--package_id', default='0',
                        help='provide id for the work package, comma separated if multiple')
    parser.add_argument('--load_quicksave', default="no", help='wanna load? -> yes/no')
    args = parser.parse_args()
    packages = args.package_id.split(",")
    print('Building docker container. This might take a while.')
    build_container(client)
    print('Build finished. Starting containers.')
    for package in packages:
        start_container(client, package, args.load_quicksave)
    print('Containers are running. Check Docker Dashboard for container health. Script will exit.')


if __name__ == "__main__":
    main()
