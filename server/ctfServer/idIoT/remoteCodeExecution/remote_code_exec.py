#!/usr/bin/env python

import paramiko
import sys
from paramiko import SSHClient


def execute(file, remote_path, host, user, pw=''):
    destexploit=remote_path
    exploit_to_execute=file
    print (host)
    print (user)

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)

    sftp = ssh.open_sftp()
    sftp.put(exploit_to_execute, destexploit)
    ssh.exec_command("chmod 777 " + destexploit)
    stdin, stdout, stderr = ssh.exec_command(destexploit)
    print "stderr: ", stderr.readlines()
    print "pwd: ", stdout.readlines()

