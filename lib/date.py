#!/usr/bin/python 

""" README 
Author: Ken Wu

This is a library file regarding to all date operations

"""

import datetime
import time

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

def execute_function_on_date_range(start_date, end_date, f):
	for single_date in daterange(start_date, end_date):
		f(single_date)

"""	
	create_date
		date_str:		Date wanted to be created.  E.g. 20150501
		date_format:	Date formatted supplied
"""
def create_date(date_str, date_format='%Y%m%d'):
	return datetime.datetime.strptime(date_str, date_format).date()

