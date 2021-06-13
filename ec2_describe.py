#!/usr/local/bin/python3
import boto3

ec2 = boto3.resource('ec2')
# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for instance in running_instances:
   for tag in instance.tags:
     if 'Name'in tag['Key']:
        name = tag['Value']
        print(
         "{0},{1},{2},{3},{4},{5}".format(
         instance.id, name, instance.platform, instance.instance_type, instance.private_ip_address, instance.image.name
        )
     )
