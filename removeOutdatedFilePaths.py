#!/usr/bin/python 

""" README 
Author: Ken Wu

This script is to remove all the outdated files/directories specified except the n latest ones

Parameters:
1)  c   - The remove command: it can be: 'rm -rf' or 'hadoop fs -rmr'.  By default, it will be 'rm -rf'
2)	n 	- The number of the items to keep (i.e. not deleting)
3)	p 	- The pattens of the paths to remove/keep seperated by ;

Usage: 
1) To keep the top 5 latest items in the hdfs file systems for these file patterns: /local-iq-scoring/addthis-unmatched and /local-iq-scoring/addthis-tmp
	./removeOutdatedFilePaths.py -c 'hadoop fs -rmr' -n 5 -p '/local-iq-scoring/addthis-unmatched;/local-iq-scoring/addthis-tmp;'


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


###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)

#The program starts here
parser = argparse.ArgumentParser(description='Runs Remove outdated files script.')
parser.add_argument('-c', dest='commandToRun', metavar='commandToRun', type=str, required=True, help='The remove command: it can be: "rm -rf" or "hadoop fs -rmr".  By default, it will be "rm -rf"')
parser.add_argument('-p', dest='filePathPatterns', metavar='filePathPatterns', type=str, required=True, help='The pattens of the paths to remove/keep seperated by ;')
parser.add_argument('-n', dest='numOfPathsToKeep', metavar='numOfPathsToKeep', type=int, required=True, help='The number of the items to keep (i.e. not deleting)')
args = parser.parse_args()

commandToRun = args.commandToRun
filePathPatterns = args.filePathPatterns
numOfPathsToKeep = args.numOfPathsToKeep

print commandToRun