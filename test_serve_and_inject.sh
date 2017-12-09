sudo dnsspoof -i wlan0 port 53&
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 9000
