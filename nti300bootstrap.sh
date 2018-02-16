#!/bin/bash

yum install -y epel-release
yum update -y
yum install -y python-pip
pip install virtualenv
pip install --upgrade pip
yum install -y python34 python-pip

#useradd -m -p pac8bc4CkyUqU robert

useradd -r -s /sbin/nologin django
useradd -m -G wheel django robert
passwd -d robert
passwd -e robert


cd /opt

virtualenv -p python3 django

cd django
source bin/activate

pip install django
django-admin startproject project1

chown -R django /opt/django/
chmod -R g=u /opt/django/

cur_ip=$(getent ahosts cloud.melanieclark.info | head -n 1 | awk '{print $1}')

sed -i "s/ALLOWED_HOSTS \= \[/&'$cur_ip'/" /opt/django/project1/project1/settings.py

/sbin/runuser django -s /bin/bash -c "\
	source /opt/django/bin/activate &&
	/opt/django/project1/manage.py runserver 0:8000"


