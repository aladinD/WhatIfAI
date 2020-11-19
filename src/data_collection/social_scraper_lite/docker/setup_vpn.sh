#!/usr/bin/expect
spawn nordvpn login
expect "sername:"
send "$env(USERNAME)\r"
expect "assword:"
send "$env(PASSWORD)\r"
expect "You can now connect to VPN by using 'nordvpn connect'."
expect eof
