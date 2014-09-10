#!/usr/bin/python 

""" README 
Author: Ken Wu

This is a library file

"""
##### Start: Standard libraries ################################################################################################################
import subprocess
##### End: Standard libraries ###################################################################################################################

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
