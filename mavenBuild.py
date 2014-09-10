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
import commands


logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
logger = logging.getLogger('etl.bin.media_deal_program')
logger.setLevel(logging.DEBUG)
debug = False


################################################################################################################################################
""" README 

Author: Ken.Wu

 This python script is to automate all maven project builds in one click.  Since every time we building a whole project we need to maven build each sub project and wait for It's finish.  Very waste human being times.  
 The first parameter is a path to the parent project folder
 The all other parameters are the project name that we want to maven build

Usgae: 
./mavenBuild.py /home/kwu/workspace/GIT_etl/etl petl-model psjobs-common psjobs-etl
./mavenBuild.py /home/kwu/workspace/GIT_etl/etl psjobs-common psjobs-etl
./mavenBuild.py /home/kwu/workspace/GIT_etl/etl psjobs-etl

"""
################################################################################################################################################


###### Start: Customized functions #############################################################################################################
def writeLineToTheFile(line, fullFilePath):
	f = open(fullFilePath, 'w')
	f.write(line)
	f.close()

def showFileDetails (dirPath):
	validJarCounter = getJarsCountDetails(dirPath)
	if validJarCounter == 0:
		print '	**ERROR**: no jar file in %s' % (dirPath)
	else:
		print '	There are totally %s jars file in %s' % (validJarCounter,dirPath)

def getJarsCountDetails (dirPath):
	validJarCounter = 0
	for filename in os.listdir(dirPath):
		fullPathName = os.path.join(dirPath, filename)
		if os.path.isdir(fullPathName):
			validJarCounter += getJarsCountDetails(fullPathName)
		else:
			if filename.endswith('.jar'):
				modTime = time.ctime(os.path.getmtime(fullPathName))
				print '	%s %s %s ' % (os.path.getsize(fullPathName), modTime, fullPathName)
				validJarCounter += 1
	return validJarCounter


###### End:   Customized functions #############################################################################################################


#The program starts here
if len(sys.argv)-1 < 1:
	print (len(sys.argv))
	print("Run the program with this format, for example, ./mavenBuild.py /home/kwu/workspace/GIT_etl/etl petl-model psjobs-common psjobs-etl: ")
	print("The 1st parameter is the home project location that it is referencing to")
	print("The 2nd and so on parameters are the project name that we want to maven build")
	print("Exiting...")
	sys.exit()
	
programArgs = sys.argv

counter = 0
projectParent = ''
allLogs = ''
logFile = 'lastBuildHistory.log'
for arg in programArgs:
	if counter > 1:
		mavenPath = arg
		wholePath = []
		wholePath.append(projectParent)
		wholePath.append('/')
		wholePath.append(mavenPath)
		wholePath.append('/pom.xml')
		wholePathStr = ''.join(wholePath)
		#print wholePathStr
		command = 'mvn -f %s clean install' % (wholePathStr)
		#print command
		#print subprocess.call(command,stdout=subprocess.PIPE,shell=True).stdout.read()
		
		allLogs = '%s %s ' % (allLogs, commands.getstatusoutput(command))
		logger.info('%s being executed sucessfully' %command)
		
		thisProjDir = os.path.dirname(wholePathStr)
		#print thisProjDir
		showFileDetails(thisProjDir)
		"""
		retPatch = pPatch.wait()
		if retPatch != 0:
			logger.error("unexcepted error: %s" % retPatch)
			sys.exit(-1)
		else:
			logger.info("mvn sucessful")
		"""	
	elif counter == 1:
		projectParent = str(arg)
	else:
		pass
	counter+=1

writeLineToTheFile(allLogs, logFile)
logger.info('All execution logs have been written to %s' %logFile)

