#!/usr/bin/python

""" README 
Author: Ken Wu
Date: May 2015
This script is customized to maniplate the s3 data and modify their contents and save it as seperate copies on s3

"""

import re
import sys, os
import gzip
from lib.date import create_date, execute_function_on_date_range
from lib.number import ensure_front_leading_zeros
from boto.s3.connection import S3Connection

LOCAL_PATH = '/tmp/s3/semantria/'
aws_key = '<???>'
aws_secret = '<???>'
conn = S3Connection(aws_key, aws_secret)
parent_bucket = conn.get_bucket('localresponse')

def extract(tar_url, extract_path='.'):
    print tar_url
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])

def f_open_edit_save(gz_path):
	f = gzip.open(gz_path, 'rb')
	file_content = f.read()
	print file_content
	f.close()

def f(date_obj):
	for i in xrange(24):	#excluding 24
		si = ensure_front_leading_zeros(i, 2)
		shour = si + "00"
		str_s3_bucket = 'topic_pipeline/semantria/d=' + date_obj.strftime('%Y-%m-%d') + '/h=' + shour
		bucket = parent_bucket.list(str_s3_bucket)
		#print bucket
		for key in bucket:	#loop through each gz file
			print 'Downloading ... ' + key.name
			local_file_name = key.name.replace('/', '_____')
			save_to_local_path = LOCAL_PATH+local_file_name
			if not os.path.exists(save_to_local_path):
				key.get_contents_to_filename(save_to_local_path)

			#now open the gz file 
			f_open_edit_save(save_to_local_path)
			

start_date = create_date('20150501')
end_date = create_date('20150503')
func = f
execute_function_on_date_range(start_date, end_date, func)


#for file_key in bucket:
#    print file_key.name

