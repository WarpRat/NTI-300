#!/usr/bin/env python

########################
##
## Robert Russell
## NTI-300 2/24/18
##
## Python Django install
## Centos 7
##
########################


#Import the os module to allow the python script to issue commands
import os

#Install updates, python3, and pip. Use pip to install virtualenv.
def setup_install():

    os.system('yum install -y epel-release')
    os.system('yum update -y')
    os.system('yum install -y python34 python-pip')
    os.system('pip install --upgrade pip')
    os.system('pip install virtualenv')

#Make the directory structure for the django server using the virtualenv and install django using pip.
def install_django():

    os.chdir('/opt')
    os.system('virtualenv -p python3 django')
    os.chdir('/opt/django')
    os.system('source bin/activate ' + \
             '&& pip install django')
    os.system('source bin/activate ' + \
              '&& django-admin startproject project1')
    os.system('chown -R centos /opt/django')

#Start the server using the non root user.
def start_django():

    os.system('sudo -u centos /bin/bash -c "' + \
             'source /opt/django/bin/activate &&' + \
             '/opt/django/project1/manage.py runserver 0:8000 &"')

#Call all three functions in order.

#print('***************Setting up the install**********************') #Testing
setup_install()

#print('******************Installing Django************************') #Testing
install_django()

#print('****************Starting the server****************************') #Testing
start_django()
