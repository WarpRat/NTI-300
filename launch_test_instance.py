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

import pprint  #Python's pretty print module. Easy way to display things in human readable form.
import httplib #For posting logs and status to slack
import json    #To create slack log objects
import subprocess      #To get user data
from datetime import datetime  #For logging
import time  #To sleep while things launch
import sys  #For error codes and messages on exit
import socket  #To handle socket errors from httplib
import boto3   #Imports the python module that can be used to control AWS resources

#Creating variables to make using the boto3 module easier.

ec2 = boto3.resource('ec2')  #Create a shortcut variable for the boto3 ec2 resource type.
client = boto3.client('ec2')  #Create a shortcut variable for the boto3 ec2 client.


#Creating variables here to be used later in creating the EC2 instance.
#This section would be improved with command line arguments here

amazon_image = 'ami-392ba941'   #Will install the CentOS AMI I created based on the official CentOS cloud image with updated storage.
amazon_instance = 't2.micro'    #Instance size
amazon_pem_key = 'django_dev' #My private key. Actually created months ago last time I was playing with django.
firewall_profiles = ['launch-wizard-4']   #The security group I've been using with the following ports open: 22,80,443,8000.
slack_webhook = 'hooks.slack.com'  #The address to integrate with slack

#Create a dictionary with all the instance info for easy reference later
ec2_data = {}
ec2_data['AMI'] = amazon_image
ec2_data['Instance Type'] = amazon_instance
for i in firewall_profiles:
    ec2_data['Security Group ' + str(firewall_profiles.index(i) + 1)] = i

#A function to write to the slack 'incoming webhook' bot
def write_to_slack(body):
    body_json = json.dumps({"text" : body})  #JSON format for incoming messages - this could be expanded to change channels and other things.
    conn = httplib.HTTPSConnection(slack_webhook)
    headers = {"Content-type": "application/json"}
    conn.request("POST", "/services/T2A60EGCV/B9MSF08UA/30AjuNdmHeQwQnASu5ZwNGI2", body_json, headers)
    response = conn.getresponse()


#Define a module to launch instances.

def launch_test_instance():

    #Get the details of who is running the script and when
    cur_time = datetime.utcnow().strftime('%H:%M:%S')  
    cur_date = datetime.now().strftime('%D')
    cur_user = subprocess.check_output('whoami').rstrip()
    cur_host = subprocess.check_output('hostname').rstrip()
    body = "At *%s UTC* on *%s*:\nThe following user triggered the EC2 launch script for the Django test server\nUser: *%s*\nHost: *%s*" % (cur_time, cur_date, cur_user, cur_host)

    #Send those details to slack
    write_to_slack(body)


    #Format the details of the instance being launched
    body = "The details of instance are:"
    for i in ec2_data:
        body = body + "\n*%s:* %s" % (i, ec2_data[i])

    #Send those details to slack
    write_to_slack(body)

    instances = ec2.create_instances(   #Create an object that stores the response to creating the instance with the previous boto3 shortcut variable.
        ImageId=amazon_image,          #References the image from above.
        InstanceType=amazon_instance,  #References the image type from above.
        MinCount=1,                      #Autoscaling options.
        MaxCount=1,                      #Autoscaling options.
        KeyName=amazon_pem_key,        #Name of the keypair you want to use to authenticate.
        SecurityGroupIds=firewall_profiles,   #Name of the security group to attach.
        #The User Data is the code that is run on boot. This pulls down my django install code from git and runs it.
        UserData="""#!/bin/bash
        curl https://raw.githubusercontent.com/WarpRat/NTI-300/master/install_django.py > /tmp/bootstrap_django.py
        chmod +x /tmp/bootstrap_django.py
        /tmp/bootstrap_django.py""")

    time.sleep(2)  #Give the instance time to come up before querying it
    instance_id = instances[0].id  #Get the new instance ID from the object created by boto
    ec2_deets = client.describe_instances(InstanceIds=[instance_id]) #Get the details from the instance ID
    pub_ip = ec2_deets['Reservations'][0]['Instances'][0]['PublicIpAddress'] #Public IP address
    pub_dns = ec2_deets['Reservations'][0]['Instances'][0]['PublicDnsName']  #Public DNS address
    priv_ip = ec2_deets['Reservations'][0]['Instances'][0]['PrivateIpAddress']  #Private IP address
    az = ec2_deets['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']  #What availability zone in launched into

    #Nicely format the information for Slack
    body = "\n*Success!*\nSuccessfully launced an instance with the instance id of: *%s*" % instances[0].id
    body = body + "\nThe details of the instance are:\n"
    body = body + "*Availability Zone:* " + az
    body = body + "\n*Private IP:* " + priv_ip
    body = body + "\n*Public IP:* " + pub_ip
    body = body + "\n*Public DNS:* " + pub_dns
    #Send it to slack
    write_to_slack(body)

    #Explain the django checking procedure to the user in Slack
    body = "Checking to see if the django server has come up yet. First we'll give it a little while for the scripts to run then attempt to connect 3 times"
    write_to_slack(body)

    #Give the scripts time to run
    time.sleep(180)

    #Start checking if Django is up
    check_django(pub_ip, 3)

#A function to check if Django came up, will take the public ip generated earlier and try three times.
#The port to check on and the number of attempts could be made arguments.
def check_django(pub_ip, tries):

    conn = httplib.HTTPConnection(pub_ip, 8000, timeout=10)
    #Try to connect if it hasn't tried 3 times yet.
    while tries > 0:
        try:
            res = do_check(conn)  #Get an httplib result object from connecting
            body = 'Good news, it looks like %s is up ' % pub_ip
            body += '\nStatus: *%s*\nReason: *%s*' % (str(res.status), str(res.reason))
            #Report success to slack
            write_to_slack(body)
            #Exit the script with a success message
            #sys.exit('Success!')
        except httplib.HTTPException as res: #Catches exceptions for expected errors when the instance isn't up yet
            body = "Not ready yet: " + str(res)
            body += "\nWaiting for 90 seconds"
            write_to_slack(body)
            time.sleep(90)
            tries -= 1
            check_django(pub_ip, tries)
        except Exception as e: #Catches a final error - I'm not certain this will ever get called in the current config.
            body = "%s never connected. Check the logs maybe? Security groups? VPC nacls?" % pub_ip
            print(body)
            print(e)
            write_to_slack(body)
            sys.exit('Never connected')


#The function that actually does the checking
def do_check(conn):
    try:

        conn.request("HEAD", "/") #This will just return status code and reason, HEAD requests don't have data
        res = conn.getresponse()
        return res

    except socket.timeout as e:  #This will return to the check_django function in the HTTPException except block
        raise httplib.HTTPException(e)  #(cont.) this is expected when the instance isn't up at all yet.

    except socket.error as e:

        if '[Errno 111]' in str(e): #This will return to the check_django function in the HTTPException except block
            raise httplib.HTTPException(e)  #(cont.) this is expected as the instance is coming up

        else:  #This is if something is really wrong, i.e. malformed IP, network stack malfunction
            body = "Something is wrong with the connection checking. This is bad. Check the logs."
            body += "\nError message: %s" % e
            write_to_slack(body)
            print(body)
            sys.exit("ohnooooo!")

    except Exception as e: #Final exception for uncaught errors.
        print(e)
        print('Uncaught exception here - failed during connectivity test')
        sys.exit('Uncaught exception. Failed during connectivity test')

launch_test_instance()  #This calls the function created above. It will require that the machine it's being run from holds the proper IAM role to launch EC2 instances.
