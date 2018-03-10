#!/usr/bin/env python

#################
##
## Robert Russell
## 3/2/18
## NTI-300 commented code
## cloned from https://github.com/nic-instruction/NTI-300-2017.git
##
#################

#Importing modules

import boto3   #Imports the python module that can be used to control AWS resources
import base64  #Used to convert strings to and from base64 encoding. I don't actually see it used here however. Could be used to convert userdata to a base64 string.
import pprint  #Python's pretty print module. Easy way to display API responses and other things in human readable form.
import httplib #For posting logs and status to slack
import json  #To create slack log objects

#Creating variables to make using the boto3 module easier. A more readable option than importing python modules using the form `from boto3 import resource as br`.

ec2 = boto3.resource('ec2')  #Create a shortcut variable for the boto3 ec2 resource type.
client = boto3.client('ec2')  #Create a shortcut variable for the boto3 ec2 client.


#Creating variables here to be used later in creating the EC2 instance.

amazon_image = 'ami-392ba941'   #Will install the CentOS AMI I created based on the official CentOS cloud image with updated storage. 
amazon_instance = 't2.micro'    #Instance size                                  
amazon_pem_key = 'django_dev' #My private key. Actually created months ago last time I was playing with django.
firewall_profiles = ['launch-wizard-4']   #The security group I've been using with the following ports open: 22,80,443,8000.
slack_webhook = 'hooks.slack.com'

#Print the current variables to confirm to the user that they are correct or to be logged for troubleshooting.
'''
print(amazon_image)
print(amazon_instance)
print(amazon_pem_key)
'''
#Define a module to launch instances.

ec2_data = {}
ec2_data['AMI'] = amazon_image
ec2_data['Instance Type'] = amazon_instance
for i in firewall_profiles:
  ec2_data['Security Group ' + str(firewall_profiles.index(i) + 1)] = i
slack_payload = {"text" : json.dumps(ec2_data, indent=3, separators=(',',': '))}

slack_json = json.dumps(slack_payload)

conn = httplib.HTTPSConnection(slack_webhook)
headers = {"Content-type": "application/json"}
conn.request("POST", "/services/T2A60EGCV/B9MSF08UA/30AjuNdmHeQwQnASu5ZwNGI2", slack_json, headers)

response = conn.getresponse()
pprint.pprint(response.read())
pprint.pprint(slack_json)
pprint.pprint(slack_payload)

def launch_test_instance():

   instances = ec2.create_instances(   #Create a variable that stores the response to creating the instance with the previous boto3 shortcut variable.
      ImageId = amazon_image,          #References the image from above.
      InstanceType = amazon_instance,  #References the image type from above.
      MinCount=1,                      #Autoscaling options.
      MaxCount=1,                      #Autoscaling options.
      KeyName = amazon_pem_key,        #Name of the keypair you want to use to authenticate.
      SecurityGroupIds = firewall_profiles,   #Name of the security group to attach.
      UserData="""#!/bin/bash
      curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/install_django.py > /tmp/bootstrap_django.py
      chmod +x /tmp/bootstrap_django.py
      /tmp/bootstrap_django.py"""
    )

   pprint.pprint(instances)   #This will print the response returned from boto3 command.


launch_test_instance()  #This calls the function created above. It will require that the machine it's being run from holds the proper IAM role to launch EC2 instances.

