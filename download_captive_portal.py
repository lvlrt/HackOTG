from subprocess import Popen, PIPE, STDOUT

cmd = 'ls /etc/fstab /etc/non-existent-file'
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = p.stdout.read()
print(output)
