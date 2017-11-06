# HackOTG
A universal, portable, cross-platform security platform based on a RPi Zero

# Installation
First get an sd card for in the Rpi zero formatted with a Raspbian image (may be the lite one).
<pre>wget https://downloads.raspberrypi.org/raspbian_lite_latest
unzip raspbian_lite_latest #will unzip an .img file 

fdisk -l #lookup the device name of your SD-card (ex. /dev/mmcblk1)
dd bs=4M if=2017-09-07-raspbian-stretch-lite.img of=/dev/mmcblk1 conv=fsync #change /dev/mmcblk1
</pre>

You may want to resize the last partition to the full size
<pre>
$ fdisk /dev/mmcblk1 #change /dev/mmcblk1 to your device

Welcome to fdisk (util-linux 2.30.2).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.
<strong>Command (m for help): p</strong>
Disk /dev/mmcblk1: 29.8 GiB, 32026656768 bytes, 62552064 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x11eccc69
Device Boot Start End Sectors Size Id Type
/dev/mmcblk1p1 8192 93813 85622 41.8M c W95 FAT32 (LBA)
/dev/mmcblk1p2 <strong>94208</strong> 62552063 62457856 29.8G 83 Linux
<strong>Command (m for help): d</strong>
<strong>Partition number (1,2, default 2): 2</strong>
Partition 2 has been deleted.
<strong>Command (m for help): n</strong>
Partition type
 p primary (1 primary, 0 extended, 3 free)
 e extended (container for logical partitions)
<strong>Select (default p): p</strong>
<strong>Partition number (2-4, default 2): 2</strong>
First sector (2048-62552063, default 2048): <strong>94208</strong>
<strong>Last sector, +sectors or +size{K,M,G,T,P} (94208-62552063, default 62552063):</strong>
Created a new partition 2 of type 'Linux' and of size 29.8 GiB.
Partition #2 contains a ext4 signature.
<strong>Do you want to remove the signature? [Y]es/[N]o: n</strong>
<strong>Command (m for help): w </strong>
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
</pre>

Now mount the partitions and change some basic files
<pre>
mkdir boot
mount /dev/mmcblk1p1 boot #change mmcblk1 part into your device
mkdir root
mount /dev/mmcblk1p2 root #change mmcblk1 part into your device

echo 'dtoverlay=dwc2' >> boot/config.txt
echo -e "dwc2\ng_ether" >> root/etc/modules

echo -e "\nallow-hotplug usb0\niface usb0 inet static\naddress 192.168.7.2\nnetmask 255.255.255.0\nnetwork 192.168.7.0\nbroadcast 192.168.7.255\ngateway 192.168.7.1" >> root/etc/network/interfaces

touch boot/ssh
</pre>

Copy the software packages
<pre>
cd root/home/pi
git clone https://github.com/larsveelaert/HackOTG
</pre>

Make it start up a hotspot
<pre>
sudo sed --in-place "/exit 0/d" root/etc/rc.local
echo -e "/bin/sh /home/pi/HackOTG/hotspot_start.sh\nexit 0\n" >> root/etc/rc.local
</pre>

Sync and unmount
<pre>
sync
unmount boot root
</pre>

# Usage
Now you can SSH to this device with the default credentials (user: pi, pass: raspberry):
<pre>
ifconfig usb0 192.168.7.3
ssh pi@192.168.7.2
</pre>
