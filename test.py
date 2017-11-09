#!/usr/bin/python

from subprocess import Popen, PIPE, STDOUT
import os

#create directory and gitignore it
directory="copied_network_profiles"
p = Popen("sudo iwlist wlan0 scan | grep -A 5 'Cell'", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
test=[]
for line in p.stdout.read().splitlines():
    test.append(line.decode("utf-8"))
    print(line.decode("utf-8"))


#show all the old ones available
# if captive portal with that name is found, reuse, if none ask if I want one
#TODO ask reuse old one or 0(new) -> network_profiles folder
    #TODO if new
        #TODO scan all, give nr's and gather data ready to use
        #-> sudo iwlist wlan0 scan | grep 

        #TODO option kiezen en terug 
        #TODO make profile, connect to it, route wlan, copy portal (ask to)
            #TODO copy portal miss herhalen ... als gefaald is?
        #TODO save profile in network_profiles

    
#TODO ask if inject scripts (which ones,)
#TODO ask if check for creds flying over the air urlsnarf? -> log to a file

#TODO make a folder with the captive portal and the injected file inserted into it.
#TODO start op server 
#TODO start up spoof
#TODO start up hostapd with all the settings (maybe bssid)


