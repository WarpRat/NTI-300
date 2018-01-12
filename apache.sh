#!/bin/bash

#Robert Russell - NTI300 - 1/11/18

yum update  #Perform initial updates
yum install -y httpd mod_ssl #Install apache with the https module
systemctl enable httpd #Set apache to start on boot
systemctl restart httpd #Start apache now

sed -i 's/^/#/g' /etc/httpd/conf.d/welcome.conf #Comment out the default welcome page

echo -e "<html>\n<h1>This is my fun new web page! Hooray!!</h1>\n<html>" > /var/www/html/index.html  #write a new landing page for the website


