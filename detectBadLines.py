#!/usr/bin/python 

""" README 
Author: Ken Wu
Date: 2015 June

This script is to detect any line(s) that is/are of different format of all other lines.  
If there is no delimiter is specified, the script will try to detect one automatically

Parameters:
1)	a path to a single text base file

Usage: 
1) To run the script with the input file located at ~/sample.out	(The most common usage)
	./detectBadLines.py ~/sample.out
2) To run the script with the input file located at ~/sample.out and delimiter as ':'	(less common usage)
	./detectBadLines.py ~/sample.out -d ':'
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

##### End: Standard libraries ###################################################################################################################

##### Start: Customized libraries ################################################################################################################
from lib.io import read_lines
##### End: Customized libraries ##################################################################################################################

################################################################################################################################################

logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
logger = logging.getLogger('com.kwu.utilities')
logger.setLevel(logging.DEBUG)
info = logger.info
debug = logger.debug

##DEBUG related #########################################
def dd():
    try:
        if not r'/usr/local/share/pysrc' in sys.path:
            sys.path.append(r'/usr/local/share/pysrc') #assuming this is the pydev installation path
        import pydevd
        pydevd.settrace()
    except: 
        pass

###### Start: Customized functions #############################################################################################################

def index(s, r, pos=0):
	try:
		return s.index(r, pos)
	except:
		return None

#This function empties all the complex clause.  A clause is empty if it is of form: "xxx" or {xxx} 
#	For example, if a line is like: Ken is a very smart guy {also known as a handsome} but somehow {he is too shy}
#	Then it should return Ken is a very smart guy {} but somehow {}
def empty_complex_clause(line, rcc):
	#debug('o: %s' % line)
	cline = line
	for elem in rcc:
		ll=0
		#dd()
		while(True):
			l = index(cline, elem[0], ll) if ll==0 or ll else None
			r = index(cline, elem[1], l+1) if l else None
			if l and r and l < r-1:
				#print "l: %s, r: %s" %(l, r)
				#print cline[0:l] + ' **** ' + cline[r:]
				new_line = cline[0:l+1] + cline[r:]
				cline = new_line
				ll = index(cline, elem[0])
				if ll:
					ll = ll + 2
				else:
					break
			else:
				#print 'none...'
				break
	#debug('c: %s' % cline)
	return cline

###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)

#The program starts here
parser = argparse.ArgumentParser(description='Runs bad lines detection script.')
parser.add_argument('file_path', help='the input file path')
parser.add_argument('-d', dest='delimiter', metavar='delim', type=str, required=False, help='specify the delimiter to be used')
#parser.add_argument('-u', dest='loggedInAs', metavar='loggedInAs', required=False, help='use to login as the user u')
args = parser.parse_args()

file_path = args.file_path
lines = read_lines(file_path)

POSSIBLE_DELIMITERS=['\t', ',']
RECONGIZED_COMPLEX_CLAUSES=[['"', '"'], ['{', '}']]

delimiter=args.delimiter

if not delimiter:
	max_occur=-1
	max_index=-1
	i=0
	for d in POSSIBLE_DELIMITERS:
		l = lines[0]
		c = l.count(d)
		if c>max_occur:
			max_occur=c
			max_index=i
		i+=1
	delimiter=POSSIBLE_DELIMITERS[max_index]
	info('The delimiter is detected to be: "%s"' %delimiter)
else:
	info('The delimiter is provided as: "%s"' %delimiter)

#Now looping each line
e_d=dict()
for line in lines:
	line = empty_complex_clause(line, rcc=RECONGIZED_COMPLEX_CLAUSES)
	s = line.split(delimiter)
	c=len(s)
	if not c in e_d:
		e_d[c] = (1, line)
	else:
		e_d[c] = (e_d[c][0] + 1, e_d[c][1])

#Pick the max occurence
max=-1 
max_ind=-1
for e in e_d:
	if e_d[e][0] > max:
		max = e_d[e][0]
		max_ind=e
		#print max

for e in e_d:
	if e != max_ind:
		info('suspect line: %s ' % str(e_d[e][1]) )
#print e_d
