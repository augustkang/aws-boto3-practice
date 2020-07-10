#!/usr/bin/python

# If instance have "target_tag" and in stopped state
# start instance

import boto3

ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
  tmp_dict = {}
  for each_tag in instance.tags:
    tmp_dict[each_tag['Key']] = each_tag['Value']
  if 'target_tag' in tmp_dict and instance.state['Name'] == 'stopped':
    print("instance name : " + tmp_dict['Name'] + " instance-id : " + instance.instance_id)

