if [ $( mount | grep urandom | wc -l ) -eq 0 ]; then
	sudo mount --bind /dev/urandom /dev/random
fi
sh /home/pi/HackOTG/hotspot_stop.sh
sudo hostapd /home/pi/HackOTG/confs/hostapd.conf&
sudo dnsmasq -C /home/pi/HackOTG/confs/dnsmasq.conf&
sleep 2
sudo ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
