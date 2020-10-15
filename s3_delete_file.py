#!/usr/bin/python3

import os
import boto3
from botocore.errorfactory import ClientError
from concurrent.futures import ProcessPoolExecutor
import time

def read_line(start,end):
    s3 = boto3.client('s3')
    with open('file_list.txt') as f:
        bucket_list = ['bucket1','bucket2','bucket3']
        key_list = f.readlines()[start:end]
        key_list = [line[:-1] for line in key_list]

	return_value = {}
	for target_key in key_list:
            for target_bucket in bucket_list:
                try:
                    return_value = s3.head_object(Bucket=target_bucket, Key=target_key)
	            s3.delete_object(Bucket=target_bucket,Key=target_key)
	            break
        	except ClientError:
                    pass

if __name__ == "__main__":

    line_count = 0
    
    with open('file_list.txt') as f:
        for line in f:
            line_count += 1
    
    num_process = input("Type number of processes to run : ")
    if num_process == "":
        print("You didn't type process number. Please try again")
        exit()

    lines_numbers = [0]
    
    for i in range(num_process):
        line_numbers.append(line_count // num_process)
    
    remainders = line_count % num_process

    if remainders != 0:
        for i in range(remainders):
            line_numbers[i+1] = line_numbers[i+1] + 1

    for index, value in enumerate(line_numbers):
        if index == 0:
            pass
        else:
            line_numbers[index] = line_numbers[index-1] + value
   
    range_list = []

    for index, value in enumerate(line_numbers):
        if index == 0:
            range_list.append(range(1,value+1))
        else:
            range_list.append(range(line_numbers[index-1]+1, line_numbers[index]+1)) 
    
    with ProcessPoolExecutor(num_process) as executor:
        for i in range(len(line_numbers)):
            if i == num_process:
                pass
            else:
                executor.submit(read_line, line_numbers[i], line_numbers[i+1])

