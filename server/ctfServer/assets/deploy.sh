#/bin/bash
echo test
for i in $(ls); do salt-cp '*' $i ~/lib ;done
## salt '*' cmd.run 'python import ~/lib/lib.py'


