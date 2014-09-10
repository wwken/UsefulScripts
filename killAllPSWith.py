#!/usr/bin/python 

import ConfigParser
import argparse
import collections
import datetime
import logging
import os
import re
import shutil
import stat
import subprocess
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

logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
logger = logging.getLogger('etl.bin.media_deal_program')
logger.setLevel(logging.DEBUG)
debug = False


################################################################################################################################################
""" README 
This script is to kill all process specified by the grep search on all input arguements

For example, if we want to kill all processes that are associated to 'view' and 'tmp', we can do:
./killAllPSWith.py view tmp

On the other hand, we can kill all eclipse process by issuing this command
./killAllPSWith.py eclipse

"""
################################################################################################################################################

###### Start: Customized functions #############################################################################################################
def execCommand(c, debugFlag=False):
	child = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr)=child.communicate()
	stdout=stdout.strip()
	erroutPut = None
	if stderr:
		outPut = stderr.split("\n")
	else:
		outPut = stdout.split("\n")
		if debugFlag == True:
			logger.debug("In execCommand, returning: %s" % outPut )
	return outPut
	
def isEmptyOutput(li):
	if len(li) == 0:
		return True
	elif len(li) == 1:
		if not li[0]:
			return True
		else:
			return False
	else:
		return False
	
###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)
grepC=""
for count, arg in enumerate(sys.argv):
	if count>0 :
		grepC+="grep -i "+arg+" | "

allRunningProcesses="ps -ef | " + grepC + " grep -v grep | grep -v "+thisFileName+" | awk '{print $2}'";

#print killC
runningProcesses = execCommand (allRunningProcesses);

if isEmptyOutput(runningProcesses):
	logger.info("No process found under this command: %s" % allRunningProcesses )
else:	
	for pid in runningProcesses:
		print "killing process: " + pid
		killCommand="kill -9 " + pid
		status=execCommand (killCommand)
		logger.info("Status: %s" % status )


