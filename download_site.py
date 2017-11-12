#!/usr/bin/python

#import urllib.request
#urllib.request.urlopen("http://example.com/foo/bar").read()

from subprocess import Popen, PIPE, STDOUT
import os
import sys

if len(sys.argv) > 3 or len(sys.argv)<2:
    print("First argument has to be site, Second (save name) is optional")
    exit();
#create directory and gitignore it
directory="copied_sites"
p = Popen("mkdir "+directory+" && touch "+directory+"/.gitignore", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
for line in p.stdout.read().splitlines():
    print(line.decode("utf-8"))
p.communicate()
#set basic url
url=sys.argv[1]
if len(sys.argv) == 3:
    savename=sys.argv[2]
else:
    savename=url

while 1==1:                                                   
    #delete previous
    p = Popen("rm -Rf "+directory+"/"+url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout.read().splitlines():
        print(line.decode("utf-8"))
    p.communicate()

    #download file
    p = Popen("cd copied_sites && wget -c -N -mkEpnp -l 1 --max-redirect=100 "+url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout.read().splitlines():
        print(line.decode("utf-8"))
    p.communicate()
    
    if len(os.listdir(directory+"/"+url)) > 0:
        # file exists
        redirects=False
        redirect_url=""
        
        for filename in os.listdir(directory+"/"+url):
            with open(directory+"/"+url+"/"+filename) as f:
                for line in f.readlines():
                    if "<meta" in line and '"refresh"' in line:
                        redirect=True
                        line=line.rstrip()
                        index= line.find("URL=")
                        if index != -1:
                            line=line[index:] # strip all till URL=

                        index= line.find('"')
                        if index != -1:
                            line=line[:index] # strip all till quote

                        index= line.find("'")
                        if index != -1:
                            line=line[:index] # strip all till single quote

                        index= line.find(";")
                        if index != -1:
                            line=line[:index] # strip all till semi

                        index= line.find(" ")
                        if index != -1:
                            line=line[:index] # strip all till space
                        redirect_url=line
        if redirects:
            #if redirects are found
            #TODO remove old url
            #delete previous
            p = Popen("rm -Rf "+directory+"/"+url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            for line in p.stdout.read().splitlines():
                print(line.decode("utf-8"))
            p.communicate()

            url=redirect_url #change url to redirected url found
        else:
            print("OK and no further redirects");
            #TODO rename to savename
            p = Popen("rm -Rf "+directory+"/"+savename+" && mv "+directory+"/"+url+" "+directory+"/"+savename, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            for line in p.stdout.read().splitlines():
                print(line.decode("utf-8"))
            p.communicate()
            break
    else:
        print("wget command copy failed")
