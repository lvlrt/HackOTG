if [ $( mount | grep urandom | wc -l ) -eq 0 ]; then
	sudo mount --bind /dev/urandom /dev/random
fi

sh /home/pi/HackOTG/hotspot_stop.sh

if [ -z "$1" ] 
then
	sudo hostapd /home/pi/HackOTG/confs/hostapd.conf&
else
	echo 'interface=wlan0\nssid='$1'\nhw_mode=g\nchannel=6\nauth_algs=1\nwmm_enabled=0\n' > /home/pi/HackOTG/confs/hostapd_open.conf
	sudo hostapd /home/pi/HackOTG/confs/hostapd_open.conf&
fi

sudo dnsmasq -C /home/pi/HackOTG/confs/dnsmasq.conf&
sleep 2
sudo ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
