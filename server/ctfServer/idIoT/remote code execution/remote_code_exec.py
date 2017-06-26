#!/usr/bin/env python

import paramiko
import sys
from paramiko import SSHClient

print(len(sys.argv))
pw=''
if len(sys.argv) == 6:
    pw=sys.argv[5]

host=sys.argv[3]
user=sys.argv[4]
destexploit=sys.argv[2]
exploit_to_execute=sys.argv[1]
print (host)
print (user)

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw)

#destexploit="./test_exploit"
sftp = ssh.open_sftp()
sftp.put(exploit_to_execute, destexploit)
ssh.exec_command("chmod 777 " + destexploit)
stdin, stdout, stderr = ssh.exec_command(destexploit)
print "stderr: ", stderr.readlines()
print "pwd: ", stdout.readlines()

