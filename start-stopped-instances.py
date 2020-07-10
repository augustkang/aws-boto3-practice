#!/usr/bin/python

# If an instance's tag have value "target_value" and in stopped state
# start that instance

import boto3

ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
  tmp_dict = {}
  for each_tag in instance.tags:
    tmp_dict[each_tag['Key']] = each_tag['Value']
  if 'target_value' in tmp_dict.values() and instance.state['Name'] == 'stopped':
    instance.start()
    print("instance " + tmp_dict['Name'] +" started")
