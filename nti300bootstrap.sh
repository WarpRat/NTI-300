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

chown -R django ../
chmod -R g=u ../



