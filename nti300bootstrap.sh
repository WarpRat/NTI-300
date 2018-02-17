#!/bin/bash
#
#Django installation script
#for use with Centos only - RHEL requires extra steps
#
#Robert Russell 2/16/18

#Install the epel repo and yum update.
#Install required packages
yum install -y epel-release
yum update -y
yum install -y python-pip
pip install virtualenv
pip install --upgrade pip
yum install -y python34 python-pip

#Set variables here:
new_user=robert
auth_key_dir="http://keys.melanieclark.info"

#Get the public IP of the EC2.
cur_ip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)



#Create a service account for django to run under, don't allow login.
#Create an account for myself and force creating a password on first use.
#Also make sure I'm in the correct group.
useradd -r -s /sbin/nologin django
useradd -m -G wheel,django "$new_user"
passwd -d "$new_user"
passwd -e "$new_user"

#
if cd /home/"$new_user"/.ssh/ || mkdir /home/"$new_user"/.ssh && cd /home/"$new_user"/.ssh; then
	curl "$auth_key_dir" > authorized_keys
	chown robert:robert authorized_keys
	chmod 600 authorized_keys
else
	echo "Error creating .ssh directory and authorized keys file for $new_user - was the user created?" |\
	       	tee /home/$new_user/ssh_error.log |\
	       	logger -t [NEW_USER] -p error
fi

cd /opt

#Create a virtual environment named django using python3. This creates a folder as well.
virtualenv -p python3 django

#Enter the django folder and activate the virtualenv.
cd django
source bin/activate

#Install django and start a new project.
pip install django
django-admin startproject project1

#Change owernship of all the django files to the django service user. Set group and owner permissions to be the same.
chown -R django /opt/django/
chmod -R g=u /opt/django/

#Add the public IP to the allowed hosts file.
sed -i "s/ALLOWED_HOSTS \= \[/&'$cur_ip'/" /opt/django/project1/project1/settings.py

#Start an example server using the service account.
/sbin/runuser django -s /bin/bash -c "\
	source /opt/django/bin/activate &&
	/opt/django/project1/manage.py runserver 0:8000 &"

