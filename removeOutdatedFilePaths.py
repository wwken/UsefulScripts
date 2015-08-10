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
	./removeOutdatedFilePaths.py -cl 'hadoop fs -ls' -cd 'hadoop fs -rmr' -n 5 -p '/local-iq-scoring/addthis-unmatched*;/local-iq-scoring/addthis-tmp*;'


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
parser.add_argument('-p', dest='filePathPatterns', metavar='filePathPatterns', type=str, required=True, help='The pattens of the paths to remove/keep seperated by ;')
parser.add_argument('-n', dest='numOfPathsToKeep', metavar='numOfPathsToKeep', type=int, required=True, help='The number of the items to keep (i.e. not deleting)')
args = parser.parse_args()

fileSystem = args.fileSystem
filePathPatterns = args.filePathPatterns
numOfPathsToKeep = args.numOfPathsToKeep

filePathPatterns = filePathPatterns.split(';')

commandToLs='hadoop fs -ls'
commandToDel='hadoop fs -rmr'

if fileSystem != 'hadoop':
	raise Exception('Non support yet!')

for p in filePathPatterns:
	command_str = commandToLs + ' ' +p
	out = lib.commands.execCommand(command_str, shell=True, stdout=subprocess.PIPE, stderr=None)
	'''
		The output might contain the following if the p is /local-iq-topic-scoring/addthis-tmp* :

		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-04 00:48 /local-iq-topic-scoring/addthis-tmp.20150720_20150803/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-03 23:27 /local-iq-topic-scoring/addthis-tmp.20150720_20150803/user
		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-05 14:30 /local-iq-topic-scoring/addthis-tmp.20150721_20150804/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-05 13:06 /local-iq-topic-scoring/addthis-tmp.20150721_20150804/user
		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-06 00:01 /local-iq-topic-scoring/addthis-tmp.20150722_20150805/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-05 22:39 /local-iq-topic-scoring/addthis-tmp.20150722_20150805/user
		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-09 01:59 /local-iq-topic-scoring/addthis-tmp.20150725_20150808/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-09 00:36 /local-iq-topic-scoring/addthis-tmp.20150725_20150808/user
		Found 2 items
		drwxr-xr-x   - hadoop hadoop          0 2015-08-09 23:44 /local-iq-topic-scoring/addthis-tmp.20150726_20150809/ip
		drwxr-xr-x   - hadoop hadoop          0 2015-08-09 22:22 /local-iq-topic-scoring/addthis-tmp.20150726_20150809/user
	'''
	ld = dict()
	l = list()
	bucketId=0
	max_date_obj = None
	bucketId_and_maxDate_stats = list()
	for o in out:
		if re.search("(Found.*items)", o):
			l = list()
			ld[bucketId] = l
			if max_date_obj:
				bucketId_and_maxDate_stats.append((bucketId, max_date_obj))
			max_date_obj = None
			bucketId +=1
			#print o
		else:
			content = o.split()
			date_str = content[5] + ' ' + content[6]
			date_obj = datetime.strptime( date_str, "%Y-%m-%d %H:%M" )
			if not max_date_obj or max_date_obj < date_obj:
				max_date_obj = date_obj
			tu = (bucketId, date_obj, content[7])
			l.append(tu)
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
				logger.info('this path to be deleted: %s'%(pp[2]))
				command_del_str = commandToDel + ' ' +p
				out = lib.commands.execCommand(command_del_str, shell=True, stdout=subprocess.PIPE, stderr=None)
				logger.info('this path deleted: %s'%(pp[2]))
	else:
		logger.info('Nothing to delete for path %s since it only has %s paths inside'%(p, lenOfbucketId_and_maxDate_stats))


