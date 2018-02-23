#!/usr/bin/env python

import os

def setup_install():
    
    os.system('yum install -y epel-release')
    os.system('yum update -y')
    os.system('yum install -y python34 python-pip')
    os.system('pip install --upgrade pip')
    os.system('pip install django')
    
def install_django():
    
    os.chdir('/opt')
    os.system('virtualenv -p python3 django')
    os.chdir('/opt/django')
    os.system('source bin/activate ' + \
             '&& pip install django')
    os.system('source bin/activate ' + \
              'django-admin startproject project1')
    os.system('chown -R centos /opt/django')
    
def start_django():
    
    os.system('sudo -u centos && ' + \
             'source /opt/django/bin/activate &&' + \
             '/opt/django/project1/manage.py runserver 0:8000 &')
    

print('Setting up the install')
input('Press any key to continue')
setup_install()

print('Installing Django')
input('Press any key to continue')
install_django()

print('Starting the server')
input('Press any key to continue')
start_django()