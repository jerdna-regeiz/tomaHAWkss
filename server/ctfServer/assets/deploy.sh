#/bin/bash
echo test
for i in $(ls); do salt-cp '*' $i ~/lib ;done
for i in $(ls); do salt-cp '*' $i ~/modules ;done
## salt '*' cmd.run 'python import ~/lib/lib.py'


