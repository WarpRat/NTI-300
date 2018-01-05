#!/bin/bash

#run initial updates
sudo yum update -y

#install Apache
sudo yum install -y httpd

#Start Apache on boot
sudo systemctl enable httpd

#start Apache now
sudo systemctl start httpd

#install the https module for Apache
sudo yum install -y mod_ssl

#restart Apache in order to use the ssl module
sudo systemctl restart httpd

