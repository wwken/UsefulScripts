#!/usr/bin/python 

""" README 
Author: Ken Wu

This is a library file regarding to all io operations

"""

from os import listdir
from os.path import isfile, join


"""	
	ensure_front_leading_zeros
		n:			Input number
		min_width:	Min width of the output from the input number

		E.g. if input is 9 as n and 2 as min_width, then the output is 09 (with zero appened in front to make it width 2)
"""
def get_all_files(mypath):
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	return onlyfiles

def read_lines(file_path, is_critical=False, replace_new_line=False):
    file = None
    try:
        file = open(file_path, 'r')
        lines = file.readlines()
        if replace_new_line:
            lines = map(lambda x: x.replace('\n', '') if x else None, lines)
        return lines
    except:
        errro_str='Failed reading the file: %s' % file_path
        if is_critical:
            log.error(errro_str)
        else:
            log.info(errro_str)
        return None
    finally:
        if file:
            file.close()