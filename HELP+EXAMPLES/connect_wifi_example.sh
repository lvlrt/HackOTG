sh /home/pi/HackOTG/hotspot_stop.sh
sudo wpa_supplicant -B -i wlan0 -D wext -c example.conf
sudo dhcpcd --nohook wpa_supplicant wlan0
