#!/usr/bin/python 

""" README 
Author: Ken Wu

This script is to kill all hadoop jobs starting with the job id and incrementing one each time until up to n.

Parameters:
1)	job id to start from
2)	n
3)	login user

Usage: 
1) To kill the job job_20140910_2345 and the next 29 jobs logged in as user etl
	./hadoopJobIdsKillWithRange.py job_20140910_2345 -n 30 -u etl

2) To kill the job job_20140910_2345 only
	./hadoopJobIdsKillWithRange.py job_20140910_2345
	
3) To kill the job job_20140910_2345 logged in as user etl
	./hadoopJobIdsKillWithRange.py job_20140910_2345 -u etl
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
import urllib
import commands
import decimal
import datetime
import time 
import md5

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

def getTheJobName(jID):
	name,_ = jID.rsplit("_", 1)
	#print "num: " + num
	return str(name)

def getTheJobNumber(jID):
	_,num = jID.rsplit("_", 1)
	#print "num: " + num
	return int(num)

def incrementTheJobID (jID):
	jNum = getTheJobNumber(jID);	#it should return the last n digits of the job which is interpreted as number
	jNum += 1
	_,numStr = jID.rsplit("_", 1)
	jNumStr = str(jNum)
	numZeroNeeded = len(numStr) - len(str(jNum))
	while numZeroNeeded > 0:
		jNumStr = '0'+jNumStr
		numZeroNeeded -=1
	jName = getTheJobName(jID);
	return jName + "_" + jNumStr

###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)

#The program starts here
parser = argparse.ArgumentParser(description='Runs hadoop job killer main script.')
parser.add_argument('jobID', help='use to specify the jobID that is to be killed')
parser.add_argument('-n', dest='numOfKills', metavar='numOfKills', type=int, required=False, help='use to specify how many jobs from the jobID needed to be killed')
parser.add_argument('-u', dest='loggedInAs', metavar='loggedInAs', required=False, help='use to login as the user u')
args = parser.parse_args()

jobID = args.jobID
numOfKills = args.numOfKills
loggedInAs = args.loggedInAs

while True:
	hKillJobCmd = "hadoop job -kill " + jobID
	if loggedInAs != None:
		hKillJobCmd = "sudo su - "+loggedInAs+" -c '" + hKillJobCmd + "'"
	print "Executing: " + hKillJobCmd 
	out = lib.commands.execCommand (hKillJobCmd)
	lib.printings.printResults(out)
	if numOfKills != None and numOfKills > 0:
		jobID = incrementTheJobID(jobID)
		numOfKills -= 1
	else:
		break
