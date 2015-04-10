#!/usr/bin/python 

""" README 
Author: Ken Wu

"""
import sys
from sys import argv

script, filename = argv

lines = open(filename)
line_pos=1
for line in lines:
	s_items=line.split("\t");
	s_f_items=filter((lambda x: len(x)>0), s_items)
	if len(s_items) != len(s_f_items):
		print "Oopppps..line %s: %s has empty field" %(line_pos, s_items)
		sys.exit(0)
	line_pos+=1
print "There is no empty field"