#!/bin/bash

yum install -y epel-release
yum update
yum install -y python-pip
pip install virtualenv
pip install --upgrade pip
yum install python34 python-pip

useradd -m -p pac8bc4CkyUqU robert

cd /opt

virtualenv -p python3 django

cd django
source bin/activate

pip install django
django-admin startproject project1

chown -R robert ../

