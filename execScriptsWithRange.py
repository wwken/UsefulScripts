#!/usr/bin/python 

""" README 
Author: Ken Wu

This script is to execute a given script with the start date and end date and numOfDaysEachRun as parameters.
The motivitaion of having this script is that due to memory constraints in some systems, it makes sense to cut the whole execution into smaller chunks (paritioned by the date range) instead.

Parameters:
1)	location of the script to be executed - e.g. /home/kwu/scripts/runStep1.sh
2)	The start date - e.g. 20140101
3)	The end date   - e.g. 20141231
4)	The number of days each run to be executed  - e.g. 30

Usage: 
1) To exeute the script runStep1.sh from 20140101 to 20141231 by running 30 days in each run (i.e. cutting the whole execution into 12 times)
	./execScriptsWithRange.py /home/kwu/scripts/runStep1.sh 20140101 20141231 30

	It means that, internally, the script will execute the following commands 12 times as follow:
	/home/kwu/scripts/runStep1.sh 20140101 20140131
	/home/kwu/scripts/runStep1.sh 20140201 20140228
	/home/kwu/scripts/runStep1.sh 20140301 20140331
	/home/kwu/scripts/runStep1.sh 20140401 20140430
	...
	...
	/home/kwu/scripts/runStep1.sh 20141201 20141231

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

def downOneMonthIfOverFlow (aDate, bDate, numOfDaysEachRun):
	diffMonth = bDate.month - aDate.month
	numOfMonthEachRun = numOfDaysEachRun / 30
	if ( diffMonth==0 or diffMonth < numOfMonthEachRun ):
		#OKAY
		#print "OKAY"
		
		#allow to jump one or two more days if it is on boundary
		tmp1BDate = bDate + timedelta(days=1)
		tmp2BDate = bDate + timedelta(days=2)
		if tmp1BDate.month==bDate.month and tmp2BDate.month !=  bDate.month:
			bDate=bDate + timedelta(days=1)

		return bDate
	else:
		oldBMonth = bDate.month
		while (bDate.month == oldBMonth):
			#print " looping..." + format(bDate)
			bDate = bDate - timedelta(days=1)
		return bDate

###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)

#The program starts here
if len(sys.argv)-1 != 4:
	logger.error (len(sys.argv))
	logger.error("This program takes four inputs...")
	logger.error("Exiting...")
	sys.exit()

scriptName = sys.argv[1]
fromDate = sys.argv[2]
toDate = sys.argv[3]
numOfDaysEachRun = int(sys.argv[4]) - 1

myDateFormat = '%Y%m%d'

#command = scriptName
curDate = datetime.strptime(fromDate, myDateFormat)
endDate = datetime.strptime(toDate, myDateFormat)

while True:
	if curDate > endDate:
		break
	nextCurDate = curDate + timedelta(days=numOfDaysEachRun)
	nextCurDate = downOneMonthIfOverFlow(curDate, nextCurDate, numOfDaysEachRun)
	
	command = scriptName + " " + format(curDate.strftime(myDateFormat)) + " " + format(nextCurDate.strftime(myDateFormat))
	out = lib.commands.execCommand (command)
	lib.printings.printResults(out)
	
	curDate = nextCurDate + timedelta(days=1)

#out = lib.commands.execCommand (command);
#lib.printings.printResults(out)




