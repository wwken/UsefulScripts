#!/usr/bin/python

""" README 
Author: Ken Wu
Date: May 2015
This script is customized to maniplate the s3 data and modify their contents and save it as seperate copies on s3

Usage: 
	General practice is to execute 1) and then 2) sequentially, from fresh.

	1) Download the orig s3 data and modify it and store it locally, execute:
	./createTopicsToEachRecord.py 

	2) Only upload all the modified gz to s3, execute:
	./createTopicsToEachRecord.py -u

		or
	./createTopicsToEachRecord.py -u -o		

"""

import re
import sys, os
import gzip
import json
import argparse
from lib.date import create_date, execute_function_on_date_range
from lib.number import ensure_front_leading_zeros
from lib.io import get_all_files
from boto.s3.connection import S3Connection

LOCAL_PATH = '/tmp/s3/semantria/'
aws_key = 'AKIAIWA7E7UACZX7BCFQ'
aws_secret = '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'

new_topics = ['Automotive','Auto_Parts','Hybrid_Cars','Luxury_Cars','SUVs','Business','Career','Eco-Friendly','Non-Profit','Politics','Small_Business','Banking','Credit_Cards','Investing','Online_Payment','Beverages','Groceries','Dining','Holiday_Party','Alcohol','Health_Conditions','Wellness_and_Fitness','Babies','Teenagers','Children','Coupons_and_Deals','Shopping','Holiday_Shopping','Luxury_Shopping','Pets','Real_Estate','Wedding','Celebrities','Movies','Music','Television','Gaming','Home_Appliances','Home_Improvement','Baseball','Basketball','Football','Sport_News','Outdoor_Sports','Sport_Retail','Soccer','Tennis','Fashion_Accessories','Beauty','Apparel', 'Electronics','Mobile_Devices','Airlines','Economy_Travel','Hotels','Luxury_Travel','Tourism']
semantria_orig_folder_name_handle = 'semantria'
semantria_modified_folder_name_handle = semantria_orig_folder_name_handle + '_modified'

parser=argparse.ArgumentParser()
parser.add_argument('-u', '--upload', action='store_true', default=False, help='specify whether to upload the modified data to s3')
parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='specify whether to overwrite an existing file on s3')
args = parser.parse_args()

def extract(tar_url, extract_path='.'):
    print tar_url
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])


def append_json_records(existing_json_ary):
	num_new_records_needed = len(new_topics) - len(existing_json_ary)
	start_pos=0
	#print 'num_new_records_needed: ' + str(num_new_records_needed)
	for i in xrange(num_new_records_needed):
		#print 'dewwww ' + str(i)
		duplicated_found=False
		while not duplicated_found:
			this_topic = new_topics[start_pos]
			for j in xrange(len(existing_json_ary)):
				if existing_json_ary[j]['title'] == this_topic:
					#print 'dew ' + this_topic
					start_pos += 1
					duplicated_found=True
					break
			if not duplicated_found:
				existing_json_ary += [{
									#u'sentiment_polarity': u'neutral',
									u'title': u''+this_topic, u'sentiment_score': 0.101010,
									#u'hitcount': 0,
									#u'type': u'concept',
									u'strength_score': 0.123456}]
				start_pos += 1
				break	#exit the outer while loop
	return existing_json_ary

def f_open_edit_save(gz_path):
	f = gzip.open(gz_path, 'rb')
	file_content = f.read()
	json_ary = file_content.split('\n')
	f.close()
	output_file_content = ""
	for json_str in json_ary:
		if json_str:
			my_data = json.loads(json_str)
			#print '\n before: ' + str(my_data)
			if not 'topics' in my_data:
				my_data['topics'] = []
			my_data['topics'] = append_json_records(my_data['topics'])
			output_file_content += json.dumps(my_data) + "\n"
			#print '\n after: ' + str(output_file_content)

	modified_gz_path = gz_path.replace(semantria_orig_folder_name_handle, semantria_modified_folder_name_handle)
	#Now write it back to the local file system
	f = gzip.open(modified_gz_path, 'wb')
	f.write(output_file_content)
	f.close()
	#sys.exit(0)	

def f(date_obj):

	conn = S3Connection(aws_key, aws_secret)
	parent_bucket = conn.get_bucket('localresponse')
	if args.upload:
		print 'Now uploading all the modified gz files to s3'
		stored_modified_path = LOCAL_PATH.replace(semantria_orig_folder_name_handle, semantria_modified_folder_name_handle)
		all_gz_files = get_all_files(stored_modified_path)
		for gz_file in all_gz_files:
			gz_file_s3_full_sub_path = gz_file.replace('_____', '/')
			if parent_bucket.get_key(gz_file_s3_full_sub_path) and not args.overwrite:
				print gz_file_s3_full_sub_path + ' already exists!...overwrite skipping...'
			else:
				key = parent_bucket.new_key(gz_file_s3_full_sub_path)
				key.set_contents_from_filename(stored_modified_path+'/'+gz_file)
				print gz_file_s3_full_sub_path + ' created!'
		sys.exit(0)
	
	for i in xrange(24):	#excluding 24
		si = ensure_front_leading_zeros(i, 2)
		shour = si + "00"
		str_s3_bucket = 'topic_pipeline/'+semantria_orig_folder_name_handle+'/d=' + date_obj.strftime('%Y-%m-%d') + '/h=' + shour
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

start_date = create_date('20150401')
end_date = create_date('20150501')
func = f
execute_function_on_date_range(start_date, end_date, func)


#for file_key in bucket:
#    print file_key.name

