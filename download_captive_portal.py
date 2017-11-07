#TODO bash notifier
#TODO notice to run as python3

from subprocess import Popen, PIPE, STDOUT

cmd = 'curl -s -L www.google.com/index.html'
#TODO detect fail
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = p.stdout.read()
print(output)
