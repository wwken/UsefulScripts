#!/usr/bin/python 

""" README 
Author: Ken Wu

This script is to remove all the outdated files/directories specified except the n latest ones

Parameters:
1)  f   - The file system to use, either local or hadoop.  So far only hadoop is supported
3)	n 	- The number of the items to keep (i.e. not deleting)
4)	p 	- The pattens of the paths to remove/keep seperated by ;

Usage: 
1) To keep the top 5 latest items in the hdfs file systems for these file patterns: /local-iq-scoring/addthis-unmatched* and /local-iq-scoring/addthis-tmp*
	./removeOutdatedFilePaths.py -f 'hadoop' -n 5 -p '/local-iq-scoring/addthis-unmatched*;/local-iq-scoring/addthis-tmp*;'
2) To keep the top 5 latest items in the hdfs file systems for these file patterns specified in the conf file: /etc/jobs/conf/dailyFilesToBeRemoved.conf
	./removeOutdatedFilePaths.py -f 'hadoop' -n 5 -p_conf '/etc/jobs/conf/dailyFilesToBeRemoved.conf'



"""

##### Start: Standard libraries ################################################################################################################
import ConfigParser
import argparse
import collections
import datetime
import logging
import os
import re
import shutil
import stat
import sys
import tarfile
import tempfile
import time
import traceback

import commands

import datetime
import time 

import subprocess

from datetime import datetime
from datetime import timedelta

##### End: Standard libraries ###################################################################################################################

##### Start: Customized libraries ################################################################################################################
import lib.printings
import lib.commands
import lib.io
##### End: Customized libraries ##################################################################################################################

################################################################################################################################################

logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
logger = logging.getLogger('com.kwu.utilities')
logger.setLevel(logging.DEBUG)
debug = False

###### Start: Customized functions #############################################################################################################

def getKey(item):
	return item[1]

###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)

#The program starts here
parser = argparse.ArgumentParser(description='Runs Remove outdated files script.')
parser.add_argument('-f', dest='fileSystem', default='hadoop', metavar='fileSystem', type=str, help='The file system to use, either local or hadoop.  So far only hadoop is supported')
parser.add_argument('-p', dest='filePathPatterns', metavar='filePathPatterns', type=str, help='The pattens of the paths to remove/keep seperated by ;')
parser.add_argument('-p_conf', dest='filePathPatternsConfFile', metavar='filePathPatternsConfFile', type=str, help='A conf file that contain all the pattens of the paths to remove/keep seperated by new line ')
parser.add_argument('-n', dest='numOfPathsToKeep', metavar='numOfPathsToKeep', type=int, required=True, help='The number of the items to keep (i.e. not deleting)')
args = parser.parse_args()

fileSystem = args.fileSystem


filePathPatterns = args.filePathPatterns
if filePathPatterns:
	filePathPatterns = filePathPatterns.split(';')
else:
	filePathPatternsConfFile = args.filePathPatternsConfFile
	filePathPatterns = lib.io.read_lines(filePathPatternsConfFile, replace_new_line=True)
numOfPathsToKeep = args.numOfPathsToKeep

commandToLs='hadoop fs -ls'
commandToDel='hadoop fs -rm -r'

if fileSystem != 'hadoop':
	raise Exception('Non support yet!')

for p in filePathPatterns:
	isThisPathS3=False
	if len(p) > 4 and p[0:4]=='s3n:':
		isThisPathS3=True

	command_str = commandToLs + ' ' +p
	out = lib.commands.execCommand(command_str, shell=True, stdout=subprocess.PIPE, stderr=None)
	'''
		For HDFS, The output might contain the following if the p is /local-iq-topic-scoring/addthis-tmp* :

		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-04 00:48 /local-iq-topic-scoring/addthis-tmp.20150720_20150803/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-03 23:27 /local-iq-topic-scoring/addthis-tmp.20150720_20150803/user
		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-05 14:30 /local-iq-topic-scoring/addthis-tmp.20150721_20150804/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-05 13:06 /local-iq-topic-scoring/addthis-tmp.20150721_20150804/user
	'''
	ld = dict()
	l = list()
	bucketId=0
	max_date_obj = None
	bucketId_and_maxDate_stats = list()
	for o in out:
		if re.search("(Found.*items)", o):
			if not isThisPathS3:
				l = list()
				ld[bucketId] = l
				if max_date_obj:
					bucketId_and_maxDate_stats.append((bucketId, max_date_obj))
				max_date_obj = None
				bucketId +=1
			else:
				logger.debug('s3 - do nothing on this line: %s' %(o))
		else:
			content = o.split()
			if len(content) > 4:
				if isThisPathS3:
					#date_str = content[3] + ' ' + content[4]
					t_path = content[5]	
					date_str = re.findall(r'20\d+', t_path)[0]
					#logger.debug('s3 t_path:%s, date_str:%s '%(t_path, date_str))
					date_obj = datetime.strptime( date_str, "%Y%m%d" )
					tu = (bucketId, date_obj, t_path)
				else:
					date_str = content[5] + ' ' + content[6]
					t_path = content[7]
					#logger.debug('hdfs date_str: %s, t_path:%s'%(date_str,t_path))
					date_obj = datetime.strptime( date_str, "%Y-%m-%d %H:%M" )
					tu = (bucketId, date_obj, t_path)
					if not max_date_obj or max_date_obj < date_obj:
						max_date_obj = date_obj
				l.append(tu)
	
	if isThisPathS3:
		lenOfBuckets = len(l)
		for i in range(0, lenOfBuckets-numOfPathsToKeep):
			pp = l[i]
			path_to_be_deleted = pp[2]
			logger.info('this path to be deleted: %s'%(path_to_be_deleted))
			command_del_str = commandToDel + ' ' +path_to_be_deleted
			out = lib.commands.execCommand(command_del_str, shell=True, stdout=subprocess.PIPE, stderr=None)
			logger.info('this path deleted: %s'%(path_to_be_deleted))
	else:
		if max_date_obj:			
			ld[bucketId] = l
			bucketId_and_maxDate_stats.append((bucketId, max_date_obj))
			bucketId_and_maxDate_stats = sorted(bucketId_and_maxDate_stats, key=getKey)
	
		#Okay, now removing the last N items from the list
		lenOfbucketId_and_maxDate_stats = len(bucketId_and_maxDate_stats)
		if lenOfbucketId_and_maxDate_stats > numOfPathsToKeep:
			for i in range(0, lenOfbucketId_and_maxDate_stats-numOfPathsToKeep):
				#Now i is the bucket ID that to be deleted
				allPaths = ld[i]
				for pp in allPaths:
					path_to_be_deleted = pp[2]
					logger.info('this path to be deleted: %s'%(path_to_be_deleted))
					command_del_str = commandToDel + ' ' +path_to_be_deleted
					out = lib.commands.execCommand(command_del_str, shell=True, stdout=subprocess.PIPE, stderr=None)
					logger.info('this path deleted: %s'%(path_to_be_deleted))
		else:
			logger.info('Nothing to delete for path %s since it only has %s paths inside'%(p, lenOfbucketId_and_maxDate_stats))


