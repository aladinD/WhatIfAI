FROM ubuntu
LABEL maintainer "n.landerer@tum.de"

ENV PACKAGE package_num
ENV LOAD_FILE load_file
ENV USERNAME user
ENV PASSWORD pwd
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt install wget expect python3 gnupg2 -y
RUN wget -qnc "https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/nordvpn-release_1.0.0_all.deb" -O /tmp/nvpn.deb
RUN dpkg -i /tmp/nvpn.deb 
RUN rm -rf /tmp/nvpn.deb
RUN apt-get purge -y --auto-remove wget

RUN apt-get update && apt-get install python3-pip -y
RUN apt install nordvpn -y

RUN pip3 install --upgrade setuptools
RUN pip3 install cloudscraper pandas beautifulsoup4 js2xml requests

COPY init.sh /usr/bin
COPY setup_vpn.sh /usr/bin

COPY sb_scraper.py /scraper/sb_scraper.py
COPY scrape.py /scraper/scrape.py

RUN service nordvpn start

RUN chmod +x /usr/bin/init.sh
ENTRYPOINT ["/bin/bash", "/usr/bin/init.sh"]

