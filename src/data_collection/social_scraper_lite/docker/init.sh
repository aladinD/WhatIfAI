#!/usr/bin/bash
service nordvpn start
sleep 2
/usr/bin/expect /usr/bin/setup_vpn.sh
python3 /scraper/scrape.py
exec "$@"