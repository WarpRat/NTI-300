#!/bin/bash

#Make a directory for the scripts to pull down
mkdir /root/bin

#Pull the script that will perform initial updates and install Apache with the basic site, make it executable, and run it.
curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/apache.sh > /root/bin/startup.sh
chmod +x /root/bin/startup.sh
/root/bin/startup.sh

#Pull the script that will look at disk use, make it executable, and pull down a cron tab with the script set to run each minute.
curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/du_to_html.sh > /root/bin/du_to_html.sh
chmod +x /root/bin/du_to_html.sh
curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/robert > /var/spool/cron/root

#Create some dummy data to make things more interesting
for i in melanie andy john max; do
	count=${RANDOM:0:3}
	mkdir /home/$i
	cd /home/$i
	dd if=/dev/zero of=/home/$i/testfile.txt bs=1M count=$count
done
