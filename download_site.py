#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import os
import sys
#TODO more checks for connectivity and more verbose
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
    savename=url.replace("http://","").replace("https://","")

while 1==1:                                                   
    #delete previous
    p = Popen("rm -Rf "+directory+"/"+url+" && rm -Rf "+directory+"/temp_wget", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout.read().splitlines():
        print(line.decode("utf-8"))
    p.communicate()

    #render javascript of website
    p = Popen("QT_QPA_PLATFORM=offscreen phantomjs resources/get_redirection_url_phantomjs.js "+url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    redirected_url=""
    for line in p.stdout.read().splitlines():
        redirected_url=line.decode("utf-8").rstrip()
    p.communicate()

    #download file
    print('downloading with wget')
    print(redirected_url)
    #p = Popen("cd copied_sites && wget -c -N -mkEpnp -l 1 --max-redirect=100 -P temp_wget "+redirected_url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    #p = Popen("cd copied_sites && wget -mkEpnp -l 1 --max-redirect=100 -P temp_wget "+redirected_url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    p = Popen("cd copied_sites && wget -kEpnp -l 1 --max-redirect=100 -e robots=off -P temp_wget "+redirected_url, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout.read().splitlines():
        print(line.decode("utf-8"))
    p.communicate()
    
    if len(os.listdir(directory+"/temp_wget")) > 0:
        # file exists
        redirects=False
        redirect_url=""
        print("OK and no further redirects");
        #TODO rename to savename
        p = Popen("rm -Rf "+directory+"/"+savename+" && mv "+directory+"/temp_wget/* "+directory+"/"+savename, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in p.stdout.read().splitlines():
            print(line.decode("utf-8"))
        p.communicate()
        break
    else:
        print("wget command copy failed")
