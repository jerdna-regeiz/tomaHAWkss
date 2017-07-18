#/bin/bash
cd ~/src/tomaHAWkss/server/ctfServer/assets/lib
echo test
for i in $(ls ~/src/tomaHAWkss/server/ctfServer/assets/lib); do salt-cp '*' $i ~/lib ;done
## salt '*' cmd.run 'python import ~/lib/lib.py'


