#!/usr/bin/python 

""" README 
Author: Ken Wu

This is a library file

"""

def isEmpty (li):
	if len(li) > 0:
		hasSomething = False
		for i in li:
			if i:
				hasSomething = True
		return not hasSomething
	else:
		return True

def printResults(out):
	if not isEmpty(out):
		for o in out:
			print o
	else:
		print "The result is empty..."
