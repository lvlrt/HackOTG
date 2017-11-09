#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import os

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#create directory and gitignore it
directory="copied_network_profiles"
p = Popen("mkdir "+directory+" && touch "+directory+"/.gitignore", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
for line in p.stdout.read().splitlines():
    print("[DEBUG]"+line.decode("utf-8"))

#show all the old ones available
p = Popen("ls -l "+directory, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
old_networks=[]
for line in p.stdout.read().splitlines():
    print("[DEBUG]"+line.decode("utf-8"))
    old_networks.append(line.decode("utf-8"))
old_networks = old_networks[:-1] #last one is unneccesairy due to the total amount of files outputted by ls (last line)
if len(old_networks) > 0:
    print("ALREADY COPIED NETWORKS:")
    counter=1
    for network in old_networks: #print all old ones with nr's before them.
        print(counter+") "+network)
        counter=counter+1
    print("Give a nr of a network you want to use or")
else:
    print("[INFO]NO COPIED NETWORKS")

print("Give '0' to copy a new non-profiled network or type anything else to quit") #Give input option 0 for create new, and add all the other ones, q = quit
answer=input()

if answer == "0":
    #CREATE NEW
    print("Looking for new networks to copy")
    #scan all, give nr's and gather data ready to use
    target_essid=""
    while 1:
        print("Scanning for networks")
        p = Popen("sudo iwlist wlan0 scan | grep -A 5 'Cell'", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        scanned_networks_raw=[]
        for line in p.stdout.read().splitlines():
            if line.decode("utf-8") !="--": #filter the grep extras
                scanned_networks_raw.append(line.decode("utf-8"))
                print("[DEBUG]"+line.decode("utf-8"))

        #parse all networks in an array with properties
        scanned_networks=[]
        for i in range(int((len(scanned_networks_raw)-int(len(scanned_networks_raw))%6)/6)):
            scanned_networks.append({})
            for data in scanned_networks_raw[6*i+0:6*i+6]: 
                if "Quality" in data:
                    scanned_networks[i]["info"]=data.lstrip().rstrip()
                else: 
                    scanned_networks[i][data.split(":",1)[0].lstrip().rstrip().replace('"','')]=data.split(":",1)[1].lstrip().rstrip().replace('"','')
        
        # list all networks
        counter = 1
        for network in scanned_networks:
            print(str(counter)+") "+network["ESSID"])
            counter=counter+1

        print("Give the number of the network you want to copy, or leave empty to scan again:")
        #TODO check if the number is in range, and is a number
        answer=input()
        if int(answer) < counter:
            print("ok")
            target_essid=scanned_networks[int(answer)]
            break

    #TODO make profile, connect to it, route wlan, copy portal (ask to)
        #TODO copy portal miss herhalen ... als gefaald is?
        #TODO save profile in network_profiles

elif is_number(answer) and int(answer) <= len(old_networks): 
    #USE EXISITING
    print("existing")
else:
    #EXIT
    print("Quiting...")
    exit()

    
#TODO ask if inject scripts (which ones,)
#TODO ask if check for creds flying over the air urlsnarf? -> log to a file

#TODO make a folder with the captive portal and the injected file inserted into it.
#TODO start op server 
#TODO start up spoof
#TODO start up hostapd with all the settings (maybe bssid)

