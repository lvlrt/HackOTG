if [ $( mount | grep urandom | wc -l ) -eq 0 ]; then
	sudo mount --bind /dev/urandom /dev/random
fi
sh /home/pi/hotspot_stop.sh
sudo hostapd /home/pi/hostapd.conf&
sudo dnsmasq -C /home/pi/dnsmasq.conf&
sleep 2
sudo ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
